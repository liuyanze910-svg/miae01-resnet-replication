# Reproducing ResNet-20 and ResNet-32 on CIFAR-10

**MIAE01 Machine Learning Programming and Tools · Week 2**

This project reproduces part of the CIFAR-10 experiment in He et al.'s *Deep Residual Learning for Image Recognition*. We ask whether **ResNet-32 has a lower mean test error rate than ResNet-20** under a shared training and evaluation protocol. Table 6 gives the paper's final test error rates. The middle panel of Figure 6 shows how errors change during training. [Paper, Section 4.2](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf#page=7)

| Model     | Parameters (approx.) | CIFAR-10 test error in Table 6 |
| --------- | -------------------: | -----------------------------: |
| ResNet-20 |                0.27M |                          8.75% |
| ResNet-32 |                0.46M |                          7.51% |

**Week 1 progress.** ResNet-20 completed eight updates on real CIFAR-10 data using a Windows CPU. The archived logs show that data loading, training, validation, and result export all ran successfully. The full runs will be evaluated on the independent test set and compared with Table 6. [Week 1 run record](docs/week1_status.md)

**Week 2 baseline.** Member A runs ResNet-20 with horizontal flipping enabled at probability 0.5, using seed 42 for the first 16,000-update run. This baseline supports Member B's depth comparison and Member C's horizontal-flip comparison. [Member A run record](docs/week2_status.md) · [Report draft and differences from the paper](docs/week2_report_draft.md)

## 1. Set up the environment

Open a terminal with Conda available. Run the commands from the project root, where `train.py` and `requirements.txt` are located. The following setup uses the CPU build on Windows or Linux.

```bash
conda create -n resnet-cifar10 python=3.12 pip -y
conda activate resnet-cifar10
python -m pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python -c "import torch, numpy; print(torch.__version__, numpy.__version__)"
```

The version check should show PyTorch `2.10.0` (the CPU build may display `2.10.0+cpu`) and NumPy `2.2.3`. An existing environment with those versions can also be used. For an NVIDIA GPU, install a PyTorch `2.10.0` CUDA build compatible with your driver, then install the dependencies in `requirements.txt`. Use `python -c "import torch; print(torch.cuda.is_available())"` to check whether the environment can access the GPU. [PyTorch installation instructions](https://pytorch.org/get-started/previous-versions/)

## 2. Download CIFAR-10 and run a smoke test

```bash
python data.py
python train.py --config configs/smoke.json --depth 20 --device cpu
```

The data script downloads and verifies the official binary archive at `data/cifar-10-binary.tar.gz`. It prints `Verified archive:` after verification. If the download times out, download **CIFAR-10 binary version** manually, place the unopened archive in `data/`, and rerun `python data.py`. Paths are relative to the project root. Training starts from randomly initialized weights. [Official CIFAR-10 download page](https://cave.cs.toronto.edu/kriz/cifar.html)

The smoke test uses 256 training images and 64 validation images. It runs eight updates with a batch size of 32. The terminal prints `Completed. Logs:` followed by the output directory when the run finishes.

| Smoke test                                  | Command from the project root                                                   |
| ------------------------------------------- | ------------------------------------------------------------------------------- |
| ResNet-20 baseline                          | `python train.py --config configs/smoke.json --depth 20 --device cpu`           |
| ResNet-32 depth comparison                  | `python train.py --config configs/smoke.json --depth 32 --device cpu`           |
| ResNet-20 with horizontal flipping disabled | `python train.py --config configs/smoke.json --depth 20 --no-flip --device cpu` |

Add `--synthetic` to a smoke-test command to check the pipeline with generated inputs when CIFAR-10 is unavailable. For the real-data smoke test, check that `summary.json` reports `dataset` as `cifar10`.

## 3. Shared 16,000-update experiment

Use `configs/reduced_budget.json` for the team comparison. It uses 45,000 training images, 5,000 validation images, and 10,000 independent test images. The split seed is `2026` and the batch size is `128`. SGD starts at a learning rate of `0.1` and reduces it by a factor of 10 after updates `8,000` and `12,000`. The run ends at update `16,000`. The earlier 64,000-update configuration and pilot logs are kept separately under the paper budget.

The Week 2 baseline uses training seed `42`. The proposed three-seed set is `42`, `43`, and `44`. Use the same seeds across conditions once the team confirms them. `--seed` controls model initialization, training-data shuffling, and random augmentation. The `split_seed` setting fixes the partition separately. Run the command from the repository root. If the archive is cached elsewhere, supply its containing folder with `--data-dir`.

```powershell
python -B -u train.py --config configs/reduced_budget.json --depth 20 --seed 42 --device cpu --output runs/week2-a-resnet20-seed42-16k
```

Record the code revision used and keep the three run logs together. Each full run evaluates the final model on the independent test set once. Use `test.error_pct` from `summary.json` as the primary metric. Report the mean and sample standard deviation after all three seeds have finished.

## 4. Expected outputs and runtime

Each run creates a directory under `runs/`, such as `runs/resnet20-cifar10-smoke-<timestamp>/`.

| File              | What to look for                                                                                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `run_config.json` | Device, package versions, seeds, dataset sizes, model depth, and training settings.                                                                                      |
| `metrics.csv`     | Training and validation records with step, sample count, loss, accuracy, error rate, learning rate, and elapsed time. A full run adds a `test` row.                      |
| `summary.json`    | Final metrics and run status. A completed Week 2 baseline reports `status` as `completed`, `steps` as `16000`, and a `test` result covering 10,000 images. |

The archived ResNet-20 smoke test took about **1.4 seconds** for training and validation on Windows 11 with Python 3.12.14 and PyTorch 2.10.0+cpu. The logged interval excludes dataset download, loading, and model setup. The first download is approximately 162 MB. [Archived run summary](docs/cifar10_smoke/summary.json)

The completed 16,000-update seed-42 baseline took **70 minutes and 16 seconds** for training and evaluation on an Intel Core Ultra 5 336H CPU with two PyTorch threads. [Baseline run summary](docs/results/week2/resnet20-flip-seed42/summary.json)

## 5. Project layout and sources

| Path                                             | Purpose                                                                                |
| ------------------------------------------------ | -------------------------------------------------------------------------------------- |
| `model.py`                                       | CIFAR-10 versions of ResNet-20 and ResNet-32 with Option A shortcuts.                  |
| `data.py`                                        | CIFAR-10 download and verification, fixed partitions, and training augmentation.       |
| `train.py`                                       | Shared entry point for training, evaluation, and logging.                              |
| `requirements.txt` and `configs/`                | Package versions and experiment settings.                                              |
| `docs/experiment_plan.md` and `docs/sources.md`  | Week 1 planning record and source and license information. |
| `docs/week2_status.md` and `docs/week2_report_draft.md` | Week 2 baseline record and the draft reproduction setup. |
| `docs/results/week2/resnet20-flip-seed42/` | Archived baseline configuration, metrics, summary, and revision. |
| `docs/week1_status.md` and `docs/cifar10_smoke/` | Week 1 status and the three archived real-data smoke-test logs.                        |

The project implements the paper independently. Yerlan Idelbayev's `akamaster/pytorch_resnet_cifar10` served as an architectural reference and uses the BSD 2-Clause license. This project includes no source files or weights from that repository. [Source and version notes](docs/sources.md) · [Reference implementation license](https://github.com/akamaster/pytorch_resnet_cifar10/blob/master/LICENSE)

The Week 2 baseline used the trainer, model, and data loader from commit `5242c9337d8558343173534fbc3dd880fd6fb2eb`. The reduced-budget setup adds `configs/reduced_budget.json`, the two Week 2 documents, and the seed-42 logs listed above. It also updates this README. [Run revision record](docs/results/week2/resnet20-flip-seed42/revision.txt)

## 6. Repository submissions

Archive logs needed for assessment or reproducibility in the appropriate experiment folder under `docs/` and commit them with the related code, configuration, and documentation. Keep datasets, checkpoints, files over 50 MB, and credentials outside the repository.
