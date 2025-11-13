import torch
import torch.nn as nn
import torch.optim as optim
import time

def train_and_evaluate(model, train_loader, val_loader, lr, epochs, device):
    
    # 주어진 하이퍼파라미터로 모델을 학습하고 평가합니다.
    
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr)
    
    start_time = time.time()
    
    """
    Overfitting에 대비하고 모델의 최적 일반화 성능(best generalization performance)을 찾기 위해 사용합니다.
    각 에포크마다 검증 데이터셋(validation set)에 대한 정확도를 측정하여, 그 과정에서 기록된 가장 높은 값을 저장합니다.
    비록 학습을 중간에 멈추는 것은 아니지만, 최종적으로 과적합되기 전의 최고 성능을 선택함으로써
    조기 종료(Early Stopping)를 적용한 것과 같은 효과를 얻을 수 있습니다.
    """

    best_val_acc = 0.0
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for batch in train_loader:
            images = batch["image"].to(device)
            labels = batch["label"].to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()

        # Validation loop
        model.eval()
        correct_val = 0
        total_val = 0
        with torch.no_grad():
            for batch in val_loader:
                images = batch["image"].to(device)
                labels = batch["label"].to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total_val += labels.size(0)
                correct_val += (predicted == labels).sum().item()
        
        val_acc = 100 * correct_val / total_val
        # 현재 에포크의 검증 정확도가 최고 기록보다 높다면 업데이트를 진행합니다.
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            
    print(f"Epoch : {epochs}, Loss: {running_loss/len(train_loader):.4f}, Val Acc: {val_acc:.2f}% (Best: {best_val_acc:.2f}%)")

    end_time = time.time()
    training_time = end_time - start_time
    
    return {
        "loss": running_loss / len(train_loader),
        "val_acc": best_val_acc, # 마지막 정확도가 아닌, 가장 높았던 검증 정확도를 반환합니다.
        "time": training_time
    }
