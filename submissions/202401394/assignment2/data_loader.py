
import torch
import numpy as np
from torch.utils.data import DataLoader
from torchvision import transforms
from datasets import load_dataset

# 하이퍼파라미터 (main.py에서 import하여 사용)
# batch_size = 128
# test_batch_size = 1000

def get_mnist_data(batch_size, test_batch_size):
    """
    MNIST 데이터셋을 로드하고, 정규화 통계를 계산하여 DataLoader를 생성합니다.
    """
    print("MNIST 데이터셋을 다운로드 중...")
    mnist = load_dataset("mnist")

    # 데이터셋의 평균과 표준편차 계산 (노트북과 동일하게 1000개 샘플로 추정)
    print("데이터셋의 통계 정보를 계산 중...")
    sample_data = torch.stack([
        transforms.ToTensor()(mnist['train'][i]['image'])
        for i in range(1000)
    ])
    mean = sample_data.mean().item()
    std = sample_data.std().item()
    
    print(f"평균(mean): {mean:.4f}")
    print(f"표준편차(std): {std:.4f}")

    # Transform 정의
    transform = transforms.Compose([
        transforms.ToTensor(),           # PIL Image -> Tensor, 0-255 -> 0-1
        transforms.Normalize((mean,), (std,))  # 정규화
    ])

    # 데이터 변환 함수 정의 (원본 노트북과 이름 동일)
    def transform_dataset(dataset):
        """데이터셋에 변환을 적용하는 함수"""
        def transform_fn(batch):
            # 이미지를 텐서로 변환하고 28x28을 784로 평탄화
            images = [transform(img).view(-1) for img in batch["image"]]
            return {
                "image": torch.stack(images),
                "label": torch.tensor(batch["label"])
            }
        return dataset.with_transform(transform_fn)

    # 훈련/테스트 데이터셋에 변환 적용
    print("데이터셋 변환 중...")
    train_dataset = transform_dataset(mnist["train"])
    test_dataset = transform_dataset(mnist["test"])

    # DataLoader 생성
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=test_batch_size,
        shuffle=False
    )
    
    # 정규화에 사용된 mean, std 값 반환 (시각화 역변환용)
    return train_loader, test_loader, mean, std