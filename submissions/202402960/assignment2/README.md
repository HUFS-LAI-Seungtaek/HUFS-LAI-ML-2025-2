# MNIST 분류 실험 결과

## 기본 모델 성능
- 최종 테스트 정확도: 97.03%

## 실험 결과
### 실험 1: [하이퍼파라미터 튜닝]
- 변경사항: 학습률 변경 (1e-3 -> 1e-2, 1e-4), 은닉층 크기 조정 (100 -> 50,200), 에포크 수 증가 (3 -> 10)

- 결과:

-실험: Baseline (lr=0.001, hidden=100, epochs=3)
-  Epoch [1/3] Loss: 0.3153, Test Acc: 94.93%
-  Epoch [2/3] Loss: 0.1424, Test Acc: 96.31%
-  Epoch [3/3] Loss: 0.1020, Test Acc: 96.70%
-  최종: Train 96.93%, Test 96.70%, Time 43.9초

-실험: Higher LR (lr=0.01, hidden=100, epochs=3)
-  Epoch [1/3] Loss: 0.2449, Test Acc: 94.95%
-  Epoch [2/3] Loss: 0.1594, Test Acc: 94.44%
-  Epoch [3/3] Loss: 0.1487, Test Acc: 94.86%
-  최종: Train 95.90%, Test 94.86%, Time 44.8초

-실험: Lower LR (lr=0.0001, hidden=100, epochs=3)
-  Epoch [1/3] Loss: 0.7722, Test Acc: 90.40%
-  Epoch [2/3] Loss: 0.3378, Test Acc: 91.96%
-  Epoch [3/3] Loss: 0.2785, Test Acc: 92.92%
-  최종: Train 92.15%, Test 92.92%, Time 44.8초

-실험: Smaller Hidden (lr=0.001, hidden=50, epochs=3)
-  Epoch [1/3] Loss: 0.3662, Test Acc: 93.89%
-  Epoch [2/3] Loss: 0.1851, Test Acc: 95.29%
-  Epoch [3/3] Loss: 0.1383, Test Acc: 96.23%
-  최종: Train 95.97%, Test 96.23%, Time 44.2초

-실험: Larger Hidden (lr=0.001, hidden=200, epochs=3)
-  Epoch [1/3] Loss: 0.2770, Test Acc: 95.99%
-  Epoch [2/3] Loss: 0.1147, Test Acc: 96.86%
-  Epoch [3/3] Loss: 0.0778, Test Acc: 97.25%
-  최종: Train 97.61%, Test 97.25%, Time 44.7초

-실험: More Epochs (lr=0.001, hidden=100, epochs=10)
-  Epoch [3/10] Loss: 0.1023, Test Acc: 96.96%
-  Epoch [6/10] Loss: 0.0530, Test Acc: 97.44%
-  Epoch [9/10] Loss: 0.0311, Test Acc: 97.68%
-  최종: Train 99.25%, Test 97.60%, Time 147.6초


- 분석: 학습률이 너무 크거나 너무 작으면 정확도가 낮아진다. 또한 은닉층 크기를 50으로 줄였을 때 변화는 적지만 정확도가 낮아짐을 알 수 있다. 반면 은닉층 크기를 200으로 늘렸을 때는 성능이 향상되었다. 에포크 수를 10으로 증가함에따라 정확도가 크게 올라간 것을 확인할 수 있지만 걸리는 시간 역시 늘어났다는 단점이 있다. 또한 이 경우 과적합의 상황도 고려해야 함을 알 수 있다.

### 실험 2: [모델 구조 개선]
- 변경사항: 은닉층 추가(3층, 4층 신경망), dropout 추가, 다른 활성화 함수 적용(ReLU -> Sigmoid)

- 결과:
-실험: 2-Layer (Baseline)
-  Epoch [2/5] Loss: 0.1423, Test Acc: 96.49%
-  Epoch [4/5] Loss: 0.0784, Test Acc: 97.04%
-  최종: Train 98.12%, Test 97.29%, Time 75.6초

-실험: 3-Layer
-  Epoch [2/5] Loss: 0.1322, Test Acc: 96.31%
-  Epoch [4/5] Loss: 0.0710, Test Acc: 97.07%
-  최종: Train 98.17%, Test 97.17%, Time 75.0초

-실험: 4-Layer
-  Epoch [2/5] Loss: 0.1410, Test Acc: 96.39%
-  Epoch [4/5] Loss: 0.0756, Test Acc: 97.21%
-  최종: Train 98.20%, Test 97.06%, Time 74.9초

-실험: With Dropout
-  Epoch [2/5] Loss: 0.1957, Test Acc: 96.20%
-  Epoch [4/5] Loss: 0.1351, Test Acc: 96.97%
-  최종: Train 96.36%, Test 97.32%, Time 73.5초

-실험: Sigmoid Activation
-  Epoch [2/5] Loss: 0.2278, Test Acc: 94.15%
-  Epoch [4/5] Loss: 0.1439, Test Acc: 95.85%
-  최종: Train 96.66%, Test 96.25%, Time 74.6초

- 분석: 은닉층 추가에 따른 큰 변화는 없었다. 오히려 정확도가 감소하는 것을 볼 수 있다. 모델이 복잡해졌지만 큰 효과는 없으므로 2개의 은닉층이 가장 적합한 것을 알 수 있다.  dropout을 추가함에 따라 Train정확도는 감소, Test의 정확도는 증가했다. ReLU 대신 Sigmoid함수를 사용한 실험에서는 정확도가 떨어진 것을 보아 원래의 ReLU함수가 성능 강화에 더 적합함을 알 수 있다.

### 실험 3 : [성능 분석]
- 가장 흔한 오분류 패턴 분석
- 4 → 9: 29번
- 7 → 2: 14번
- 7 → 9: 11번
- 3 → 9: 10번
- 7 → 1: 9번

## 결론 및 인사이트
- 가장 효과적인 개선 방법: 학습률: 1e-3, 은닉층 크기 : 150~200, 에포크 수 : 5~8, 2개의 은닉층, dropout추가
- 관찰된 패턴: 학습률은 너무 적어서도, 너무 과해서도 안된다. 은닉층의 크기는 클 수록 정확도가 올라간다. 에포크 수는 과적합을 유발하지 않는 선에서 클 수록 정확도가 높아진다. 또한 dropout을 추가함으로써 성능을 향상시킬 수 있다.
- 추가 개선 아이디어: 현재의 모델인 MLP는 공간적 구조를 반영하지 못한다. 따라서 CNN기반의 모델로 전환하여 시각적 정보의 손실을 줄일 수 있다. (#chat GPT에게 도움을 받았습니다)