import torch

Device: str = 'cuda' if torch.cuda.is_available() else 'cpu'


if __name__ == '__main__':
    pass