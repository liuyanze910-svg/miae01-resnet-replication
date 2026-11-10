# Week 2 Run Record - Member B

Member B evaluates the depth comparison with ResNet-32 and horizontal flipping enabled. This run uses the same data split, training seed, update budget, optimizer, learning-rate schedule, augmentation policy, and final evaluation rule as Member A's ResNet-20 baseline.

## First depth-comparison run

| Item | Setting |
| --- | --- |
| Model and seeds | ResNet-32, training seed `42`, split seed `2026` |
| Schedule | 16,000 updates at batch size 128. Learning rate `0.1` through update 8,000, `0.01` through update 12,000, and `0.001` through update 16,000. |
| Dataset | 45,000 training, 5,000 validation, and 10,000 independent test images |
| Augmentation | Four-pixel padding, random 32 x 32 crop, and random horizontal flipping |
| Primary metric | `test.error_pct` in `summary.json`, evaluated on the model at update 16,000 |
| Run status | Completed on 2026-11-10 at 01:41 (UTC+08:00) after about 2 hours and 54 minutes |
| Final validation accuracy | 90.56% on 5,000 images |
| Final test accuracy | 90.22% on 10,000 images |
| Final test error | **9.78%** on 10,000 images |

The run used a Mac CPU with Python 3.12.16, PyTorch 2.10.0, NumPy 2.2.3, and 464,154 trainable parameters. The official CIFAR-10 binary archive passed the published MD5 check before training. The portable copies of the run configuration, metrics, summary, and code revision are in [the ResNet-32 seed-42 results directory](results/week2/resnet32-flip-seed42/).

## Matched seed-42 comparison

| Model | Parameters | Test accuracy | Test error |
| --- | ---: | ---: | ---: |
| ResNet-20 (Member A) | 269,722 | 89.77% | 10.23% |
| ResNet-32 (Member B) | 464,154 | 90.22% | 9.78% |

For seed 42, the ResNet-32 test error is 0.45 percentage points lower than the matched ResNet-20 baseline. This single run is preliminary evidence in the direction of the paper's depth claim. A claim verdict requires the remaining seeds and the mean plus sample standard deviation across all three runs.

## Reproduction note

The paper reports a 7.51% test error for ResNet-32 in Table 6. This reduced-budget run is 2.27 percentage points higher. The comparison is not yet final because the project uses 16,000 rather than 64,000 updates, a fixed 45,000/5,000 training-validation split, a single CPU, and only one completed seed at this milestone. These deviations and the complete three-seed statistics will be reported in the final analysis.

