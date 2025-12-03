import torch
import torch.nn as nn

class BeatSaberMLP(nn.Module):
    def __init__(self):
        super(BeatSaberMLP, self).__init__()
        # 14 -> 32 -> ReLU
        self.layer1 = nn.Sequential(
            nn.Linear(14, 32),
            nn.ReLU()
        )
        # 32 -> 16 -> ReLU
        self.layer2 = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU()
        )
        # 16 -> 5 (Softmax는 Loss 함수에 포함됨)
        self.layer3 = nn.Linear(16, 5)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x

# from beatsaber_model import BeatSaberMLP 로 사용가능!