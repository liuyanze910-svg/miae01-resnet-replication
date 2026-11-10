# Week 2 Run Record — Member A

Member A supplies the ResNet-20 baseline with horizontal flipping enabled at probability 0.5. Member B uses it to compare depths, and Member C uses it to compare horizontal flipping. Match the data split, training seed, update budget, and final evaluation rule across conditions. Use `configs/reduced_budget.json`, added to the training code from commit `5242c93`.

## First baseline run

| Item | Setting |
| --- | --- |
| Model and seeds | ResNet-20, training seed `42`, split seed `2026` |
| Schedule | 16,000 updates at batch size 128. Learning rate `0.1` through update 8,000, `0.01` through update 12,000, and `0.001` through update 16,000. |
| Dataset | 45,000 training, 5,000 validation, and 10,000 independent test images |
| Primary metric | `test.error_pct` in `summary.json`, evaluated on the model at update 16,000 |
| Run folder | `runs/week2-a-resnet20-seed42-16k/` |
| Run status | Completed on 2026-11-09 at 18:48 (UTC+08:00) after about 70 minutes and 16 seconds |
| Final validation accuracy | 90.02% on 5,000 images |
| Final test accuracy | 89.77% on 10,000 images |
| Final test error | **10.23%** on 10,000 images |

The first run started on 2026-11-09 at 17:38 (UTC+08:00) using an Intel Core Ultra 5 336H CPU and two PyTorch threads. The exported configuration records Windows 11 build 26200, Python 3.12.14, PyTorch 2.10.0+cpu, NumPy 2.2.3, and 269,722 trainable parameters. The run's revision record identifies the base training-code commit and the SHA-256 of the exact configuration used.

Run from the repository root. The command assumes the official CIFAR-10 binary archive is in `data/`. For a cached archive, add `--data-dir` with the path to its containing folder. Choose a new output directory for a rerun.

```powershell
git rev-parse HEAD
python -B -u train.py --config configs/reduced_budget.json --depth 20 --seed 42 --device cpu --output runs/week2-a-resnet20-seed42-16k
```

## Completion and handoff

1. Check that `run_config.json` records depth 20, seed 42, split seed 2026, flipping enabled, 16,000 updates, and learning-rate milestones 8,000 and 12,000. Record the training-code revision, configuration, actual hardware, and software versions.
2. Check that `summary.json` reports `status` as `completed` and `steps` as `16000`. Verify that `metrics.csv` has one final `test` row for 10,000 images and that its `error_pct` matches `summary.json`.
3. Retain `run_config.json`, `metrics.csv`, and `summary.json` together with the revision record. Give Members B and C the seed 42 test error and logs for their matched comparisons. Member B leads the Week 2 GitHub check-in.

The seed-42 results passed these checks. The portable copies are in [the baseline results directory](results/week2/resnet20-flip-seed42/).

The earlier 64,000-update pilot used `configs/paper_budget.json`. Its logs belong to the separate paper-budget run. For Week 3, run the remaining two team-confirmed seeds, then compute the mean and sample standard deviation of the three 16,000-update test errors in Excel.
