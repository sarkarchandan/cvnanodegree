from turtle import forward
from black import out
from .common import Device
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    """Net class is an example of a simple convolutional network model. Here we have 
    used a single convolution layer, followed by a max pooling layer to reduce the 
    activation size from the convolution layer and finally a fully connected dense 
    layer."""

    conv1: nn.Conv2d
    pool: nn.MaxPool2d
    fc1: nn.Linear
    
    def __init__(self, num_classes: int) -> None:
        super().__init__().__init__()
        # We initialize the 2D convolution layer with a single channel input 
        # for the grayscale images. We want 32 output channels and kernel size 
        # of 3. That means, we want to convolve each image with 32 (3,3) kernels 
        # to generate 32 activation maps out of the colvolution layer.
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3)
        # We initialize the max pooling layer in order to reduce the size of 
        # the activation maps with a kernel size of (2, 2) and sliding window of 
        # stride by 2 pixels. From each sliding window, the max activation value 
        # would be taken.
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        # We initalize a fully connected layer with incoming features size of 
        # 4 * 32, which should be the resulting activation size after down sampling
        # by max pooling layer. The output features are naturally the number of 
        # classes.
        self.fc1 = nn.Linear(in_features=32 * 4, out_features=num_classes)

    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = F.relu(x)
        return x


if __name__ == '__main__':
    pass