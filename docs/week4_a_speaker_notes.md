# Week 4: Presentation Speaker Notes

Eight slides covering the paper background, CIFAR-10 baseline and interpretation.

## Slide 1. ResNet on CIFAR-10

English speaker script
This presentation covers the ResNet-20 baseline on CIFAR-10, including the architecture, training and evaluation protocol, deviations from the paper, and archived results.
Sources
https://arxiv.org/abs/1512.03385
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/week3_status.md

## Slide 2. The paper at a glance

Speaker script
He, Zhang, Ren and Sun presented this paper at CVPR 2016. They observed that increasing the depth of a plain network can lead to higher training error, a phenomenon called degradation. They proposed residual learning to carry information across layers. Next, the diagram shows how the input travels through two paths.
Source
https://arxiv.org/abs/1512.03385 (Section 1)

## Slide 3. Residual block: two paths for the input

Speaker script
Input x follows two paths. The convolutional branch F(x) learns a correction and the shortcut S(x) carries the input. The two are added elementwise and passed through ReLU, yielding ReLU(F(x)+S(x)). When shapes match, S(x)=x. At a stage transition, Option A subsamples the shortcut and pads channels with zeros. Next, we use these blocks to construct ResNet-20.
Sources
https://arxiv.org/abs/1512.03385 (Section 3, Figure 2)
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py

## Slide 4. CIFAR-10 ResNet-20

English speaker script
The input has three color channels and a spatial size of 32 by 32. An initial convolution produces 16 channels. We then use three stages, with three residual blocks per stage. Every block contains two convolutions. The first block in stages two and three reduces the spatial resolution and increases the channel count. Global average pooling reduces the final 64-channel feature map to a vector, and the classifier produces ten logits. The layer count is one initial convolution, plus three times three times two block convolutions, plus one fully connected layer: twenty weighted layers. Batch-normalization and activation operations are not included in that count. The archived model has 269,722 trainable parameters.
Sources
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/model.py
https://github.com/liuyanze910-svg/miae01-resnet-replication/blob/39c480f39e15bfde3b61f474207acc567f43a8b3/docs/results/week2/resnet20-flip-seed42/run_config.json
https://arxiv.org/abs/1512.03385 (Section 4.2)

## Slide 5. CIFAR-10 data and preprocessing

Speaker script
CIFAR-10 consists of 32 by 32 color images in ten classes. Split seed 2026 partitions the original training set into 45,000 training images and 5,000 validation images. The 10,000 official test images are used for final evaluation. Training uses four-pixel zero padding, a random crop and a horizontal flip with probability 0.5. Pixel values are divided by 255 and the training-only per-pixel mean is subtracted. Validation and testing use no random augmentation.
Sources
https://github.com/liuyanze910-svg/miae01-resnet-replication/tree/main
https://arxiv.org/abs/1512.03385 (Section 4.2)

## Slide 6. Optimization and learning rate

Speaker script
The model uses cross-entropy, SGD with batch size 128, momentum 0.9 and weight decay 0.0001. The learning rate starts at 0.1 and drops to 0.01 after 8k updates and 0.001 after 12k. The project uses 16k updates; the paper uses 64k with drops at 32k and 48k. This difference limits direct comparison. We use Kaiming initialization without pretrained weights or dropout.
Sources
https://arxiv.org/abs/1512.03385 (Section 4.2)
https://github.com/liuyanze910-svg/miae01-resnet-replication/tree/main

## Slide 7. Baseline results

Speaker script
The test errors for seeds 42, 43 and 44 are 10.23%, 10.58% and 10.36%. Their arithmetic mean is 10.39%, with a sample standard deviation of 0.18 percentage points; this is not a confidence interval. Each final model was evaluated on the same 10,000 test images.
Sources
https://github.com/liuyanze910-svg/miae01-resnet-replication/tree/main/docs/results/week2/resnet20-flip-seed42
https://github.com/liuyanze910-svg/miae01-resnet-replication/tree/main/docs/results/week3/resnet20-flip-seed43
https://github.com/liuyanze910-svg/miae01-resnet-replication/tree/main/docs/results/week3/resnet20-flip-seed44

## Slide 8. Paper comparison and limitations

Speaker script
Table 6 of the paper reports 8.75% CIFAR-10 test error for ResNet-20. Our three-seed mean is 10.39%, higher by 1.64 percentage points. The paper value should not be presented as our three-seed mean. The protocols differ, particularly in update count and the training/validation split, so this comparison does not isolate a cause of the gap. Configuration, training logs and summaries are archived, but the original model weights were not saved, preventing reevaluation of those models.
Sources
https://arxiv.org/abs/1512.03385 (Table 6, Section 4.2)
https://github.com/liuyanze910-svg/miae01-resnet-replication/tree/main/docs/results/week2/resnet20-flip-seed42
https://github.com/liuyanze910-svg/miae01-resnet-replication/tree/main/docs/results/week3/resnet20-flip-seed43
https://github.com/liuyanze910-svg/miae01-resnet-replication/tree/main/docs/results/week3/resnet20-flip-seed44
