# Sources, Licenses, and Starting Version

| Item | Source and license information |
| --- | --- |
| Model and experiment code | Independently implemented from Sections 3 and 4.2 of He et al. (CVPR 2016). The first Week 1 code submission is recorded in [PR #1](https://github.com/liuyanze910-svg/miae01-resnet-replication/pull/1), where its commit is shown as `9771ed4`. The project license is for the team to confirm. |
| Public PyTorch reference | Yerlan Idelbayev's `akamaster/pytorch_resnet_cifar10` uses the BSD 2-Clause license. It was consulted to check the CIFAR-10 architecture. This project includes no source files or weights from that repository. If the team later adopts code from it, record the full upstream commit SHA and retain its license. |
| CIFAR-10 | The project downloads the official binary archive and verifies it against the MD5 checksum published on the dataset page. The dataset and model artifacts are kept locally. Cite Alex Krizhevsky's *Learning Multiple Layers of Features from Tiny Images* (2009). |
| Runtime dependencies | The project pins `torch==2.10.0` and `numpy==2.2.3`. Each run logs the exact builds it used. |

- [Original ResNet paper](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf)
- [PyTorch reference implementation license](https://github.com/akamaster/pytorch_resnet_cifar10/blob/master/LICENSE)
- [Official CIFAR-10 dataset and documentation](https://cave.cs.toronto.edu/kriz/cifar.html)
