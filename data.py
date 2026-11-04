"""Download, verify and read the official CIFAR-10 binary archive."""

import argparse
import hashlib
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset

FILENAME = "cifar-10-binary.tar.gz"
URL = f"https://cave.cs.toronto.edu/kriz/{FILENAME}"
MD5 = "c32a1d4ab5d03f1284b67883e8d87530"
TRAIN_FILES = tuple(f"data_batch_{i}.bin" for i in range(1, 6))
TEST_FILE = "test_batch.bin"


def check_archive(path):
    with path.open("rb") as source:
        checksum = hashlib.file_digest(source, "md5").hexdigest()
    if checksum != MD5:
        raise ValueError(f"CIFAR-10 checksum mismatch. Replace the archive: {path}")


def get_archive(data_dir):
    path = data_dir / FILENAME
    if path.exists():
        check_archive(path)
        return path
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading CIFAR-10 (~162 MB): {URL}", flush=True)
    try:
        with tempfile.TemporaryDirectory(dir=data_dir) as temporary:
            download = Path(temporary) / FILENAME
            with urllib.request.urlopen(URL, timeout=60) as response, download.open("wb") as target:
                shutil.copyfileobj(response, target)
            check_archive(download)
            download.replace(path)
    except OSError as exc:
        raise RuntimeError(f"Download failed. Place {FILENAME} in {data_dir.resolve()} and retry.") from exc
    return path


def read_batches(path, *, include_test):
    names = TRAIN_FILES + (TEST_FILE,) if include_test else TRAIN_FILES
    batches = {}
    with tarfile.open(path, "r|gz") as archive:
        for member in archive:
            if not member.isfile() or not member.name.startswith("cifar-10-batches-bin/"):
                continue
            name = member.name.split("/", 1)[1]
            if name in names:
                with archive.extractfile(member) as source:
                    raw = source.read()
                batches[name] = np.frombuffer(raw, dtype=np.uint8).reshape(10000, 3073)
            if len(batches) == len(names):
                break
    train = np.concatenate([batches[name] for name in TRAIN_FILES])
    test = batches[TEST_FILE] if include_test else None
    return train, test


class ImageDataset(Dataset):
    def __init__(self, records, indices, mean, *, augment=False, flip=False):
        self.records = records
        self.indices = indices
        self.mean = mean
        self.augment = augment
        self.flip = flip

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, index):
        record = self.records[self.indices[index]]
        image = torch.from_numpy(record[1:].astype(np.float32).reshape(3, 32, 32))
        image = image.div_(255).sub_(self.mean)
        if self.augment:
            image = F.pad(image, (4, 4, 4, 4))
            top, left = torch.randint(0, 9, (2,)).tolist()
            image = image[:, top:top + 32, left:left + 32]
            if self.flip and torch.rand(()).item() < 0.5:
                image = image.flip(-1)
        return image, int(record[0])


def datasets(data_dir, config, *, synthetic):
    smoke = config["mode"] == "smoke"
    rng = np.random.default_rng(config["split_seed"])
    if synthetic:
        train = rng.integers(0, 256, (320, 3073), dtype=np.uint8)
        train[:, 0] %= 10
        train_indices, val_indices = np.arange(256), np.arange(256, 320)
        test = None
    else:
        train, test = read_batches(get_archive(data_dir), include_test=not smoke)
        indices = rng.permutation(len(train))
        train_indices, val_indices = indices[5000:], indices[:5000]
        if smoke:
            train_indices, val_indices = train_indices[:256], val_indices[:64]

    # Estimate each channel/pixel mean on training examples only, in bounded chunks.
    total = np.zeros(3072, dtype=np.float64)
    for chunk in np.array_split(train_indices, (len(train_indices) + 999) // 1000):
        total += train[chunk, 1:].sum(axis=0)
    mean = torch.tensor(total.reshape(3, 32, 32) / (255 * len(train_indices)), dtype=torch.float32)
    train_set = ImageDataset(train, train_indices, mean, augment=True, flip=config["horizontal_flip"])
    val_set = ImageDataset(train, val_indices, mean)
    test_set = ImageDataset(test, np.arange(len(test)), mean) if test is not None else None
    return train_set, val_set, test_set


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    args = parser.parse_args()
    print(f"Verified archive: {get_archive(args.data_dir).resolve()}")
