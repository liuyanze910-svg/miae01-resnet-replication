# Week 4 Results Integration - Member B

Member B integrated the completed three-seed ResNet-20 and ResNet-32 runs into a matched depth analysis. The analysis uses the final test error from each archived `summary.json`; it does not rerun training or alter the raw experiment records.

## Matched depth comparison

| Seed | ResNet-20 flip error (%) | ResNet-32 flip error (%) | ResNet-20 minus ResNet-32 (pp) |
| ---: | ---: | ---: | ---: |
| 42 | 10.23 | 9.78 | +0.45 |
| 43 | 10.58 | 9.95 | +0.63 |
| 44 | 10.36 | 10.14 | +0.22 |
| **Mean +/- sample SD** | **10.39 +/- 0.18** | **9.96 +/- 0.18** | **+0.43 +/- 0.21** |

ResNet-32 has lower test error for all three matched seeds. Under the shared reduced-budget protocol, this supports the paper's depth claim in direction. The paper's reported improvement is 1.24 percentage points (8.75% to 7.51%), whereas this reproduction observes 0.43 percentage points. The absolute paper values are therefore not exactly reproduced.

The group protocol uses 16,000 updates rather than the paper's 64,000, retains a 5,000-image validation holdout, and uses the documented PyTorch implementation and available CPU hardware. These differences are plausible sources of the larger error rates, but this project does not claim that the reduced schedule alone explains the full gap without a controlled 64,000-update check.

## Reproducible outputs

- [Analysis script](../scripts/analyze_depth_comparison.py) validates all six flip-condition runs and regenerates the derived files.
- [Matched per-seed CSV](results/week4/depth_comparison.csv) records the paired differences.
- [Summary JSON](results/week4/depth_comparison_summary.json) records means, sample standard deviations, and paper gaps.
- [Depth comparison figure](results/week4/depth_comparison.svg) shows the seed-level test errors.

Run the analysis from the repository root with:

```bash
python scripts/analyze_depth_comparison.py
```

The script fails if a run is incomplete, has the wrong depth or seed, uses a different update count, or lacks the full 10,000-image test evaluation.

## Contribution

Member B (Liu Yanze, 2260031728) completed the ResNet-32 seeds, calculated the matched depth differences, added the reproducible aggregation script and figure, and integrated the depth conclusion into the report draft and README.
