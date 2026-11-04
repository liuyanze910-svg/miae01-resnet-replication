# CIFAR-10 上的 ResNet-20 与 ResNet-32 复现

**MIAE01 机器学习编程与工具 · 论文复现项目 · 第 1 周**

本项目复现 He 等人《Deep Residual Learning for Image Recognition》中 CIFAR-10 的部分实验。我们将在相同的数据划分、训练预算、数据增强和评估流程下，检验 **ResNet-32 的平均测试错误率是否低于 ResNet-20**。原论文第 4.2 节的表 6 提供最终测试错误率，图 6 中间面板提供训练过程的对照。[原论文](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf#page=7)

| 原论文表 6    | 参数量（约值） | CIFAR-10 测试错误率 |
| --------- | ------: | -------------: |
| ResNet-20 |   0.27M |          8.75% |
| ResNet-32 |   0.46M |          7.51% |

**当前进度。** ResNet-20 已在 Windows CPU 上用真实 CIFAR-10 完成 8 次参数更新。第 1 周的日志用于确认数据读取、训练、验证和结果导出能完整运行。正式实验结束后再用独立测试集和原论文比较。[短跑验收记录](docs/week1_status.md)

## 1. 从新环境开始

在项目根目录，也就是能看到 `train.py` 和 `requirements.txt` 的目录，打开已能运行 `conda` 的终端。以下为 Windows 或 Linux 的 CPU 安装步骤。

```bash
conda create -n resnet-cifar10 python=3.12 pip -y
conda activate resnet-cifar10
python -m pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python -c "import torch, numpy; print(torch.__version__, numpy.__version__)"
```

应看到 PyTorch `2.10.0`（CPU 构建可能显示 `2.10.0+cpu`）和 NumPy `2.2.3`。已有同版本环境的组员可以直接激活该环境。使用 NVIDIA GPU 时，请按官方安装说明选择与驱动兼容的 PyTorch `2.10.0` CUDA 构建，再安装 `requirements.txt` 中的依赖。训练前可用 `python -c "import torch; print(torch.cuda.is_available())"` 确认是否返回 `True`。[PyTorch 安装说明](https://pytorch.org/get-started/previous-versions/)

## 2. 下载 CIFAR-10 并运行短试验

```bash
python data.py
python train.py --config configs/smoke.json --depth 20 --device cpu
```

`data.py` 将官方 CIFAR-10 二进制版下载到 `data/cifar-10-binary.tar.gz`，校验后显示 `Verified archive:`。如果下载超时，可手动下载 **CIFAR-10 binary version**，把压缩包原样放进 `data/`，再运行 `python data.py`。所有路径均相对于项目根目录。模型从随机初始化开始训练，无需下载预训练权重。[CIFAR-10 官方下载页](https://cave.cs.toronto.edu/kriz/cifar.html)

短试验取 **256 张训练图和 64 张验证图**，每批 32 张，共 8 次更新。完成后终端会显示 `Completed. Logs:`，并打印本次输出目录。

| 短试验              | 从项目根目录运行                                                                        |
| ---------------- | ------------------------------------------------------------------------------- |
| ResNet-20 基线     | `python train.py --config configs/smoke.json --depth 20 --device cpu`           |
| ResNet-32 深度对照   | `python train.py --config configs/smoke.json --depth 32 --device cpu`           |
| ResNet-20 关闭水平翻转 | `python train.py --config configs/smoke.json --depth 20 --no-flip --device cpu` |

没有数据包时，可在任一短试验命令末尾加 `--synthetic`，用生成数据检查程序。提交真实数据短试验时，确认 `summary.json` 中的 `dataset` 是 `cifar10`。

## 3. 正式实验配置草案

`configs/paper_budget.json` 使用 **45,000 张训练图、5,000 张验证图和 10,000 张独立测试图**。数据划分种子为 `2026`，批量大小为 `128`，总计 `64,000` 次更新。SGD 初始学习率为 `0.1`，在第 `32,000` 和 `48,000` 次更新后各除以 10。与论文的设置差异和待确认项见[实验方案](docs/experiment_plan.md)。

下面用训练种子 `42` 演示同一轮对照。正式统计至少使用 3 个由小组确认的共同种子，每个实验使用同一组种子。`--seed` 控制模型初始化、训练打乱和随机增强，固定的数据划分由配置中的 `split_seed` 控制。指定 `--device cuda` 时，若 CUDA 不可用，程序会直接提示。

```bash
python train.py --config configs/paper_budget.json --depth 20 --seed 42 --device cuda
python train.py --config configs/paper_budget.json --depth 32 --seed 42 --device cuda
python train.py --config configs/paper_budget.json --depth 20 --seed 42 --no-flip --device cuda
```

关闭翻转的实验沿用 ResNet-20 基线的划分、种子、训练步数及其他超参数。每次正式运行在最后一次更新后评估独立测试集。最终比较以测试错误率为主，同时记录准确率、参数量和运行耗时。每项正式结果汇总至少 3 个种子的均值与标准差。

## 4. 预期输出与耗时

每次运行都会在 `runs/` 下创建独立目录，例如 `runs/resnet20-cifar10-smoke-<时间戳>/`。

| 文件                | 内容与核对方法                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------ |
| `run_config.json` | 实际设备、依赖版本、随机种子、数据规模、模型深度和训练设置。                                                             |
| `metrics.csv`     | 训练及验证的步数、样本数、loss、准确率、错误率、学习率与耗时。正式实验完成后增加一行 `test`。                                       |
| `summary.json`    | 最终指标和完成状态。真实数据短试验应显示 `status: completed`、`dataset: cifar10`、`steps: 8`，并有 `validation` 结果。 |

ResNet-20 的 CIFAR-10 短试验在 Windows 11、Python 3.12.14、PyTorch 2.10.0+cpu 环境中，实测训练和验证合计 **约 1.4 秒**。下载、数据读取和模型准备另计。首次下载约 162 MB，所需时间取决于网络。[真实运行摘要](docs/cifar10_smoke/summary.json)

正式配置的 CPU 耗时按短测估算。在同一台 Windows 电脑上，使用 2 个 CPU 线程、批量 128，预热 4 步后计时 16 步。按测得速度推算，64,000 次训练更新约需 **ResNet-20 6 小时、ResNet-32 10 小时**。该估算仅计训练更新，验证和测试另计。完整运行与 GPU 耗时待正式实验后记录。

## 5. 文件、来源与版本

| 路径                                           | 用途                                                   |
| -------------------------------------------- | ---------------------------------------------------- |
| `model.py`                                   | 根据论文实现 CIFAR-10 版 ResNet-20、ResNet-32 和 Option A 捷径。 |
| `data.py`                                    | 下载和校验 CIFAR-10，固定数据划分并执行训练增强。                        |
| `train.py`                                   | 共用训练入口、验证与测试流程、日志导出。                                 |
| `requirements.txt`、`configs/`                | 依赖版本与两种实验配置。                                         |
| `docs/experiment_plan.md`、`docs/sources.md`  | 论文设置对照、实验计划、代码和数据来源与许可。                              |
| `docs/week1_status.md`、`docs/cifar10_smoke/` | 第 1 周验收记录和真实短试验的三份日志。                                |

本项目依据论文独立实现，新增的核心文件为 `model.py`、`data.py` 和 `train.py`。课程列出的公开对照仓库为 Yerlan Idelbayev 的 `akamaster/pytorch_resnet_cifar10`，采用 BSD 2-Clause 许可证。该仓库用于核对模型结构，当前项目没有纳入或修改其源文件。项目起始版本暂记为 `week1-draft`，推送后在 `docs/sources.md` 记录该项目起始提交的完整 SHA。[来源说明](docs/sources.md) · [公开对照实现及其许可证](https://github.com/akamaster/pytorch_resnet_cifar10/blob/master/LICENSE)

## 6. 仓库提交

将用于验收或结果复核的实验日志归档到 `docs/` 下对应的实验目录，并随相关代码、配置和文档一起提交。数据集、模型检查点、超过 50 MB 的文件和凭据留在仓库之外。
