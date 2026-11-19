# Week 3 Run Record - Member C

Member C completed the reduced-budget ResNet-20 experiment with horizontal flipping disabled. The three runs use training seeds 42, 43, and 44. The comparison uses Member A's ResNet-20 baseline with flipping enabled.

## Experiment design

Random horizontal flipping presents training images in both orientations. This extension examines how disabling that augmentation changes the test error under the group's training protocol. Both conditions use ResNet-20, the same training seeds and data split, four-pixel padding and random cropping, the same optimizer and learning-rate schedule, and the same evaluation rule. The augmentation setting changed between conditions: the baseline flips with probability 0.5, while the extension disables flipping.

| Item | Setting |
| --- | --- |
| Dataset and model | CIFAR-10 and ResNet-20, 269,722 trainable parameters |
| Training seeds | 42, 43, and 44 |
| Data split | Split seed 2026, 45,000 training, 5,000 validation, and 10,000 independent test images |
| Training | 16,000 updates, batch size 128, SGD, momentum 0.9, weight decay 0.0001 |
| Learning rate | 0.1 initially, reduced to 0.01 after step 8,000 and to 0.001 after step 12,000 |
| Evaluation | Test error from the model after step 16,000 |

## Paired results

Each row compares runs with the same training seed. Difference is the test error with flipping disabled minus the baseline test error, in percentage points (pp).

| Seed | Baseline test error (%) | No-flip test error (%) | Difference (pp) | No-flip logs |
| ---: | ---: | ---: | ---: | --- |
| 42 | 10.23 | 11.98 | +1.75 | [Week 2 seed 42](results/week2/resnet20-no-flip-seed42/) |
| 43 | 10.58 | 12.36 | +1.78 | [Week 3 seed 43](results/week3/resnet20-no-flip-seed43/) |
| 44 | 10.36 | 12.01 | +1.65 | [Week 3 seed 44](results/week3/resnet20-no-flip-seed44/) |
| Mean ± sample SD | 10.39 ± 0.18 | 12.12 ± 0.21 | 1.73 ± 0.07 | |

Mean and sample standard deviation use the three seed-level test errors. The unrounded no-flip mean is 12.1167% and its sample standard deviation is 0.2113 percentage points. The mean paired difference is 1.7267 percentage points. Member A's per-seed baseline results and logs are listed in the [Week 3 baseline record](week3_status.md).

## Preliminary interpretation and limitations

The no-flip test error is higher for each of the three matched seeds, by 1.65 to 1.78 percentage points. Under the group's 16,000-update protocol, these runs suggest that horizontal flipping improved ResNet-20 test accuracy. The comparison covers three seeds and one data split, so the magnitude may vary with the seeds, split, and training conditions.

## Reproducibility

All three no-flip runs completed 16,000 updates and evaluated the final model on 10,000 test images. Each archived run contains its configuration, metrics, summary, and revision record. The training code matches commit `5242c9337d8558343173534fbc3dd880fd6fb2eb`. The local `configs/reduced_budget.json` used for these runs has SHA-256 `d30aba8212eafefe1472734f89fba3e328924f5c71bdec5d0bb79e71848da1a5` and the same configuration values as the shared file. The runs used macOS on arm64, Python 3.12.14, PyTorch 2.10.0, NumPy 2.2.3, and CPU.

Run from the repository root with the required environment and CIFAR-10 archive available. Select a new output directory for each run.

```bash
python -B -u train.py --config configs/reduced_budget.json --depth 20 --seed 43 --no-flip --device cpu --output runs/c_no_flip_16k_seed43
python -B -u train.py --config configs/reduced_budget.json --depth 20 --seed 44 --no-flip --device cpu --output runs/c_no_flip_16k_seed44
```
