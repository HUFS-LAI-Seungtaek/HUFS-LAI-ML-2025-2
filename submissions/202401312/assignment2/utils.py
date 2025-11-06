import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from datasets import load_dataset

# ReLU 활성화 함
class MLP(nn.Module):
    def __init__(self, input_size=784, hidden_size=100, num_classes=10):
        super(MLP, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes)
        )
    def forward(self, x):
        return self.layers(x)

# Tanh 활성화 함수
class MLP_Tanh(nn.Module):
    def __init__(self, input_size=784, hidden_size=100, num_classes=10):
        super(MLP_Tanh, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, num_classes)
        )
    def forward(self, x):
        return self.layers(x)

# Sigmoid 활성화 함수
class MLP_Sigmoid(nn.Module):
    def __init__(self, input_size=784, hidden_size=100, num_classes=10):
        super(MLP_Sigmoid, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.Sigmoid(),
            nn.Linear(hidden_size, num_classes)
        )
    def forward(self, x):
        return self.layers(x)

# 
def DataLoader_exper(batch_size=128, test_batch_size=1000):
    # MNIST 데이터셋 로딩
    mnist = load_dataset("mnist")

    # 데이터셋의 평균과 표준편차 계산 (1000개 샘플로 추정)
    sample_data = torch.stack([
        transforms.ToTensor()(mnist['train'][i]['image']) 
        for i in range(1000)])
    mean = sample_data.mean().item()
    std = sample_data.std().item()

    # Transform 정의
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((mean,), (std,))
    ])

    # 데이터 변환 함수 정의
    def transform_dataset(dataset):
        def transform_fn(batch):
            images = [transform(img).view(-1) for img in batch["image"]] 
            return {
                "image": torch.stack(images), 
                "label": torch.tensor(batch["label"])
            }
        return dataset.with_transform(transform_fn)

    # 훈련/테스트 데이터셋에 변환 적용
    train_dataset = transform_dataset(mnist["train"])
    test_dataset = transform_dataset(mnist["test"])
    
    # DataLoader_exper 생성
    train_loader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True  # 훈련 데이터는 섞기
    )
    test_loader = DataLoader(
    test_dataset,
    batch_size=test_batch_size,
    shuffle=False  # 테스트 데이터는 순서 유지
    )
  
    return train_loader, test_loader