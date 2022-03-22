from multiprocessing.sharedctypes import Value
from typing import List
import torch
import numpy as np
import matplotlib.pyplot as plt


Device: str = 'cuda' if torch.cuda.is_available() else 'cpu'


def visualize_FMNIST(x: torch.Tensor, y: torch.Tensor,
                    classes: List[str], grid_size: int = 4) -> None:
    """Plots the FashionMNIST dataset in to square grids
    
    :param x: Image dataset
    :type x: torch.Tensor
    :param y: Image labels
    :type y: torch.Tensor
    :param classes: List of classes
    :type classes: List[str]
    :param grid_size: Size of the square grid
    :type grid_size: int
    """
    if grid_size < 2 or np.floor(grid_size) != grid_size:
        raise ValueError('Grid size must be integer greater or equal to 2')
    if grid_size ** 2 > x.shape[0]:
        raise ValueError('Total number of elements in the grid should be lesser or \
                        equal to length of dataset')
    plt.figure(figsize=(15, 15))
    # Choose grid_size**2 number of random indices from the dataset
    random_indices: np.ndarray = np.random.choice(x.shape[0], size=grid_size**2)
    # Iterate over all possible places in the grid.
    # We range from 1 to use the index for subplot.
    for idx in range(1, grid_size**2 + 1):
        plt.subplot(grid_size, grid_size, idx)
        # The dataset x has the dimension (m, 1, height, width). 
        # This selects a tensor of shape (1, height, width) 
        # and then collapse the dimension 0 and leaves just 
        # (height, width), basically a 2D image.
        image: torch.Tensor = torch.squeeze(x[random_indices[idx - 1]], dim=0)
        plt.imshow(image, cmap='gray')
        plt.title(classes[y[random_indices[idx - 1]].item()])
        plt.axis('off')
    plt.show()
    

if __name__ == '__main__':
    pass
