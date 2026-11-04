# Reproducing ResNet-20 and ResNet-32 on CIFAR-10

|                                                   |            |
| ------------------------------------------------- | ---------- |
| \*\*MIAE01 Machine Learning Programming and Tools | Week 1\*\* |

This project reproduces part of the CIFAR-10 experiment in He et al.'s *Deep Residual Learning for Image Recognition*. We ask whether **ResNet-32 has a lower mean test error rate than ResNet-20** under a shared training and evaluation protocol. Table 6 gives the paper's final test error rates. The middle panel of Figure 6 shows how errors change during training. [Paper, Section 4.2](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf#page=7)

| Model     | Parameters (approx.) | CIFAR-10 test error in Table 6 |
| --------- | -------------------: | -----------------------------: |
| ResNet-20 |                0.27M |                          8.75% |
| ResNet-32 |                0.46M |                          7.51% |

**Week 1 progress.** ResNet-20 completed eight updates on real CIFAR-10 data using a Windows CPU. The archived logs show that data loading, training, validation, and result export all ran successfully. The full runs will be evaluated on the independent test set and compared with Table 6. [Week 1 run record](docs/week1_status.md)

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

## 3. Proposed full-run configuration

`configs/paper_budget.json` uses 45,000 training images, 5,000 validation images, and 10,000 independent test images. The split seed is `2026`. The batch size is `128`, and the training budget is `64,000` updates. SGD starts at a learning rate of `0.1` and reduces it by a factor of 10 after updates `32,000` and `48,000`. [Experimental protocol and differences from the paper](docs/experiment_plan.md)

The commands below use training seed `42` as an example. Use at least three agreed seeds across the runs, with the same set of seeds for each condition. `--seed` controls model initialization, training-data shuffling, and random augmentation. The `split_seed` setting fixes the partition separately. The program reports an error if `--device cuda` is selected in an environment without CUDA support.

```bash
python train.py --config configs/paper_budget.json --depth 20 --seed 42 --device cuda
python train.py --config configs/paper_budget.json --depth 32 --seed 42 --device cuda
python train.py --config configs/paper_budget.json --depth 20 --seed 42 --no-flip --device cuda
```

The run with horizontal flipping disabled uses the same model depth, data partition, training budget, and other hyperparameters as the ResNet-20 baseline. Each full run evaluates the final model on the independent test set once. Use test error as the primary metric and report the mean and standard deviation across seeds. Also record accuracy, parameter count, and elapsed time.

## 4. Expected outputs and runtime

Each run creates a directory under `runs/`, such as `runs/resnet20-cifar10-smoke-<timestamp>/`.

| File              | What to look for                                                                                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `run_config.json` | Device, package versions, seeds, dataset sizes, model depth, and training settings.                                                                                      |
| `metrics.csv`     | Training and validation records with step, sample count, loss, accuracy, error rate, learning rate, and elapsed time. A full run adds a `test` row.                      |
| `summary.json`    | Final metrics and run status. A successful real-data smoke test reports `status` as `completed`, `dataset` as `cifar10`, and `steps` as `8`, with a `validation` result. |

The archived ResNet-20 smoke test took about **1.4 seconds** for training and validation on Windows 11 with Python 3.12.14 and PyTorch 2.10.0+cpu. The logged interval excludes dataset download, loading, and model setup. The first download is approximately 162 MB. [Archived run summary](docs/cifar10_smoke/summary.json)

A separate CPU benchmark used two threads and batch size 128, with four warm-up steps and 16 timed steps. Extrapolating to 64,000 updates gives roughly six hours for ResNet-20 and ten hours for ResNet-32 on that machine. These estimates cover training updates only. Full-run and GPU runtimes have yet to be measured.

## 5. Project layout and sources

| Path                                             | Purpose                                                                                |
| ------------------------------------------------ | -------------------------------------------------------------------------------------- |
| `model.py`                                       | CIFAR-10 versions of ResNet-20 and ResNet-32 with Option A shortcuts.                  |
| `data.py`                                        | CIFAR-10 download and verification, fixed partitions, and training augmentation.       |
| `train.py`                                       | Shared entry point for training, evaluation, and logging.                              |
| `requirements.txt` and `configs/`                | Package versions and experiment settings.                                              |
| `docs/experiment_plan.md` and `docs/sources.md`  | Experimental protocol, differences from the paper, and source and license information. |
| `docs/week1_status.md` and `docs/cifar10_smoke/` | Week 1 status and the three archived real-data smoke-test logs.                        |

The project implements the paper independently. Yerlan Idelbayev's `akamaster/pytorch_resnet_cifar10` served as an architectural reference and uses the BSD 2-Clause license. This project includes no source files or weights from that repository. [Source and version notes](docs/sources.md) · [Reference implementation license](https://github.com/akamaster/pytorch_resnet_cifar10/blob/master/LICENSE)

## 6. Repository submissions

Archive logs needed for assessment or reproducibility in the appropriate experiment folder under `docs/` and commit them with the related code, configuration, and documentation. Keep datasets, checkpoints, files over 50 MB, and credentials outside the repository.
