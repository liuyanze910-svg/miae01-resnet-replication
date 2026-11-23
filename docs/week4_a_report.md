# ResNet Replication on CIFAR-10: Background and Reproduction Setup

Member A: SuSiying (2260032041)
Week 4, 23-29 November 2026

## 1. Introduction and reproduction scope

Increasing the depth of a neural network can make optimization harder. He et al. distinguish this degradation problem from overfitting: a deeper plain network can have higher training error than a shallower counterpart. Their residual formulation learns a correction F(x) and adds an identity shortcut, producing y = F(x) + x when the dimensions agree. This gives a block a direct way to preserve its input [1, Sections 1 and 3].

Our project reproduces a limited part of the CIFAR-10 experiments in Section 4.2. The principal question is whether ResNet-32 obtains lower test classification error than ResNet-20 under a common protocol. This question is linked to Table 6 and the middle panel of Figure 6 in the paper. Table 6 reports 8.75% error for ResNet-20 and 7.51% for ResNet-32 [1]. These are published reference scores, not three-seed estimates with uncertainty reported for those two models.

The reproduction uses CIFAR-10, an independent PyTorch implementation, and a reduced budget of 16,000 optimizer updates. Member A supplies the ResNet-20 baseline with horizontal flipping. Member B owns the ResNet-32 comparison, the Paper vs. Ours table, main results figures, discrepancy analysis, and claim verdict. Member C owns the ResNet-20 no-flip extension and overall conclusion. This contribution covers the background, scope, setup, and documented deviations. It does not reproduce ImageNet, object detection, networks deeper than 32 layers, or the plain-network experiment needed to directly retest degradation.

## 2. Reproduction setup

### 2.1 Starting code and model

The group repository is [liuyanze910-svg/miae01-resnet-replication](https://github.com/liuyanze910-svg/miae01-resnet-replication). Member A's seed-42 baseline used training-code commit `5242c9337d8558343173534fbc3dd880fd6fb2eb`. Seeds 43 and 44 recorded launch revision `9cea1f51c2782c078ef4c64266bb423c2857873c`. The repository comparison between these revisions contains documentation, configuration, and log changes, with no changes to `train.py`, `model.py`, or `data.py` [4]. The Week 4 evidence review uses snapshot `39c480f39e15bfde3b61f474207acc567f43a8b3`.

The implementation follows the paper's CIFAR-10 architecture. ResNet-20 starts with a 3 x 3 convolution, followed by three stages with 16, 32, and 64 channels. Each stage contains three residual blocks, each with two 3 x 3 convolutions. Strided convolutions reduce the spatial dimensions between stages. Parameter-free Option A shortcuts subsample the input and add zero channels when dimensions change. Global average pooling feeds a ten-class linear classifier. The model has 269,722 trainable parameters. ResNet-32 uses five blocks per stage and has 464,154 parameters.

The ResNet-20 depth count is 1 stem convolution + 3 stages x 3 blocks x 2 convolutions + 1 fully connected layer = 20 weighted layers. Batch normalization and ReLU operations are not included in this naming convention. Starting from a 3 x 32 x 32 input, the stage outputs have shapes 16 x 32 x 32, 32 x 16 x 16, and 64 x 8 x 8 in channel-height-width order. Global average pooling produces a 64-dimensional vector, and the classifier produces ten logits.

In the implemented block, F(x) contains a convolution-BN-ReLU sequence followed by a second convolution and BN. The block output is ReLU(F(x) + S(x)), where S(x) is the identity when dimensions agree. At stage transitions, Option A changes S(x) by strided subsampling and channel zero padding. Thus the abstract residual sum F(x) + x and the complete implemented block should be distinguished [5].

Convolutions use batch normalization and ReLU. Training starts from Kaiming normal initialization without pretrained weights or dropout. The project implements the models independently. Idelbayev's PyTorch CIFAR-10 ResNet repository served as an architecture reference, as documented in the source notes [3, 5]. The source notes state that no upstream source files or weights were copied.

### 2.2 Data and preprocessing

The data script downloads the official CIFAR-10 binary archive and checks MD5 `c32a1d4ab5d03f1284b67883e8d87530` before reading it [2]. A NumPy generator with split seed 2026 permutes the 50,000 training images. The first 5,000 become the validation set and the remaining 45,000 supply training updates. The separate official 10,000-image test set remains outside training and validation.

The loader converts pixel values to floating point, divides by 255, and subtracts a per-channel, per-pixel mean estimated from the 45,000 training images only. It applies that same mean to validation and test images. Training images receive four-pixel zero padding after centering and a random 32 x 32 crop. A and B enable horizontal flipping with probability 0.5. C disables flipping while retaining random cropping. Evaluation uses the original single 32 x 32 view without random augmentation [5].

### 2.3 Optimization and evaluation

All completed comparison runs use training seeds 42, 43, and 44, independently of the fixed split seed. The trainer uses cross-entropy and SGD with batch size 128, momentum 0.9, weight decay 0.0001, and initial learning rate 0.1. The learning rate becomes 0.01 after update 8,000 and 0.001 after update 12,000. Training ends at update 16,000. With `drop_last=True`, every optimizer update processes a full batch, for 2,048,000 image presentations per run.

One optimizer update consists of a forward pass, cross-entropy calculation, gradient backpropagation, and an SGD parameter update on one batch. The precise learning-rate ranges are updates 1-8,000 at 0.1, 8,001-12,000 at 0.01, and 12,001-16,000 at 0.001. The script changes the rate after the milestone update. Image presentations include repeat visits to training images and should not be described as distinct images or epochs.

The trainer records training metrics every 1,000 updates and validation metrics at updates 5,000, 10,000, 15,000, and 16,000. It evaluates the final weights once on all 10,000 test images. The primary metric is `test.error_pct` in `summary.json`, cross-checked against the final test row in `metrics.csv`. The evaluation rule uses the final model rather than selecting a checkpoint by test performance. Report means and sample standard deviations across the three training seeds, with sample SD using denominator n - 1. Error rates use percent, while error differences and their SD use percentage points (pp).

The split seed controls the NumPy permutation used for the training/validation partition. Training seeds control model initialization and training randomness, with a separately seeded DataLoader generator for shuffling. The three final test evaluations use the same 10,000 test images. Consequently, sample SD describes variation across three training seeds on one fixed split. It is not a confidence interval or an estimate of variation across independent test datasets.

### 2.4 Execution environment

Member A ran on an Intel Core Ultra 5 336H CPU with two PyTorch threads per process, Windows 11 build 26200, Python 3.12.14, PyTorch 2.10.0+cpu, and NumPy 2.2.3. The seed-42 run took 4,216.195 seconds. Seeds 43 and 44 ran concurrently on the same CPU and took 7,613.904 and 7,629.524 seconds respectively [6]. These elapsed times are observations under different concurrent workloads, so they do not form a controlled speed comparison.

B and C's archived configurations record macOS on arm64 and CPU execution, PyTorch 2.10.0, and NumPy 2.2.3. B records Python 3.12.16, while C records Python 3.12.14 [7]. Their environments therefore differ from A's Windows environment even though the declared experimental settings match.

## 3. Deviations from the paper

Table 1 records the setup deviations for this contribution. It distinguishes observed differences from details that cannot be established from the paper alone.

Table 1. Original settings, implemented settings, and reasons for differences

| Item | Paper setting [1, Section 4.2] | Implemented setting | Reason or qualification |
| --- | --- | --- | --- |
| Training budget | 64,000 optimizer updates | 16,000 updates for A, B, and C | Fit available compute time. At batch size 128, image presentations fall from 8,192,000 to 2,048,000, or 25% of the original budget. |
| LR schedule | Initial 0.1, divided by 10 at 32,000 and 48,000 updates | Initial 0.1, divided by 10 after 8,000 and 12,000 updates | Preserve the relative schedule positions of 50% and 75%. This compresses the entire schedule and changes both budget and decay timing. |
| Train/val split | Describes experiments on the 50,000-image training set and a 45,000/5,000 split for determining the schedule | Keep a permanent 45,000/5,000 training/validation split with split seed 2026 | Retain a common validation set across group runs. The paper provides no per-run split manifest, so its final fitting procedure cannot be reconstructed exactly from these statements alone. |
| Preprocessing | Per-pixel mean subtraction, four-pixel padding, random crop, and horizontal flip | Mean from the 45,000 training images, division by 255, then centering and zero padding | Make preprocessing explicit and avoid using validation images for mean estimation. The paper does not fully specify all ordering and subset details, so this is a potential implementation difference. |
| No-flip extension | Table 6 uses data augmentation including horizontal flipping | A/B use flip probability 0.5. C disables flipping | C's intentional extension tests sensitivity to this augmentation. There is no directly corresponding no-flip score in Table 6. |
| Execution | Batch size 128 on two GPUs | Independent PyTorch implementation on CPUs. A uses Windows, B/C use macOS | Use available machines. Kernel arithmetic and implementation details can differ. Their effects on error are not measured here. |
| Implementation | Option A shortcuts, initialization and batch normalization described at method level | Kaiming normal initialization, PyTorch BN defaults, end-channel zero padding, and recorded training seeds | Record concrete choices for reproducibility. The paper does not give matching seed-level execution traces, and exact implementation equivalence is not established. |

The reduced schedule is an observed protocol difference, not evidence that fewer updates caused the entire error gap. Its separate contribution cannot be quantified without a controlled budget comparison. Keeping schedule positions fixed also does not make a 16,000-update run equivalent to the paper's 64,000-update run. This contribution introduces no new full training run.

Matching seed labels supports organized seed-level comparisons but does not guarantee identical random operations across conditions. Different model depths consume different initialization draws. Disabling flipping changes the augmentation random-number consumption in `data.py`. Platform differences add another limitation. These constraints should accompany B and C's interpretation of their comparisons.

## 4. Traceability and Member A contribution

Member A completed the eight-update real-data smoke test in Week 1, seed 42 in Week 2, and seeds 43 and 44 in Week 3 [6]. The three baseline test errors are 10.23%, 10.58%, and 10.36%, giving a mean of 10.39% and a sample SD of 0.18 pp. These values are supplied to B and C as baseline inputs. Their main comparison tables, figures, and conclusions remain in the respective members' contributions.

Each baseline archive contains `run_config.json`, `metrics.csv`, `summary.json`, and `revision.txt`. The Week 4 review checked completion status, 16,000 updates, fixed split and optimization settings, 16 training records, four validation evaluations, and one final test evaluation. Final validation/test rows agree with their summaries. The 12 corresponding files in the local Week 3 A update folder also agree with the repository after parsing JSON/CSV and normalizing text line endings. These checks establish archive consistency, not independent re-evaluation of model predictions or a new dataset checksum check.

The current trainer exports logs but does not save model weights or an optimizer checkpoint. The archive therefore supports review of the recipe and recorded metrics, but cannot directly reproduce the predictions of the original trained model. Independent re-evaluation would require the original weights or a new training run. No such run was performed for this Week 4 update.

SuSiying (2260032041) prepared the baseline setup and logs in earlier weeks and contributes the Week 4 introduction, scope, methods, deviation table, background/methods slides, and evidence review. Member B's depth experiments and Member C's extension are credited to those members. This document is Member A's section draft for the group's later report assembly.

AI usage statement for Member A: ChatGPT assisted with earlier configuration and report drafting, as recorded in the existing baseline draft. In Week 4, Codex assisted with reading the paper and logs, checking archive consistency, and drafting the methods text and slides. ImageGen recreated decorative slide backgrounds from the supplied template previews. No scientific evidence was generated as artwork, and no new model training was performed. The archived training program produced the reported experimental scores. Each member should provide their own AI usage statement for the combined report.

## References

[1] K. He, X. Zhang, S. Ren, and J. Sun. Deep Residual Learning for Image Recognition. CVPR, 2016. Section 4.2, Figure 6, and Table 6. https://arxiv.org/abs/1512.03385

[2] A. Krizhevsky. Learning Multiple Layers of Features from Tiny Images. University of Toronto, 2009. Dataset: https://cave.cs.toronto.edu/kriz/cifar.html

[3] Y. Idelbayev. PyTorch CIFAR-10 ResNet implementation, BSD 2-Clause architecture reference. https://github.com/akamaster/pytorch_resnet_cifar10

[4] [Training-code revision comparison](https://github.com/liuyanze910-svg/miae01-resnet-replication/compare/5242c9337d8558343173534fbc3dd880fd6fb2eb...9cea1f51c2782c078ef4c64266bb423c2857873c).

[5] [Source and license notes](sources.md), [model](../model.py), [data loader](../data.py), [trainer](../train.py), and [shared configuration](../configs/reduced_budget.json), reviewed at snapshot `39c480f39e15bfde3b61f474207acc567f43a8b3`.

[6] [Week 1 record](week1_status.md), [Week 2 A record](week2_status.md), [Week 3 A record](week3_status.md), and baseline archives: [seed 42](results/week2/resnet20-flip-seed42/), [seed 43](results/week3/resnet20-flip-seed43/), [seed 44](results/week3/resnet20-flip-seed44/).

[7] [Member B run record](week3_b_status.md) and [Member C run record](week3_c_status.md), with their linked original logs. These are evidence sources owned by the respective members.
