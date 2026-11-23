# Week 4: Presentation Speaker Notes

Sixteen slides on the paper background and the CIFAR-10 baseline.

## Slide 1. ResNet on CIFAR-10

English speaker script
This presentation covers the ResNet-20 baseline on CIFAR-10, including the architecture, training and evaluation protocol, deviations from the paper, and archived results.
Sources
https://arxiv.org/abs/1512.03385
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.

## Slide 2. The paper at a glance

He, Zhang, Ren, and Sun presented residual learning at CVPR 2016. They studied degradation, where a deeper plain network can have higher training error. A shortcut carries information across layers and is added to a learned residual. The paper reports ImageNet and CIFAR-10 experiments. Our reproduction focuses on a CIFAR-10 ResNet-20 baseline and does not directly retest degradation in plain networks.
Source: https://arxiv.org/abs/1512.03385 (Sections 1 and 4.2)

## Slide 3. Residual learning

English speaker script
The paper discusses degradation: increasing the depth of a plain network can increase training error, even though the deeper model has more capacity. This is an optimization issue rather than simply a gap between training and test performance. Residual learning represents a transformation as a correction F of x added to a shortcut S of x. When the shape is unchanged, S of x is the input itself. In our implementation, a ReLU follows the addition. When the shape changes, Option A subsamples the shortcut and pads its channels with zeros. Our experiment uses residual networks at two depths, so it does not directly retest degradation against a plain network.
Group members: SuSiying 2260032041 / Liu Yanze 2260031728 / Liang Linlin 2260032082
Sources
https://arxiv.org/abs/1512.03385 (Sections 1 and 3, Figure 2)
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.

## Slide 4. Shortcut connection: two paths

The input follows two paths. The convolutional branch learns a correction F(x); the shortcut carries S(x). Their outputs are added elementwise and passed through ReLU. When dimensions match, S(x) equals x. At stage transitions, Option A subsamples the shortcut and pads channels with zeros. The diagram is schematic; model.py defines the exact operations.
Sources: https://arxiv.org/abs/1512.03385 (Section 3, Figure 2)
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py

## Slide 5. Reproduction scope

English speaker script
We reproduce the CIFAR-10 ResNet-20 baseline using an independent PyTorch implementation, a fixed data split, and a reduced training budget. The primary metric is test classification error, as in the paper’s Section 4.2 and Table 6.
Sources
https://arxiv.org/abs/1512.03385 (Section 4.2, Figure 6, Table 6)
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/experiment_plan.md
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.

## Slide 6. CIFAR-10 basics

CIFAR-10 is an image-classification dataset. Each 32 x 32 color image belongs to one of ten categories, including airplane, automobile, cat, and dog. The official dataset has 50,000 training images and 10,000 separate test images. Our protocol holds out 5,000 training images for validation and uses 45,000 for updates.
Source: https://cave.cs.toronto.edu/kriz/cifar.html

## Slide 7. CIFAR-10 ResNet-20

English speaker script
The input has three color channels and a spatial size of 32 by 32. An initial convolution produces 16 channels. We then use three stages, with three residual blocks per stage. Every block contains two convolutions. The first block in stages two and three reduces the spatial resolution and increases the channel count. Global average pooling reduces the final 64-channel feature map to a vector, and the classifier produces ten logits. The layer count is one initial convolution, plus three times three times two block convolutions, plus one fully connected layer: twenty weighted layers. Batch-normalization and activation operations are not included in that count. The archived model has 269,722 trainable parameters.
Group members: SuSiying 2260032041 / Liu Yanze 2260031728 / Liang Linlin 2260032082
Sources
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week2/resnet20-flip-seed42/run_config.json
https://arxiv.org/abs/1512.03385 (Section 4.2)
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.

## Slide 8. Residual block and shortcut

Source: https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py

## Slide 9. Data and preprocessing

English speaker script
CIFAR-10 provides 50,000 training images and a separate set of 10,000 test images. We use split seed 2026 to reserve 5,000 training images for validation and retain 45,000 for updates. The loader divides pixel values by 255 and subtracts a per-channel, per-pixel mean estimated from the training subset only. It does not divide by a standard deviation. Training then applies four-pixel zero padding after centering, a random 32 by 32 crop, and horizontal flipping with probability one half. Validation and test use a single view without random augmentation. The download script verifies the archive against the published MD5 before reading it. In this Week 4 review, we inspected the code and existing logs rather than downloading or verifying the dataset again.
Group members: SuSiying 2260032041 / Liu Yanze 2260031728 / Liang Linlin 2260032082
Sources
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/data.py
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/configs/reduced_budget.json
https://cave.cs.toronto.edu/kriz/cifar.html
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.

## Slide 10. Training image augmentation

Source: https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/data.py

## Slide 11. Optimization and learning rate

English speaker script
Training starts from Kaiming normal initialization without pretrained weights. We optimize cross-entropy with SGD, using batch size 128, momentum 0.9, and weight decay 0.0001. Updates one through eight thousand use learning rate 0.1. Updates eight thousand and one through twelve thousand use 0.01. The final four thousand updates use 0.001. The trainer changes the rate after completing the milestone update. Every update uses a full batch, so one run processes 16,000 times 128, or 2,048,000 image presentations. These include repeated presentations of the same training images. This is a quarter of the paper's update budget. Keeping the relative decay positions does not make the shorter schedule equivalent to the original one.
Group members: SuSiying 2260032041 / Liu Yanze 2260031728 / Liang Linlin 2260032082
Sources
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/train.py
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/configs/reduced_budget.json
https://arxiv.org/abs/1512.03385 (Section 4.2)
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.

## Slide 12. Evaluation and seed statistics

English speaker script
We separate the data-split seed from the training seed. Split seed 2026 fixes the partition. Training seeds 42, 43, and 44 control initialization and training randomness. Each run records validation metrics at updates 5,000, 10,000, 15,000, and 16,000. The final model is evaluated once on the same 10,000 test images. We do not choose a checkpoint by test performance. The primary metric is the percentage of misclassified test images. We report the mean and sample standard deviation across three training seeds, using n minus one in the variance denominator. This standard deviation describes variation across those training runs on one fixed split. It is not a confidence interval or an estimate across independent datasets.
Group members: SuSiying 2260032041 / Liu Yanze 2260031728 / Liang Linlin 2260032082
Sources
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/train.py
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/data.py
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week2/resnet20-flip-seed42/metrics.csv
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.

## Slide 13. Protocol deviations and limits

English speaker script
The paper uses 64,000 updates and learning-rate drops at 32,000 and 48,000. Our baseline uses 16,000 updates and drops after 8,000 and 12,000. A permanent validation holdout and explicit preprocessing also affect comparability. No controlled budget rerun was performed, so the complete error gap cannot be attributed to training duration.
Sources
https://arxiv.org/abs/1512.03385 (Section 4.2)
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/configs/reduced_budget.json
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_b_status.md
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_c_status.md
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.

## Slide 14. Baseline results

English speaker script
The three test errors are 10.23, 10.58, and 10.36 percent. Their mean is 10.39 percent and the sample standard deviation is 0.18 percentage points. Final test rows agree with the archived summaries. No saved weights are available for independent re-evaluation.
Sources
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week2/resnet20-flip-seed42/summary.json
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed43/summary.json
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed44/summary.json
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.

## Slide 15. Baseline statistics

Source: https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md

## Slide 16. Traceability and limits

English speaker script
Each baseline run records its configuration, metrics, summary and revision. The training program did not save model weights. Re-evaluating the original model requires those weights or a new training run.
Sources
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week2/resnet20-flip-seed42/revision.txt
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed43/revision.txt
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed44/revision.txt
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week3/resnet20-flip-seed43/run_config.json
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/train.py
Cover membership layout reference: user-supplied Mure(4).pptx. ResNet content and Art template retained. No MURE research content incorporated.
