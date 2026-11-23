# Week 4 Member A: Detailed Speaker Notes

SuSiying (2260032041). English presentation script.

## Slide 1. ResNet on CIFAR-10

### English speaker script

Our project reproduces a focused part of Deep Residual Learning for Image Recognition by He and colleagues. I am responsible for the ResNet-20 baseline and the common reproduction setup. I will explain the motivation, architecture, dataset, training procedure, evaluation rule, and deviations from the original protocol. All three baseline runs were completed before Week 4. The numbers shown later come from the archived training logs. Member B presents the depth-comparison results, and Member C presents the no-flip extension and the overall conclusion.


Sources:

- https://arxiv.org/abs/1512.03385
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md

## Slide 2. Residual learning

### English speaker script

The paper discusses degradation: increasing the depth of a plain network can increase training error, even though the deeper model has more capacity. This is an optimization issue rather than simply a gap between training and test performance. Residual learning represents a transformation as a correction F of x added to a shortcut S of x. When the shape is unchanged, S of x is the input itself. In our implementation, a ReLU follows the addition. When the shape changes, Option A subsamples the shortcut and pads its channels with zeros. Our experiment uses residual networks at two depths, so it does not directly retest degradation against a plain network.


Sources:

- https://arxiv.org/abs/1512.03385 (Sections 1 and 3, Figure 2)
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py

## Slide 3. Scope of the reproduction

### English speaker script

The principal question is whether ResNet-32 obtains a lower test error than ResNet-20 under the same declared protocol. This is linked to Table 6 and the middle panel of Figure 6 in the paper. We focus on CIFAR-10 and use an independent PyTorch implementation with a reduced budget. Member A supplies the ResNet-20 baseline with horizontal flipping. Member B owns the depth comparison, Paper versus Ours table, main figures, and discrepancy analysis. Member C owns the no-flip extension and overall conclusion. Our evidence covers two residual-network depths on one dataset and one fixed split. It does not establish a general result about every deeper network.


Sources:

- https://arxiv.org/abs/1512.03385 (Section 4.2, Figure 6, Table 6)
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/experiment_plan.md
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md

## Slide 4. CIFAR-10 ResNet-20

### English speaker script

The input has three color channels and a spatial size of 32 by 32. An initial convolution produces 16 channels. We then use three stages, with three residual blocks per stage. Every block contains two convolutions. The first block in stages two and three reduces the spatial resolution and increases the channel count. Global average pooling reduces the final 64-channel feature map to a vector, and the classifier produces ten logits. The layer count is one initial convolution, plus three times three times two block convolutions, plus one fully connected layer: twenty weighted layers. Batch-normalization and activation operations are not included in that count. The archived model has 269,722 trainable parameters.


Sources:

- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week2/resnet20-flip-seed42/run_config.json
- https://arxiv.org/abs/1512.03385 (Section 4.2)

## Slide 5. Data and preprocessing

### English speaker script

CIFAR-10 provides 50,000 training images and a separate set of 10,000 test images. We use split seed 2026 to reserve 5,000 training images for validation and retain 45,000 for updates. The loader divides pixel values by 255 and subtracts a per-channel, per-pixel mean estimated from the training subset only. It does not divide by a standard deviation. Training then applies four-pixel zero padding after centering, a random 32 by 32 crop, and horizontal flipping with probability one half. Validation and test use a single view without random augmentation. The download script verifies the archive against the published MD5 before reading it. In this Week 4 review, we inspected the code and existing logs rather than downloading or verifying the dataset again.


Sources:

- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/data.py
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/configs/reduced_budget.json
- https://cave.cs.toronto.edu/kriz/cifar.html

## Slide 6. Optimization and learning rate

### English speaker script

Training starts from Kaiming normal initialization without pretrained weights. We optimize cross-entropy with SGD, using batch size 128, momentum 0.9, and weight decay 0.0001. Updates one through eight thousand use learning rate 0.1. Updates eight thousand and one through twelve thousand use 0.01. The final four thousand updates use 0.001. The trainer changes the rate after completing the milestone update. Every update uses a full batch, so one run processes 16,000 times 128, or 2,048,000 image presentations. These include repeated presentations of the same training images. This is a quarter of the paper's update budget. Keeping the relative decay positions does not make the shorter schedule equivalent to the original one.


Sources:

- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/train.py
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/configs/reduced_budget.json
- https://arxiv.org/abs/1512.03385 (Section 4.2)

## Slide 7. Evaluation and seed statistics

### English speaker script

We separate the data-split seed from the training seed. Split seed 2026 fixes the partition. Training seeds 42, 43, and 44 control initialization and training randomness. Each run records validation metrics at updates 5,000, 10,000, 15,000, and 16,000. The final model is evaluated once on the same 10,000 test images. We do not choose a checkpoint by test performance. The primary metric is the percentage of misclassified test images. We report the mean and sample standard deviation across three training seeds, using n minus one in the variance denominator. This standard deviation describes variation across those training runs on one fixed split. It is not a confidence interval or an estimate across independent datasets.


Sources:

- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/train.py
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/data.py
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week2/resnet20-flip-seed42/metrics.csv
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md

## Slide 8. Protocol deviations and limits

### English speaker script

The main documented difference is our compressed schedule. The paper uses 64,000 updates, with learning-rate drops at 32,000 and 48,000. We use 16,000 updates, with drops after 8,000 and 12,000. We also retain a permanent validation holdout, whereas the paper describes a training-set experiment and a 45,000 by 5,000 split for selecting its schedule. Preprocessing order and implementation details are explicit in our code but are not fully specified by the paper. A ran on Windows CPU, while B and C ran on macOS CPU. These differences limit exact comparability. No controlled budget rerun was performed, so we cannot attribute the entire paper-to-project error gap to training length. The complete deviation table is in the report body.


Sources:

- https://arxiv.org/abs/1512.03385 (Section 4.2)
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/configs/reduced_budget.json
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_b_status.md
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_c_status.md

## Slide 9. Member A baseline evidence

### English speaker script

The baseline test errors are 10.23 percent for seed 42, 10.58 percent for seed 43, and 10.36 percent for seed 44. Each result uses 10,000 test images. Their mean error is 10.39 percent, and their sample standard deviation is approximately 0.1769 percentage points, reported as 0.18. The corresponding accuracies are 89.77, 89.42, and 89.64 percent. These are the completed Member A baseline inputs for the other comparisons. We checked that the final test rows in metrics CSV agree with summary JSON. These checks establish consistency of the archived results. They do not independently establish the predictions of a loaded model, because the current trainer does not save the trained weights.


Sources:

- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week2/resnet20-flip-seed42/summary.json
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed43/summary.json
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed44/summary.json
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md

## Slide 10. Traceability and handoff

### English speaker script

Every baseline run has four evidence files. Run configuration records the seeds, environment, and settings. Metrics CSV records training, validation, and the final test evaluation. Summary JSON provides completion status and the final scores. Revision text identifies the training-code revision and launch command. A used Python 3.12.14, PyTorch 2.10.0 plus CPU, NumPy 2.2.3, and two CPU threads per process. The baseline code revisions are recorded in the report and notes. The archive supports review of the recipe and logged results, but it does not contain saved model weights. Members B and C can use these baseline inputs for their own sections. Codex assisted with drafting and log checks, and ImageGen recreated the decorative template backgrounds. No new training was performed for this update.


Sources:

- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week2/resnet20-flip-seed42/revision.txt
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed43/revision.txt
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed44/revision.txt
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed43/run_config.json
- https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/train.py

## Preparation questions

- Why is this model called ResNet-20? Count the 1 stem convolution, 18 block convolutions, and 1 classifier. BN and ReLU are not weighted layers in this naming convention.
- What does 0.18 pp mean? It is the sample SD of three seed-level test errors on one fixed split, not a confidence interval.
- Why does our error differ from the paper? The protocol differs in budget, schedule, split, and implementation. Their separate effects have not been isolated by controlled runs.
- Can the archived logs reproduce the predictions directly? No. They support consistency checks, but the trainer did not save model weights. Re-evaluation would require the weights or a new training run.
- Did A verify degradation itself? No plain-network control was run. A supplies a residual-network baseline for the team depth comparison.
