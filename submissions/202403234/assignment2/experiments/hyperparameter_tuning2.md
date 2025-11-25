#러닝레이트 에포크


learning_rates = [1e-5, 1e-3, 3e-2]
epoch_list = [3, 5, 10]
print("=== 러닝레이트랑 에포크 비교 실험 시작 ===\n")

def train_and_eval(lr, epochs):
    model = MLP().to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    for epoch in range(epochs):
        model.train()
        for batch in train_loader:
            imgs = batch["image"].to(device)
            labels = batch["label"].to(device)
            optimizer.zero_grad()
            loss = criterion(model(imgs), labels)
            loss.backward()
            optimizer.step()

    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for batch in test_loader:
            imgs = batch["image"].to(device)
            labels = batch["label"].to(device)
            preds = model(imgs).argmax(1)
            total += labels.size(0)
            correct += (preds == labels).sum().item()
    return 100 * correct / total


for lr in learning_rates:
    for ep in epoch_list:
        acc = train_and_eval(lr, ep)
        print(f"Learning Rate {lr:.0e}, Epochs {ep} -> Test Accuracy: {acc:.2f}%")
print("\n=== 실험 종료 ===")


#결과
=== 러닝레이트랑 에포크 비교 실험 시작 ===

Learning Rate 1e-05, Epochs 3 -> Test Accuracy: 85.12%
Learning Rate 1e-05, Epochs 5 -> Test Accuracy: 87.95%
Learning Rate 1e-05, Epochs 10 -> Test Accuracy: 90.37%
Learning Rate 1e-03, Epochs 3 -> Test Accuracy: 96.94%
Learning Rate 1e-03, Epochs 5 -> Test Accuracy: 97.49%
Learning Rate 1e-03, Epochs 10 -> Test Accuracy: 97.76%
Learning Rate 3e-02, Epochs 3 -> Test Accuracy: 91.29%
Learning Rate 3e-02, Epochs 5 -> Test Accuracy: 90.38%
Learning Rate 3e-02, Epochs 10 -> Test Accuracy: 91.50%

=== 실험 종료 ===