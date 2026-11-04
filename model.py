"""CIFAR-10 residual network from He et al. (CVPR 2016), Section 4.2."""

import torch.nn.functional as F
from torch import nn


def conv3(in_channels, out_channels, stride=1):
    return nn.Conv2d(in_channels, out_channels, 3, stride, padding=1, bias=False)


class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride):
        super().__init__()
        self.conv1 = conv3(in_channels, out_channels, stride)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = conv3(out_channels, out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.stride = stride
        self.extra_channels = out_channels - in_channels

    def forward(self, x):
        residual = self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x)))))
        shortcut = x[:, :, ::self.stride, ::self.stride]
        if self.extra_channels:
            # Option A has no trainable projection. Pad only the channel dimension.
            shortcut = F.pad(shortcut, (0, 0, 0, 0, 0, self.extra_channels))
        return F.relu(residual + shortcut)


class CifarResNet(nn.Module):
    def __init__(self, depth):
        super().__init__()
        blocks_per_stage = {20: 3, 32: 5}[depth]
        layers = [conv3(3, 16), nn.BatchNorm2d(16), nn.ReLU()]
        in_channels = 16
        for out_channels in (16, 32, 64):
            for _ in range(blocks_per_stage):
                stride = 2 if in_channels != out_channels else 1
                layers.append(ResidualBlock(in_channels, out_channels, stride))
                in_channels = out_channels
        self.features = nn.Sequential(*layers)
        self.classifier = nn.Linear(64, 10)
        for layer in self.modules():
            if isinstance(layer, (nn.Conv2d, nn.Linear)):
                nn.init.kaiming_normal_(layer.weight, nonlinearity="relu")
        nn.init.zeros_(self.classifier.bias)

    def forward(self, x):
        pooled = self.features(x).mean(dim=(2, 3))
        return self.classifier(pooled)
