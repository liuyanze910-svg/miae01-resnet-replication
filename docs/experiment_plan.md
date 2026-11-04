# Week 1 Experimental Plan

## Claim to evaluate

Section 4.2 of He et al. reports that increasing depth improves the accuracy of several residual networks on CIFAR-10. Members A and B will test one comparison from that result. **Does ResNet-32 achieve a lower mean test error rate than ResNet-20 under our shared protocol?** Table 6 is the reference for final test error. The middle panel of Figure 6 shows the training and test error curves. Our conclusion will be limited to these two depths and the settings below. If the difference varies in direction across seeds, report that variation. [He et al., CVPR 2016, Section 4.2, Table 6, and Figure 6](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf#page=7)

| Model | Parameters in the paper (approx.) | Test error in Table 6 | Implied test accuracy |
| --- | ---: | ---: | ---: |
| ResNet-20 | 0.27M | 8.75% | 91.25% |
| ResNet-32 | 0.46M | 7.51% | 92.49% |

Error rate equals 100% minus accuracy. The reported error rate falls by 1.24 percentage points from ResNet-20 to ResNet-32. The five-run statistics in Table 6 refer to ResNet-110. Our project will compute its own means and standard deviations for ResNet-20 and ResNet-32.

## Paper protocol and proposed team settings

| Item | Paper, Section 4.2 | Proposed team setting |
| --- | --- | --- |
| Dataset and partitions | CIFAR-10 has 50,000 official training images and 10,000 test images. The authors used a 45,000/5,000 split to determine the training schedule and describe training on the training set and evaluating on the test set. | With `split_seed=2026`, use 45,000 images for updates and 5,000 for validation. Evaluate the final weights once on the independent 10,000-image test set. A and B still need to confirm the final training-set size and document the difference if the proposed split is retained. |
| Architecture | 32 x 32 inputs, three stages with 16, 32, and 64 channels, Option A shortcuts, and depth `6n + 2`. | Use three residual blocks per stage for ResNet-20 and five for ResNet-32. Downsample spatially with stride 2 and zero-pad the added shortcut channels. |
| Preprocessing | Subtract the per-pixel mean. | Scale pixels to the range 0 to 1 and compute a mean for each channel and spatial position from the training subset. Use those same means for validation and testing. |
| Training augmentation | Pad by four pixels on each side, randomly crop to 32 x 32, and use horizontal flips. | Zero-pad the centered image, crop randomly, then flip with probability 0.5 in the baseline. These are implementation choices. Member C can disable the flip with `--no-flip`. |
| Optimization and budget | Batch size 128 on two GPUs, momentum 0.9, and weight decay 0.0001. Start at 0.1 and divide by 10 after 32,000 and 48,000 updates. Stop at 64,000. | Use the same batch size, optimizer hyperparameters, learning-rate milestones, and update budget for the full run. Use PyTorch SGD on one CPU or one CUDA GPU. |
| Training and evaluation | Batch normalization, He initialization, and no dropout. Evaluate one original-size view per test image. | Use He initialization and PyTorch's batch-normalization defaults as implemented in `model.py`. Evaluate the final weights without random test augmentation. Section 4.2 leaves the checkpoint-selection details for Table 6 unspecified. |
| Week 1 smoke test | Table 6 reports full experiments. | Run eight updates with batch size 32 and evaluate a small validation subset to verify the pipeline. |

## How the team will compare runs

Members A and B will agree on the hardware, training budget, data partitions, and training seeds before full runs. Use the same augmentation policy and evaluation procedure for both depths. Record test error, test accuracy, parameter count, elapsed time, and training and validation curves. For each seed, compute `ResNet-20 test error - ResNet-32 test error`. A positive value means ResNet-32 had lower error for that seed. Report the means, standard deviations, and per-seed differences. Member C can check the shared log format in `metrics.csv` and `summary.json` before running the augmentation comparison.

## What a residual block learns

A shortcut carries the input `x` to the addition, while the convolutional branch learns an adjustment `F(x)`. For example, if the input is 10 and the desired output is 12, the branch can learn to add 2. A real block adds feature maps element by element. When their shapes differ, the Option A shortcut aligns them first.
