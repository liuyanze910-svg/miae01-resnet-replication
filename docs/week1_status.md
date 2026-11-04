# Week 1 Status for Member A

| Check | Status |
| --- | --- |
| Dependencies and training entry point | Verified in the `susu` environment on Windows with Python 3.12.14, PyTorch 2.10.0+cpu, and NumPy 2.2.3. |
| ResNet-20 synthetic smoke test | Completed eight updates with 269,722 trainable parameters. The run produced training and validation logs. [Synthetic run logs](synthetic_smoke/) |
| ResNet-20 smoke test on real CIFAR-10 | Completed eight updates on a Windows CPU on November 4, 2026, at 12:39 Hong Kong time. The training script verified the official archive. [Real-data run logs](cifar10_smoke/) |
| Paper comparison, README, and experimental plan | The drafts are ready. Members A and B still need to agree on the final protocol for comparing the two depths. |
| GitHub submission | Member A opened [PR #1](https://github.com/liuyanze910-svg/miae01-resnet-replication/pull/1) for the initial Week 1 submission. |

## Real-data smoke test results

| Item | Recorded value |
| --- | --- |
| Dataset and settings | CIFAR-10, 256 training images, 64 validation images, batch size 32, learning rate 0.1, and seed 42. |
| Training updates | ResNet-20 completed eight updates with 269,722 trainable parameters. |
| Validation metrics | 1 of 64 images classified correctly, 1.56% accuracy, and cross-entropy loss of 199.95. |
| Original logs | [Run configuration](cifar10_smoke/run_config.json), [metrics](cifar10_smoke/metrics.csv), and [summary](cifar10_smoke/summary.json). |

The smoke test verifies real-data loading, parameter updates, validation, and log export. Its validation metrics reflect a 64-image subset after eight updates. The full reproduction will use the agreed training budget and evaluate on the independent test set.
