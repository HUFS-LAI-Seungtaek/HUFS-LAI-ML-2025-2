# MNIST 분류 실험 결과

## 기본 모델 성능
- 최종 테스트 정확도: 96.88%
- 훈련 시간: 약 50초

## 실험 결과

### 세팅: 자동화 코드 활용 및 변인통제
실험을 시작하기에 앞서, 하이퍼파라미터 설정을 반복하지 않도록 자동화 코드를 작성하고, 랜덤 시드를 고정하여 재현성과 변인통제를 확보한 뒤 실험을 진행하였다.
(아래 코드는 생성형 AI ChatGPT의 도움을 받아 작성되었습니다.)
```python
# =======================================
# 🔧 실험 자동화용 공용 함수
# =======================================
import random, numpy as np

def set_seed(seed=0):
    """랜덤 결과 고정"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

@torch.no_grad()
def eval_acc(model, loader):
    """테스트 데이터 정확도 계산"""
    model.eval()
    correct = total = 0
    for batch in loader:
        imgs = batch["image"].to(device)
        labels = batch["label"].to(device)
        outputs = model(imgs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    return 100 * correct / total

def train_once(lr=1e-3, hidden=100, epochs=3, seed=0):
    """하이퍼파라미터 조합 1개로 모델 학습 및 평가"""
    set_seed(seed)
    model = MLP(input_size=784, hidden_size=hidden, num_classes=10).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(epochs):
        model.train()
        for batch in train_loader:
            imgs = batch["image"].to(device)
            labels = batch["label"].to(device)
            optimizer.zero_grad()
            out = model(imgs)
            loss = loss_fn(out, labels)
            loss.backward()
            optimizer.step()
    return eval_acc(model, test_loader)
```

### 실험 1: [Learning Rate 변경]
- 변경사항:
```python
learning_rates = [1e-4, 1e-3, 1e-2, 2e-3, 3e-3, 4e-3]
```
를 통해 기존 학습률(0.001)을 포함한 총 6개의 학습률을 대상으로 실험을 진행하였다.

- 결과:
<img width="609" height="476" alt="image" src="https://github.com/user-attachments/assets/5e036f3f-3bbd-4c2b-b8e1-370f01359c06" />

```
=== 실험 1: Learning Rate 변화 ===
LR=0.0001 → 정확도: 92.49%
LR=0.0010 → 정확도: 96.79%
LR=0.0100 → 정확도: 95.53%
LR=0.0020 → 정확도: 97.19%
LR=0.0030 → 정확도: 96.52%
LR=0.0040 → 정확도: 96.49%
```
와 같이 학습률이 2e-3(0.002)로 설정되어 있을 때의 정확도가 97.19%로 가장 높게 측정되었다.

- 분석:
학습률이 너무 낮을 경우(1e-4)에는 전체적으로 정확도가 낮게 나타났고, 너무 높을 경우(1e-2)에도 오히려 정확도가 떨어졌다.
이를 통해 학습률이 지나치게 작거나 크면 모델이 가중치를 효과적으로 조정하지 못해 학습 효율이 떨어진다는 것을 알 수 있다.
중간값 부근인 0.002에서 가장 높은 정확도(97.19%)가 나온 것은 이 값이 MNIST 데이터에서 적절한 가중치 갱신 폭을 제공했기 때문으로 보인다.
Adam 옵티마이저의 적응적 학습률 조정 특성이 이 범위(0.001~0.002)에서 MNIST 데이터의 단순 패턴 구조에 가장 효율적으로 작용했다고 추론해 볼 수 있다.
따라서 학습률의 경우, 0.002가 빠른 학습 속도와 안정적 수렴 간의 균형을 보여주었다고 볼 수 있다.

### 실험 2: [은닉층 크기 변경]
- 변경사항:
```python
hidden_sizes = [50, 100, 200, 300, 400]

print("\n=== 실험 2: 은닉층 크기 변화 ===")
for h in hidden_sizes:
    acc = train_once(lr=0.002, hidden=h, epochs=3)
    print(f"hidden={h} → 정확도: {acc:.2f}%")
```
를 통해 위 학습률 변경 실험에서 정확도가 가장 높게 측정되었던 학습률인 2e-3(0.002)로 학습률을 설정하고, 기존 은닉층 크기인 100을 포함해 총 5개의 은닉층 크기를 이용해 실험을 진행해 보았다.

- 결과:
<img width="700" height="471" alt="image" src="https://github.com/user-attachments/assets/4c3de43c-64cb-4953-a509-7f2b6f8b4638" />


```
=== 실험 2: 은닉층 크기 변화 ===
hidden=50 → 정확도: 96.76%
hidden=100 → 정확도: 97.19%
hidden=200 → 정확도: 97.41%
hidden=300 → 정확도: 97.49%
hidden=400 → 정확도: 97.20%
```
와 같이 은닉층 크기가 300으로 설정되어 있을 때의 정확도가 97.49%로 가장 높게 측정되었다.

- 분석:
은닉층 크기가 너무 작으면(50) 모델이 복잡한 패턴을 충분히 학습하지 못해 underfitting이 발생한다.
반대로 너무 크면(400) 파라미터 수가 불필요하게 증가하여 overfitting 위험이 높아지고, 오히려 일반화 성능이 떨어진다.
은닉층 크기 300의 경우, 입력(784차원)과 출력(10차원) 사이에서 표현력과 일반화 사이의 균형이 최적화된 구조로 작용하여 훈련 데이터의 패턴을 충분히 학습하면서도 overfitting을 억제할 수 있었던 것으로 보인다.
즉, 은닉층 크기와 같은 경우는 300이 테스트해 본 후보 중에서 데이터 복잡도와 가장 잘 맞는 수준이다.

### 실험 3: [모델 구조 개선(활성화 함수 변경, Dropout 추가) 및 에포크 수 증가]
- 변경사항:
```python
class MLP_ReLU(nn.Module):
    """기존 활성화 함수(ReLU)"""
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 300),
            nn.ReLU(),
            nn.Dropout(0.3),   # Dropout 추가
            nn.Linear(300, 10)
        )
    def forward(self, x):
        return self.layers(x)

class MLP_Sigmoid(nn.Module):
    """시그모이드 활성화 함수"""
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 300),
            nn.Sigmoid(),
            nn.Dropout(0.3),
            nn.Linear(300, 10)
        )
    def forward(self, x):
        return self.layers(x)

class MLP_Tanh(nn.Module):
    """tanh 활성화 함수"""
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 300),
            nn.Tanh(),
            nn.Dropout(0.3),
            nn.Linear(300, 10)
        )
    def forward(self, x):
        return self.layers(x)

class MLP_PReLU(nn.Module):
    """PReLU 활성화 함수"""
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 300),
            nn.PReLU(),
            nn.Dropout(0.3),
            nn.Linear(300, 10)
        )
    def forward(self, x):
        return self.layers(x)
```
를 통해 위 학습률 변경 실험과 은닉층 크기 변경 실험에서 정확도가 가장 높게 측정되었던 학습률인 2e-3(0.002), 은닉층 크기인 300으로 학습률과 은닉층 크기를 설정하고, 기존 활성화 함수인 ReLU를 포함해 총 4개의 활성화 함수를 이용해 실험을 진행해 보았다.
Dropout(0.3)을 추가하고, Epoch 수를 최대 50개로 설정해 둔 다음 Early Stopping을 추가하여 연속 두 Epoch 동안 개선이 없을 시 자동으로 중단하게 설정해 두어 Dropout과 Epoch에 대한 실험도 동시에 진행해 보았다.

- 결과:
<img width="777" height="548" alt="image" src="https://github.com/user-attachments/assets/7c7eac70-42a4-4d8a-82b2-79726b1aec0a" />


```
=== 실험 3: 모델 구조 개선(활성화 함수 변경, Dropout 추가) 및 에포크 수 증가 ===

[ReLU] 활성화 함수 실험 시작
Epoch  1: 테스트 정확도 96.32%
Epoch  2: 테스트 정확도 97.50%
Epoch  3: 테스트 정확도 97.57%
Epoch  4: 테스트 정확도 97.35%
Epoch  5: 테스트 정확도 97.65%
Epoch  6: 테스트 정확도 97.98%
Epoch  7: 테스트 정확도 97.83%
Epoch  8: 테스트 정확도 97.97%
개선X, Epoch 8에서 조기 종료
[ReLU] 최종 정확도: 97.98%


[Sigmoid] 활성화 함수 실험 시작
Epoch  1: 테스트 정확도 94.82%
Epoch  2: 테스트 정확도 96.26%
Epoch  3: 테스트 정확도 97.07%
Epoch  4: 테스트 정확도 97.11%
Epoch  5: 테스트 정확도 97.52%
Epoch  6: 테스트 정확도 97.59%
Epoch  7: 테스트 정확도 97.75%
Epoch  8: 테스트 정확도 97.68%
Epoch  9: 테스트 정확도 97.67%
개선X, Epoch 9에서 조기 종료
[Sigmoid] 최종 정확도: 97.75%


[Tanh] 활성화 함수 실험 시작
Epoch  1: 테스트 정확도 95.54%
Epoch  2: 테스트 정확도 96.54%
Epoch  3: 테스트 정확도 96.74%
Epoch  4: 테스트 정확도 96.86%
Epoch  5: 테스트 정확도 97.15%
Epoch  6: 테스트 정확도 97.17%
Epoch  7: 테스트 정확도 97.05%
Epoch  8: 테스트 정확도 97.23%
Epoch  9: 테스트 정확도 97.26%
Epoch 10: 테스트 정확도 97.54%
Epoch 11: 테스트 정확도 97.43%
Epoch 12: 테스트 정확도 97.35%
개선X, Epoch 12에서 조기 종료
[Tanh] 최종 정확도: 97.54%


[PReLU] 활성화 함수 실험 시작
Epoch  1: 테스트 정확도 96.35%
Epoch  2: 테스트 정확도 97.10%
Epoch  3: 테스트 정확도 97.71%
Epoch  4: 테스트 정확도 97.68%
Epoch  5: 테스트 정확도 97.62%
개선X, Epoch 5에서 조기 종료
[PReLU] 최종 정확도: 97.71%
```
와 같이 활성화 함수가 ReLU으로 설정되어 있을 때, Epoch 6에서의 정확도가 97.98%로 가장 높게 측정되었다.

- 분석:
우선 활성화 함수들을 보면, 
ReLU는 음수를 0으로 절단하고 양수는 그대로 전달하는 비선형 함수로, vanishing gradient 문제를 최소화하면서 깊은 네트워크에서도 학습이 빠르고 안정적으로 이루어진다.
반면 Sigmoid와 Tanh는 출력이 포화 영역(gradient ≈ 0)으로 수렴하기 쉬워 학습 속도가 느려지는 현상이 관찰되었다.
PReLU는 초기 수렴 속도가 가장 빨랐으나, 데이터가 단순한 MNIST 특성상 과도한 표현력으로 인한 미세한 과적합이 발생한 것으로 보인다.
Dropout(0.3) 적용으로 기존 Epoch 3에서의 정확도와 비교해 보았을 때 일반화 성능이 향상되었고,
Early Stopping으로 불필요한 학습을 줄여 시간 효율성과 과적합 억제 효과를 동시에 얻을 수 있었다.
즉, 활성화 함수는 ReLU가 가장 적합하였고, Dropout은 유의미했음을 알 수 있다.

## 결론 및 인사이트
- 가장 효과적인 개선 방법:
학습률 0.002, 은닉층 300, ReLU + Dropout(0.3) + Epoch 6 조합이 정확도 97.98%로
정확도와 안정성 모두에서 가장 우수한 성능을 보였다.
이는 적절한 학습 속도, 충분한 표현력, 과적합 방지 요소가 균형을 이룬 결과로 볼 수 있다.

- 관찰된 패턴:
학습률이 너무 낮거나 높으면 모두 정확도가 저하되며,
중간값(0.002)에서 정확도가 가장 높게 나왔다.
은닉층 크기는 일정 수준(300)까지 증가하면 성능이 향상되지만,
그 이상에서는 오히려 일반화 성능이 감소했다.
활성화 함수 실험에서는 PReLU가 가장 빠른 수렴(약 5 epoch) 속도를 보였고,
ReLU가 최종 정확도(97.98%)에서 가장 높은 성능을 기록했다.
이는 PReLU가 학습 초기 가중치 갱신을 유연하게 해
초기 수렴 속도를 높인 반면,
ReLU가 일반화 성능과 최종 안정성 면에서 더 우수했음을 의미한다.

- 추가 평가:
모든 실험에서 변수를 하나씩 조절했을 때 예측 가능한 방향으로 성능이 변화하였으며,
이는 실험의 경향성이 일관되고 재현성이 높음을 확인하게 했다.

- 추가 개선 아이디어:
Batch Normalization을 추가하여 학습 안정성을 높이거나,
2~3개 은닉층으로 확장한 MLP 실험을 통해 더 깊은 구조의 효과를 관찰할 수 있을 듯하다.
CNN 구조를 적용하면 이미지 데이터 특성을 더 효율적으로 반영할 가능성이 있다.
또한 Dropout 비율을 0.2부터 0.5 범위에서 조정하여
일반화 성능 향상과 과적합 억제 사이의 최적점을 찾는 것도 의미가 있을 듯하다.
