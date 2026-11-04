"""Shared ResNet-20/32 entry point for smoke tests and paper-budget runs."""

import argparse
import csv
import json
import math
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

from data import datasets
from model import CifarResNet

FIELDS = ("step", "split", "samples", "loss", "accuracy_pct", "error_pct", "learning_rate", "elapsed_seconds")


class Metrics:
    def __init__(self):
        self.samples = 0
        self.loss_sum = 0.0
        self.correct = 0

    def add(self, logits, labels, loss):
        if not math.isfinite(loss):
            raise FloatingPointError(f"Non-finite loss: {loss}")
        self.samples += labels.numel()
        self.loss_sum += loss * labels.numel()
        self.correct += logits.detach().argmax(dim=1).eq(labels).sum().item()

    def values(self):
        accuracy = 100 * self.correct / self.samples
        return dict(samples=self.samples, loss=self.loss_sum / self.samples,
                    accuracy_pct=accuracy, error_pct=100 - accuracy)


@torch.inference_mode()
def evaluate(model, loader, criterion, device):
    model.eval()
    metrics = Metrics()
    for images, labels in loader:
        labels = labels.to(device)
        logits = model(images.to(device))
        metrics.add(logits, labels, criterion(logits, labels).item())
    return metrics.values()


def training_batches(loader):
    while True:
        yield from loader


def write_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=int, choices=(20, 32), default=20)
    parser.add_argument("--config", type=Path, default=Path("configs/smoke.json"))
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--no-flip", action="store_true")
    parser.add_argument("--synthetic", action="store_true", help="Offline smoke test with generated data")
    parser.add_argument("--output", type=Path, help="New directory for this run")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8-sig"))
    if config["mode"] not in ("smoke", "full"):
        parser.error("configuration mode must be smoke or full")
    if args.synthetic and config["mode"] != "smoke":
        parser.error("--synthetic is only available in smoke mode")
    if args.seed is not None:
        config["seed"] = args.seed
    if args.no_flip:
        config["horizontal_flip"] = False
    device_name = args.device
    if device_name == "auto":
        device_name = "cuda" if torch.cuda.is_available() else "cpu"
    if device_name == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA is unavailable. Use --device cpu or install a compatible CUDA build.")
    device = torch.device(device_name)
    torch.set_num_threads(2)
    torch.manual_seed(config["seed"])
    torch.backends.cudnn.benchmark = False

    train, validation, test = datasets(args.data_dir, config, synthetic=args.synthetic)
    batch_size = config["batch_size"]
    generator = torch.Generator().manual_seed(config["seed"])
    train_loader = DataLoader(train, batch_size=batch_size, shuffle=True, generator=generator,
                              drop_last=True, num_workers=0)
    if not len(train_loader):
        parser.error("batch size exceeds the available training samples")
    validation_loader = DataLoader(validation, batch_size=batch_size, num_workers=0)
    model = CifarResNet(args.depth).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=config["learning_rate"],
                                momentum=config["momentum"], weight_decay=config["weight_decay"])

    dataset_name = "synthetic" if args.synthetic else "cifar10"
    timestamp = datetime.now(timezone.utc)
    run_id = timestamp.strftime("%Y%m%dT%H%M%S%fZ")
    output = args.output or Path("runs") / f"resnet{args.depth}-{dataset_name}-{config['mode']}-{run_id}"
    output.mkdir(parents=True, exist_ok=False)
    metadata = {
        **config, "depth": args.depth, "dataset": dataset_name,
        "device": str(device), "device_name": torch.cuda.get_device_name() if device.type == "cuda" else "CPU",
        "python": platform.python_version(), "torch": str(torch.__version__), "numpy": np.__version__,
        "platform": platform.platform(), "started_utc": timestamp.isoformat(),
        "parameters": sum(p.numel() for p in model.parameters()),
        "train_samples": len(train), "validation_samples": len(validation),
        "test_samples": len(test) if test is not None else 0,
    }
    write_json(output / "run_config.json", metadata)
    started = time.perf_counter()
    print(f"ResNet-{args.depth} | {dataset_name} | {config['mode']} | {device} | "
          f"{metadata['parameters']:,} params | {config['max_steps']} updates", flush=True)

    with (output / "metrics.csv").open("w", encoding="utf-8", newline="") as log:
        writer = csv.DictWriter(log, fieldnames=FIELDS)
        writer.writeheader()

        def log_row(step, split, values):
            writer.writerow({"step": step, "split": split, **values,
                             "learning_rate": optimizer.param_groups[0]["lr"],
                             "elapsed_seconds": round(time.perf_counter() - started, 3)})
            log.flush()
            print(f"step {step:>5} | {split:<10} | loss {values['loss']:.4f} | "
                  f"accuracy {values['accuracy_pct']:.2f}%", flush=True)

        model.train()
        training = Metrics()
        batches = training_batches(train_loader)
        final_step = config["max_steps"]
        for step in range(1, final_step + 1):
            images, labels = next(batches)
            labels = labels.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(images.to(device))
            loss = criterion(logits, labels)
            loss_value = loss.item()
            training.add(logits, labels, loss_value)
            loss.backward()
            optimizer.step()

            if step % config["log_every"] == 0 or step == final_step:
                log_row(step, "train", training.values())
                training = Metrics()
            if step % config["val_every"] == 0 or step == final_step:
                validation_metrics = evaluate(model, validation_loader, criterion, device)
                log_row(step, "validation", validation_metrics)
                model.train()
            if step in config["lr_milestones"]:
                for group in optimizer.param_groups:
                    group["lr"] *= 0.1

        summary = {"status": "completed", "mode": config["mode"], "dataset": dataset_name,
                   "depth": args.depth, "seed": config["seed"], "steps": final_step,
                   "parameters": metadata["parameters"], "validation": validation_metrics}
        if test is not None:
            test_loader = DataLoader(test, batch_size=batch_size, num_workers=0)
            summary["test"] = evaluate(model, test_loader, criterion, device)
            log_row(final_step, "test", summary["test"])
        summary["elapsed_seconds"] = round(time.perf_counter() - started, 3)
        write_json(output / "summary.json", summary)
    print(f"Completed. Logs: {output.resolve()}", flush=True)


if __name__ == "__main__":
    main()
