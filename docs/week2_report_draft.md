# ResNet Reproduction on CIFAR 10

Member A Week 2 Baseline Draft

## 1 Introduction and Claim

He et al. studied the degradation problem, where adding layers to a plain neural network can raise training error. A residual block learns a correction F(x) and adds it to a shortcut carrying the input. This design gives the block a direct way to preserve the input when little correction is needed [1, Sections 1 and 3].

We test one claim from the CIFAR-10 experiments in Section 4.2 and Table 6 [1]. Under a common training protocol with horizontal flipping enabled, ResNet-32 is expected to have a lower mean test classification error than ResNet-20. Member A runs ResNet-20 as the baseline, and Member B runs ResNet-32 for the depth comparison. Member C uses the same ResNet-20 to test the effect of disabling horizontal flipping. Our scope is limited to these CIFAR-10 models and the reduced training budget described below.

## 2 Reproduction Setup

### Model and starting code

We use an independent PyTorch implementation based on the CIFAR-10 architecture in [1, Section 4.2]. ResNet-20 has three stages with 16, 32, and 64 channels, with three residual blocks per stage. Each block has two 3 × 3 convolutions. Option A shortcuts use subsampling and zero-padding when the shape changes. Global average pooling feeds a ten-class classifier. The seed-42 baseline has 269,722 trainable parameters.

The group repository is liuyanze910-svg/miae01-resnet-replication. Member A started from commit 5242c9337d8558343173534fbc3dd880fd6fb2eb. The reduced schedule was added in configs/reduced_budget.json. The README and Week 2 report and run notes were updated, and the baseline logs were copied into docs/results/week2_a/resnet20-flip-seed42/. The training, model, and data-loading code came from the base commit. The public PyTorch repository [3] was consulted as an architecture reference.

### Data and training

The data script retrieves the official CIFAR-10 binary archive and checks its published MD5 checksum [2]. A fixed split seed of 2026 divides the original training set into 45,000 training images and 5,000 validation images. The separate 10,000-image official test set is evaluated once using the weights at step 16,000. The trainer estimates a per-pixel mean from the 45,000 training images and applies it to all splits. For training, it zero-pads each centered image by four pixels, randomly crops a 32 × 32 image, and flips it horizontally with probability 0.5 in the baseline.

Training starts from He initialization without pretrained weights. We use cross-entropy and SGD with batch size 128, momentum 0.9, weight decay 0.0001, and an initial learning rate of 0.1. The first run uses training seed 42. The proposed matched seeds for the final comparisons are 42, 43, and 44. Member A ran on an Intel Core Ultra 5 336H CPU with two PyTorch threads, Windows 11 build 26200, Python 3.12.14, PyTorch 2.10.0+cpu, and NumPy 2.2.3.

## 3 Reduced Training Budget and Deviations

To fit the compute time available on our local machines, we reduced training from 64,000 to 16,000 optimizer updates, or 25% of the paper's budget. At a batch size of 128, this also reduces the number of training examples processed across batches to one quarter. We moved the two learning-rate drops from 32,000 and 48,000 to 8,000 and 12,000, keeping them at 50% and 75% of training. A, B, and C use the same 16,000-step budget so that the group can compare depth and augmentation under a common schedule. Table 1 records the differences from the paper.

Table 1. Differences between the paper and the group protocol

| Item | Paper [1, Section 4.2] | Group protocol | Reason |
| --- | --- | --- | --- |
| Training budget | 64,000 updates | 16,000 updates per run | Fit the available compute time. |
| Learning-rate drops | After 32,000 and 48,000 updates | After 8,000 and 12,000 updates | Preserve the two positions in the schedule. |
| Train and validation split | 45,000/5,000 for schedule selection. The paper describes training on the official training set for the reported test experiment. | Retain the same 5,000-image validation holdout throughout. Use the other 45,000 images for updates and mean estimation. | Compare validation results on the same images across group runs. |
| Training preprocessing | Per-pixel centering, four-pixel padding, random cropping, and horizontal flipping. | Estimate the mean on the training subset. Zero-pad after centering and use a flip probability of 0.5 for A and B. | Use the same preprocessing across the depth comparison and define the flip ablation precisely. |
| Hardware and implementation | Two GPUs | Member A used one CPU and the group's PyTorch implementation. Record B and C's environments with their runs. | Use available hardware and document the execution environment. |

## 4 Preliminary Results

Table 2 reports the percentage of misclassified images on the official test set, the same metric as the paper. The paper column uses its 64,000-step schedule, and the group columns use our 16,000-step schedule. The seed-42 baseline has 89.77% test accuracy and 10.23% test error on 10,000 images. Final validation accuracy is 90.02% on 5,000 images. Training and evaluation took 70 minutes and 16 seconds.

Table 2. Paper vs Ours on CIFAR 10 test classification error

| Condition | Paper Table 6 | Ours seed 42 | Ours three-seed mean ± SD |
| --- | ---: | ---: | ---: |
| A · ResNet-20 with flipping | 8.75% | 10.23% | Pending |
| B · ResNet-32 with flipping | 7.51% | Pending verification | Pending |

## 5 Gap Analysis and Claim Assessment

For the completed A run, our error is 1.48 percentage points above the paper's ResNet-20 result (10.23% minus 8.75%). This is a 16.91% increase relative to the paper's error rate. The shorter schedule, permanent validation holdout, and implementation differences are documented. Their individual effects on this gap require controlled evidence. For example, a same-seed comparison between the 16,000- and 64,000-step schedules could test the budget change while holding the model, data split, and augmentation fixed.

The current judgment on the depth claim is inconclusive. It requires matched A and B results across at least three seeds. For each seed, calculate ResNet-20 error minus ResNet-32 error. A positive difference favors ResNet-32. Report the paired differences alongside each model's mean and sample standard deviation, and use a numbered figure to show how consistent the direction is across seeds. Conclusions apply to the two depths under the tested protocol.

## 6 Extension Design

Member C tests whether turning off horizontal flipping changes ResNet-20 test error. The ablation changes the flip setting and keeps the architecture, split, random crop, batch size, optimizer, training budget, and evaluation rule fixed. For each matched seed, compare C's test error with A's. A positive difference means the error was higher with flipping disabled. This comparison can show how sensitive the common ResNet-20 baseline is to the augmentation policy. The result and its interpretation are pending the paired runs.

## 7 Reproducibility and Contributions

The seed-42 run is documented in docs/results/week2_a/resnet20-flip-seed42/. The summary gives the final scores, metrics.csv gives the step-16,000 test row, and run_config.json and revision.txt identify the settings and training-code revision. Member A (SuSiying) prepared the baseline setup and run record and drafted the reproduction setup. Add the group's verified B and C contributions and the overall reproduction judgment when their results are integrated.

AI use for this section. ChatGPT assisted with the run configuration, execution, log checks, and report drafting. The reported scores were computed by the training and evaluation program. Update this statement with the other members' actual AI use before submitting the group report.

## References

[1] K. He, X. Zhang, S. Ren, and J. Sun. Deep Residual Learning for Image Recognition. CVPR, 2016. https://arxiv.org/abs/1512.03385

[2] A. Krizhevsky. Learning Multiple Layers of Features from Tiny Images. University of Toronto, 2009. https://cave.cs.toronto.edu/kriz/cifar.html

[3] Y. Idelbayev. akamaster/pytorch_resnet_cifar10. PyTorch implementation reference, BSD 2-Clause. https://github.com/akamaster/pytorch_resnet_cifar10
