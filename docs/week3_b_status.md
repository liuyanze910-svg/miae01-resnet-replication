# Week 3 Run Record - Member B

Member B completed the remaining training seeds for the reduced-budget ResNet-32 experiment with horizontal flipping. Together with seed 42 from Week 2, these runs provide the planned three-seed estimate for this model and augmentation setting.

## Fixed experiment setting

| Item | Setting |
| --- | --- |
| Model | ResNet-32 with 464,154 trainable parameters |
| Training seeds | `42`, `43`, and `44` |
| Data split seed | `2026` |
| Dataset split | 45,000 training, 5,000 validation, and 10,000 independent test images |
| Augmentation | Four-pixel padding, random 32 x 32 crop, and random horizontal flipping |
| Training budget | 16,000 updates with batch size 128 |
| Optimizer | SGD, momentum `0.9`, weight decay `0.0001` |
| Learning-rate schedule | `0.1` through update 8,000, `0.01` through update 12,000, then `0.001` through update 16,000 |
| Primary metric | `test.error_pct` from the model evaluated after update 16,000 |

## Three-seed results

| Seed | Final validation accuracy | Final test accuracy | Final test error | Runtime |
| ---: | ---: | ---: | ---: | ---: |
| 42 | 90.56% | 90.22% | 9.78% | 10,425.936 s |
| 43 | 89.78% | 90.05% | 9.95% | 10,141.764 s |
| 44 | 90.34% | 89.86% | 10.14% | 9,722.363 s |
| **Mean** | - | **90.04%** | **9.96%** | - |
| **Sample standard deviation** | - | **0.18 pp** | **0.18 pp** | - |

The unrounded mean test error is 9.9567%, and the sample standard deviation across the three training seeds is 0.1801 percentage points. The three runs took 30,290.063 seconds in total, approximately 8 hours 24 minutes 50 seconds.

## Interpretation

The paper reports 7.51% test error for ResNet-32 in Table 6. This project's reduced-budget three-seed mean is 2.45 percentage points higher after rounding. This is not an exact contradiction of the paper because the project intentionally uses 16,000 instead of 64,000 updates and reserves 5,000 training images for validation. The result should therefore be described as a reduced-budget reproduction.

The three ResNet-32 seeds are internally consistent: their test errors span only 0.36 percentage points. A final multi-seed verdict about the paper's depth claim also requires the matched ResNet-20 results under the same three seeds and training protocol.

## Reproducibility record

Seed 42 remains archived in `docs/results/week2/resnet32-flip-seed42/`. Portable copies for seeds 43 and 44 are in `docs/results/week3/resnet32-flip-seed43/` and `docs/results/week3/resnet32-flip-seed44/`. Each directory contains `metrics.csv`, `run_config.json`, `summary.json`, and `revision.txt`.

All three runs use training code commit `5242c9337d8558343173534fbc3dd880fd6fb2eb` and `configs/reduced_budget.json` with SHA-256 `2fa72464c33c3fa125ec5f53d811391be1e3653d4514d7d3f98d47b2570b194a`. The new runs used Python 3.12.16, PyTorch 2.10.0, NumPy 2.2.3, and a Mac CPU.
