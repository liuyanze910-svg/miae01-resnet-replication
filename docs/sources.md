# 来源、许可和起始版本

| 内容 | 起始来源与许可 |
| --- | --- |
| 模型和复现实验代码 | 依据 He 等人的 CVPR 2016 论文第 3 节、第 4.2 节编写。起始版本标识为 `week1-draft`，首次提交的实际 Git SHA 由 A 提交后用 `git rev-parse HEAD` 记录。项目对外开源许可由小组确认 |
| 公开 PyTorch 对照实现 | Yerlan Idelbayev 的 `akamaster/pytorch_resnet_cifar10`，BSD 2-Clause。查阅该仓库核对 CIFAR 架构和公开实现背景。启动包不包含其源文件或模型权重。如果小组改用该实现，应固定完整 commit SHA 并保留原 `LICENSE` |
| CIFAR-10 | 从作者页面下载官方二进制版，按作者公布的 MD5 校验。数据和模型产物留在本地。数据集引用为 Alex Krizhevsky, *Learning Multiple Layers of Features from Tiny Images*, 2009 |
| 运行依赖 | `torch==2.10.0`，`numpy==2.2.3`。具体构建号由运行日志记录 |

- [ResNet 原论文](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf)
- [公开对照实现及原许可](https://github.com/akamaster/pytorch_resnet_cifar10/blob/master/LICENSE)
- [CIFAR-10 官方数据和说明](https://cave.cs.toronto.edu/kriz/cifar.html)
