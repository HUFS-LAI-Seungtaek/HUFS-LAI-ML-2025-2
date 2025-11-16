#은닉층 크기 깊이 조정
hidden_structures = [
    [100],
    [100, 50],
    [100, 50, 25],
    [100, 50, 25, 12]
]

nb_epochs = 3
learning_rate = 2e-3

def make_model(layer_sizes):
    layers = []
    input_dim = 784
    for hidden_dim in layer_sizes:
        layers.append(nn.Linear(input_dim, hidden_dim))
        layers.append(nn.ReLU())
        input_dim = hidden_dim
    layers.append(nn.Linear(input_dim, 10))
    model = nn.Sequential(*layers)
    return model

def train_and_test(structure):
    model = make_model(structure).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
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

print("=== 은닉층 개수별 성능 비교 실험 시작 ===\n")
for structure in hidden_structures:
    acc = train_and_test(structure)
    print(f"구조 {structure} -> Test Accuracy: {acc:.2f}%")
print("\n=== 실험 종료 ===")


#결과
=== 은닉층 개수별 성능 비교 실험 시작 ===

구조 [100] → Test Accuracy: 96.80%
구조 [100, 50] → Test Accuracy: 96.92%
구조 [100, 50, 25] → Test Accuracy: 97.17%
구조 [100, 50, 25, 12] → Test Accuracy: 96.77%

=== 실험 종료 ===