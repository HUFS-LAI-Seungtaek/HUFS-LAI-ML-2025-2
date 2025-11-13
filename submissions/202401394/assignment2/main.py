# main.py 파일

import torch
import torch.nn as nn
import torch.optim as optim
from models import MLP
from data_loader import get_mnist_data
from utils import full_train_loop, plot_results, analyze_predictions
import time
import numpy as np
import sys
# sys.path.append('/content/') # 주피터 환경에서는 경로 추가 필요할 수 있음

# --- 하이퍼파라미터 설정 (원본 노트북과 동일) ---
batch_size = 128        # 배치 크기
test_batch_size = 1000  # 테스트 배치 크기
learning_rate = 1e-3    # 학습률 (0.001)
nb_epochs = 3           # 에포크 수

# --- 디바이스 설정 ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def print_setup(model):
    """훈련 환경 및 모델 정보를 출력합니다."""
    # 원본 노트북의 출력 로직 그대로 사용
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("Using CPU")
        
    # 모델 구조 및 파라미터 출력
    print("모델 구조:")
    print(model)
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n총 파라미터 수: {total_params:,}")
    print(f"학습 가능한 파라미터 수: {trainable_params:,}")
    print("\n레이어별 파라미터:")
    for name, param in model.named_parameters():
        print(f"{name}: {param.shape} ({param.numel():,} 개)")
        
    # 하이퍼파라미터 요약
    print("\n=== 하이퍼파라미터 ===")
    print(f"배치 크기: {batch_size}")
    print(f"테스트 배치 크기: {test_batch_size}")
    print(f"학습률: {learning_rate}")
    print(f"에포크 수: {nb_epochs}")
    print(f"\n사용 디바이스: {device}")
    if device.type == "cuda":
        print(f"GPU 이름: {torch.cuda.get_device_name(0)}")
        print(f"GPU 메모리: {torch.cuda.get_device_properties(0).total_memory // 1024**3} GB")

def main():
    # 1. 환경 및 모델 정보 확인
    # 모델을 미리 생성하여 파라미터 수 계산 및 출력에 사용
    initial_model = MLP()
    print_setup(initial_model)
    del initial_model # 훈련용 모델은 새로 생성

    # 2. 데이터 로더 및 통계 준비
    train_loader, test_loader, mean, std = get_mnist_data(batch_size, test_batch_size)

    # 3. 모델, 손실함수, 최적화기 초기화
    model = MLP().to(device)  # 모델을 GPU로 이동
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    
    # 4. 훈련 시작 및 결과 저장
    start_time = time.time()
    train_losses, train_accuracies, test_accuracies = full_train_loop(
        model, criterion, optimizer, train_loader, test_loader, nb_epochs, device
    )
    end_time = time.time()

    # 5. 최종 결과 요약 및 시각화
    print("\n" + "=" * 60)
    plot_results(nb_epochs, train_losses, train_accuracies, test_accuracies)

    print("=== 최종 결과 요약 ===")
    print(f"최종 훈련 Loss: {train_losses[-1]:.4f}")
    print(f"최종 훈련 정확도: {train_accuracies[-1]:.2f}%")
    print(f"최종 테스트 정확도: {test_accuracies[-1]:.2f}%")
    print(f"과적합 정도: {train_accuracies[-1] - test_accuracies[-1]:.2f}% (훈련-테스트 정확도 차이)")
    print(f"총 훈련 시간: {end_time - start_time:.2f} 초")

    # 6. 예측 상세 분석
    print("\n" + "=" * 60)
    analyze_predictions(model, test_loader, device, mean, std)

if __name__ == '__main__':
    main()