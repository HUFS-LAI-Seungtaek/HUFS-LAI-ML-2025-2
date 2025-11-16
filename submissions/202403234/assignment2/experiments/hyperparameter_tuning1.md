# 러닝레이트 실험
learning_rates = [1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]
nb_epochs = 3

def train_and_eval(lr):
    model = MLP().to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    for epoch in range(nb_epochs):
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

print("=== 러닝레이트 실험 시작 ===\n")
for lr in learning_rates:
    acc = train_and_eval(lr)
    print(f"Learning Rate {lr:.0e} -> Test Accuracy: {acc:.2f}%")
print("\n=== 실험 종료 ===")



#결과
=== 러닝레이트 실험 시작 ===

Learning Rate 1e-05 -> Test Accuracy: 84.44%
Learning Rate 3e-05 -> Test Accuracy: 89.92%
Learning Rate 1e-04 -> Test Accuracy: 92.68%
Learning Rate 3e-04 -> Test Accuracy: 95.31%
Learning Rate 1e-03 -> Test Accuracy: 97.08%
Learning Rate 3e-03 -> Test Accuracy: 96.90%
Learning Rate 1e-02 -> Test Accuracy: 95.84%
Learning Rate 3e-02 -> Test Accuracy: 92.88%

=== 실험 종료 ===