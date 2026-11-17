# Week 3 Baseline Results

Member A, SuSiying (2260032041), completed the remaining ResNet-20 baseline runs on 17 November 2026. Each run used 16,000 updates with horizontal flipping enabled at probability 0.5. Together with the Week 2 seed-42 run, this completes the three baseline seeds for the depth and augmentation comparisons.

## Final results

| Seed | Test error (%) | Test accuracy (%) | Validation accuracy (%) | Elapsed seconds | Archived logs |
| --- | ---: | ---: | ---: | ---: | --- |
| 42 | 10.23 | 89.77 | 90.02 | 4216.195 | [Week 2 seed 42](results/week2/resnet20-flip-seed42/) |
| 43 | 10.58 | 89.42 | 90.08 | 7613.904 | [Week 3 seed 43](results/week3/resnet20-flip-seed43/) |
| 44 | 10.36 | 89.64 | 89.74 | 7629.524 | [Week 3 seed 44](results/week3/resnet20-flip-seed44/) |

The three test errors have a mean of **10.39%** and a sample standard deviation of **0.18 percentage points**, with n = 3. The full-precision standard deviation is 0.1769180601 percentage points. The [Excel workbook](results/week3/baseline_results.xlsx) uses `AVERAGE(B11:B13)` and `STDEV(B11:B13)` on the Baseline sheet. It also includes a chart and all 63 training, validation, and test metric rows.

The mean error exceeds the paper's ResNet-20 reference of 8.75% by 1.64 percentage points, or 18.74% relative to the paper's error. The paper trained for 64,000 steps. The group protocol uses one quarter of that update budget, as described in the [report draft](week2_report_draft.md).

## Run configuration and verification

Both new runs use [the shared reduced-budget configuration](../configs/reduced_budget.json), split seed 2026, and the same training code as seed 42. The 45,000-image training subset, 5,000-image validation subset, and independent 10,000-image test set are fixed across all three runs. The SGD settings, batch size 128, preprocessing, and learning-rate drops after steps 8,000 and 12,000 match the Week 2 baseline.

The run revision records identify commit `9cea1f51c2782c078ef4c64266bb423c2857873c` at launch. Its trainer, model, and data loader match the seed-42 code from `5242c9337d8558343173534fbc3dd880fd6fb2eb`. The dataset archive passed its official MD5 check before training. Each run reports `status` as `completed`, contains all 16 training intervals and four validation evaluations, and has exactly one final test evaluation on 10,000 images. The final test and validation rows agree with the summaries.

The two new seeds ran concurrently on the same Intel Core Ultra 5 336H CPU, using two PyTorch threads per process. The environment was Windows 11 build 26200, Python 3.12.14, PyTorch 2.10.0+cpu, and NumPy 2.2.3. Their elapsed times include the effects of the simultaneous workload. The seed-42 runtime came from its earlier individual run.

## Reproduction commands and handoff

Run these commands from the repository root in the configured environment, with the official binary archive in `data/`. Choose a new output directory for a rerun. A cached archive in another folder can be selected with `--data-dir`.

```powershell
python -B -u train.py --config configs/reduced_budget.json --depth 20 --seed 43 --device cpu --output runs/week3-a-resnet20-seed43-16k
python -B -u train.py --config configs/reduced_budget.json --depth 20 --seed 44 --device cpu --output runs/week3-a-resnet20-seed44-16k
```

Give Members B and C the three per-seed errors and archived logs above. Match seeds 42, 43, and 44 when comparing ResNet-32 with this baseline or comparing the no-flip condition with this baseline. The group-level depth and augmentation conclusions depend on those matched comparison runs.
