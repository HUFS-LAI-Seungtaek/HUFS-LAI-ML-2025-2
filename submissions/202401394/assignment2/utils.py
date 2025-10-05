# utils.py 파일

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import time

# --- 훈련 함수 ---

def train_one_epoch(model, criterion, optimizer, train_loader, device, epoch, nb_epochs):
    """
    한 에포크 동안 모델을 훈련하고 손실 및 정확도를 반환합니다.
    """
    model.train()
    running_loss = 0.0
    correct_train = 0
    total_train = 0
    
    total_batches = len(train_loader)

    for batch_idx, batch in enumerate(train_loader):
        # 데이터를 디바이스로 이동
        imgs = batch["image"].to(device)
        labels = batch["label"].to(device)

        # 그래디언트 초기화
        optimizer.zero_grad()

        # Forward pass
        outputs = model(imgs)
        loss = criterion(outputs, labels)

        # Backward pass
        loss.backward()

        # 파라미터 업데이트
        optimizer.step()

        # 통계 업데이트
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total_train += labels.size(0)
        correct_train += (predicted == labels).sum().item()

        # 100 배치마다 중간 결과 출력
        if (batch_idx + 1) % 100 == 0:
            current_loss = running_loss / (batch_idx + 1)
            current_acc = 100 * correct_train / total_train
            print(f"Epoch [{epoch+1}/{nb_epochs}], Batch [{batch_idx+1}/{total_batches}]")
            print(f"  Loss: {current_loss:.4f}, Train Acc: {current_acc:.2f}%")

    # 에포크 종료 후 통계
    epoch_loss = running_loss / total_batches
    epoch_train_acc = 100 * correct_train / total_train
    
    return epoch_loss, epoch_train_acc

# --- 평가 함수 ---

def evaluate(model, test_loader, device):
    """
    모델의 테스트 정확도를 계산하고 반환합니다. (원본 노트북의 테스트 루프)
    """
    model.eval()  # 평가 모드로 설정
    correct_test = 0
    total_test = 0

    with torch.no_grad():  # 그래디언트 계산 비활성화
        for batch in test_loader:
            imgs = batch["image"].to(device)
            labels = batch["label"].to(device)

            outputs = model(imgs)
            _, predicted = torch.max(outputs, 1)
            total_test += labels.size(0)
            correct_test += (predicted == labels).sum().item()

    test_acc = 100 * correct_test / total_test
    return test_acc

# --- 전체 훈련 루프 ---

def full_train_loop(model, criterion, optimizer, train_loader, test_loader, nb_epochs, device):
    """
    설정된 에포크 수만큼 모델 훈련 및 평가를 반복합니다.
    """
    train_losses = []
    train_accuracies = []
    test_accuracies = []

    print("=== 훈련 시작 ===\n")
    
    for epoch in range(nb_epochs):
        # 훈련 (중간 출력 포함)
        epoch_loss, epoch_train_acc = train_one_epoch(
            model, criterion, optimizer, train_loader, device, epoch, nb_epochs
        )
        
        train_losses.append(epoch_loss)
        train_accuracies.append(epoch_train_acc)

        print(f"\nEpoch [{epoch+1}/{nb_epochs}] 훈련 완료:")
        print(f"  평균 Loss: {epoch_loss:.4f}")
        print(f"  훈련 정확도: {epoch_train_acc:.2f}%")

        # 테스트 정확도 계산
        test_acc = evaluate(model, test_loader, device)
        test_accuracies.append(test_acc)
        print(f"  테스트 정확도: {test_acc:.2f}%")
        print("-" * 60)

    print(f"\n=== 훈련 완료 ===")
    print(f"최종 훈련 정확도: {train_accuracies[-1]:.2f}%")
    print(f"최종 테스트 정확도: {test_accuracies[-1]:.2f}%")
    
    return train_losses, train_accuracies, test_accuracies

# --- 시각화 함수 ---

def plot_results(nb_epochs, train_losses, train_accuracies, test_accuracies):
    """훈련 Loss와 정확도 결과를 시각화합니다."""
    # 원본 노트북의 시각화 코드를 변수명 수정 없이 사용
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Loss 그래프
    epochs_range = range(1, nb_epochs + 1)
    ax1.plot(epochs_range, train_losses, 'b-', marker='o', linewidth=2, markersize=8)
    ax1.set_title('Training Loss', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Loss', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(epochs_range)

    # 정확도 그래프
    ax2.plot(epochs_range, train_accuracies, 'g-', marker='s', linewidth=2,
             markersize=8, label='Train Accuracy')
    ax2.plot(epochs_range, test_accuracies, 'r-', marker='^', linewidth=2,
             markersize=8, label='Test Accuracy')
    ax2.set_title('Accuracy Comparison', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Accuracy (%)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=11)
    ax2.set_xticks(epochs_range)
    ax2.set_ylim(80, 100)

    plt.tight_layout()
    plt.show()
    
# --- 예측 분석 함수 ---

def analyze_predictions(model, test_loader, device, mean, std):
    """
    올바른 예측 7개와 틀린 예측 3개를 시각화하고, 상세 분석을 수행합니다.
    """
    model.eval()
    correct_samples = []
    wrong_samples = []
    
    # 훈련 데이터셋에서 사용한 mean, std를 역변환에 다시 불러와 사용
    # transform 정의를 위해 data_loader.py의 transforms.ToTensor()를 다시 import

    from torchvision import transforms 
    
    with torch.no_grad():
        for batch in test_loader:
            imgs = batch["image"].to(device)
            labels = batch["label"].to(device)
            outputs = model(imgs)
            _, predicted = torch.max(outputs, 1)

            # 정확한 예측과 틀린 예측 분리
            for i in range(len(imgs)):
                if len(correct_samples) >= 7 and len(wrong_samples) >= 3:
                    break

                sample = (imgs[i], labels[i], predicted[i], outputs[i])
                if labels[i] == predicted[i] and len(correct_samples) < 7:
                    correct_samples.append(sample)
                elif labels[i] != predicted[i] and len(wrong_samples) < 3:
                    wrong_samples.append(sample)

            if len(correct_samples) >= 7 and len(wrong_samples) >= 3:
                break
    
    # --- 시각화: 7개 맞춘 것 + 3개 틀린 것 ---
    display_samples = correct_samples + wrong_samples
    
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    axes = axes.flatten()

    for i, (img, true_label, pred_label, output) in enumerate(display_samples):
        # 28x28로 reshape (정규화된 상태)
        img_display = img.cpu().view(28, 28)

        # 정규화를 역변환 (시각화를 위해)
        img_display = img_display * std + mean
        img_display = torch.clamp(img_display, 0, 1)

        axes[i].imshow(img_display, cmap='gray')

        # 색상 설정: 맞으면 초록, 틀리면 빨강
        color = 'green' if true_label == pred_label else 'red'
        axes[i].set_title(f'True: {true_label.item()}, Pred: {pred_label.item()}', color=color, fontweight='bold')
        axes[i].axis('off')

    plt.tight_layout()
    plt.suptitle('Prediction Results (Green: Correct, Red: Wrong)', y=1.02, fontsize=16, fontweight='bold')
    plt.show()

    print(f"올바른 예측: {len([s for s in display_samples if s[1] == s[2]])}개")
    print(f"틀린 예측: {len([s for s in display_samples if s[1] != s[2]])}개")
    
    # --- 틀린 예측에 대한 상세 분석 ---
    if wrong_samples:
        wrong_img, wrong_true, wrong_pred, wrong_output = wrong_samples[0]

        # 소프트맥스를 통해 확률로 변환
        probabilities = torch.softmax(wrong_output, dim=0).cpu()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # 왼쪽: 틀린 예측 이미지
        img_display = wrong_img.cpu().view(28, 28) * std + mean
        img_display = torch.clamp(img_display, 0, 1)
        ax1.imshow(img_display, cmap='gray')
        ax1.set_title(f'Wrong Prediction Case\nTrue: {wrong_true.item()}, Pred: {wrong_pred.item()}',
                      color='red', fontsize=12, fontweight='bold')
        ax1.axis('off')

        # 오른쪽: 확률 분포
        bars = ax2.bar(range(10), probabilities, alpha=0.7, color='lightblue', edgecolor='black')

        # 실제 라벨과 예측 라벨 강조
        bars[wrong_true.item()].set_color('green')
        bars[wrong_pred.item()].set_color('red')

        ax2.set_xlabel('Digit Class', fontsize=11)
        ax2.set_ylabel('Probability', fontsize=11)
        ax2.set_title('Model Confidence by Class', fontsize=12, fontweight='bold')
        ax2.set_xticks(range(10))
        ax2.grid(axis='y', alpha=0.3)

        # 범례 추가
        legend_elements = [Line2D([0], [0], color='green', lw=4, label=f'True Label ({wrong_true.item()})'),
                           Line2D([0], [0], color='red', lw=4, label=f'Predicted ({wrong_pred.item()})')]
        ax2.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        plt.show()

        # 상위 3개 확률 출력
        top3_probs, top3_indices = torch.topk(probabilities, 3)
        print("\n=== 모델의 상위 3개 예측 ===")
        for i, (prob, idx) in enumerate(zip(top3_probs, top3_indices)):
            print(f"{i+1}위: 숫자 {idx.item()} (확률: {prob.item()*100:.2f}%)")

        print(f"\n실제 라벨 {wrong_true.item()}의 확률: {probabilities[wrong_true.item()]*100:.2f}%")

    else:
        print("틀린 예측 샘플이 없습니다. 모델이 모든 테스트 샘플을 정확히 예측했습니다!")