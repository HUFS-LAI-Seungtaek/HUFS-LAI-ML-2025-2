# MNIST 분류 실험 결과

## 기본 모델 성능
- 최종 테스트 정확도: 97.02%
- 훈련 시간: 53초

## 실험 결과
### 실험의 구조
실험 1\~4는 연속적인 과정으로, 모두 epoch수는 5로 고정하고 실험했다. 실험1은 hidden size를 조절해 최고 성능을 나타내는 size를 구하고 이를 실험2에 적용하였다. 같은 방식으로 실험2에서 최적 Hidden Layers수를 구해 실험3에 적용했고, 실험3에서는 최적 Dropout rate를 구했다. 결과적으로 실험4는 실험2에 dropout rate를 적용한 것으로, Dropout 유무에 따른 정답률을 비교하고자 하였다.
이렇게 연쇄적으로 이전 실험에서 최고 정답률을 기록한 값을 다음 실험에 적용한 이유는 파라미터 간 상호작용을 판단하고 최종적으로 dropout의 영향을 분석해 보기 위해서이다.

### 실험 1: [최고 정답률을 만드는 Hidden Size 찾기]
- 변경사항: Hidden Size만을 50, 100\~1000까지 100씩 증가시켜 경향성 변화를 관찰했다.
- 결과: Test 정답률은 Hidden Size = 800에서 가장 큰 98.00%였다. 
- 분석: Hidden Size가 50에서 200까지는 증가하다가 이후 감소하는 경향성을 보이지만, 800일 때 예외적으로 증가한 것이 최적값이 되었다. Hidden size의 크기가 작으면 underfitting, 반대로 크면 overfitting의 위험이 높아지고, 이 경우 성능은 떨어진다. 그러나 (AI에 이유를 질문했더니 800에서 가장 높은 성능을 보인 것은 우연히 최적으로 매칭되었거나, seed=42에 의한 우연일 수 있다고 한다.)

### 실험 2: [최고 정답률을 만드는 Hidden Layers 수 찾기]
- 변경사항: 실험1에서 구한 Hidden Size = 800으로 고정하고 Hidden Layer의 개수를 1-10까지 증가시켜 경향성 변화를 관찰했다.
- 결과: Hidden Layers = 1일 때 98.00%로 가장 정확했다.
- 분석: Hidden Layers가 증가할수록 정확도가 감소하는 경향을 보였다. 이는 hidden layer 수가 많이 필요하지 않은 작업에 깊은 hidden layer를 사용해서 오히려 이번 데이터셋에서는 hidden layer가 큰 것이 비효율적이라는 의미이다. Hidden layer가 깊어질수록 overfitting의 가능성이 증가할 것을 추정된다. 첫 epoch에서의 정확도는 hidden layer가 커질수록 급격히 낮아지는 것을 통해 vanishing gradient문제도 발견되었다.

### 실험 3: [최고 정답률을 만드는 Dropout Rate 찾기]
- 변경사항: 실험1의 Hidden Size=800, 실험2의 Hidden Layers=1로 고정하고 Dropout Rate를 0.05\~0.95까지 0.1씩 증가시켜 경향성 변화를 관찰했다.
- 결과: Dropout=0.35일 때 98.07% Test 정답률을 기록했다.
- 분석: Dropout rate는 0.35까지 증가하며 정확도가 향상되었다가 그 후 감소하였다. 실험2 Hidden Layer=1, Dropout rate=0일 떄와 비교하여 실험3에서 Dropout rate=0.35일 때 정답률이 더 높아 적절한 dropout이 overfitting을 방지해 모델의 성능을 높인다는 것은 관찰할 수 있었다.

### 실험 4: [Dropout Rate를 적용하여 실험 2의 정답률 경향성 변화 관찰]
- 변경사항: 실험2와 같은 조건에 실험4에서 구한 Dropout Rate = 0.35를 추가로 적용하여 Hidden Layer 개수에 따른 정답률 경향성 변화를 관찰했다.
- 결과: 최고 정답률을 dropout이 없을 때는 hidden layers=1에서 98.00%, dropout이 있을 때는 hidden layers=1일 때 98.07%이다.
- 분석 (실험2와의 비교): Dropout를 적용한 결과 대체로 hidden layer가 깊어질수록 정답률이 감소하는 경향성을 보였지만 dropout이 없을 떄와 비교하면 일관적이지 않은 결과가 나왔다. 실험3을 통해 구한 최적의 dropout rate는 hidden layer=1일 때의 최적값으로, hidden layer값이 1이 아닐 때에도 최적인 비율이 아니라서 그럴 가능성이 있는 것 같다. 또한 overfitting이 아니거나, vanishing gradient가 발생한 상태에서 dropout를 적용하면 오히려 학습이 더욱 불안정해질 가능성이 있다.
(AI의 보충 설명입니다: Dropout를 적용하는 것 또는 적용하지 않는 것 중 한 쪽이 일관적으로 성능이 좋지 않고 hidden layer에 따라 다른 양상을 보였다. Hidden layer 1\~5층까지는 약간의 과적합 경향이 보여 dropout를 적용했을 때 0.35가 적절한 규제였으면 소폭 성능을 증가시켰다. Hidden layer 6\~10층에서는 vanishing gradient문제로 불안정한 모델에 dropout까지 적용해서 dropout가 오히려 성능을 악화시켰다.)

## 결론 및 인사이트
- 가장 효과적인 개선 방법: 실행한 실험에서는 Hidden Size=800, Hidden Layers=1, Dropout=0.35일 때가 98.07%로 가장 높은 정확도를 기록했다.
- 관찰된 패턴: Hidden size는 200까지는 성능이 증가하고 그 이후는 감소하는 경향을 보였다(800 제외). Hidden layers는 크기가 커질수록 정답률이 낮아지는 경향성을 보였다. Dropout rate는 0.35까지는 증가할수록 정확도가 높아졌지만 그 이후는 증가할수록 정확도 감소의 속도가 빨라졌다.
- 추가 개선 아이디어: Learning rate조절 등 이 실험의 조건 중 변경해 보지 않는 조건들을 추가로 시도해 볼 수 있다. 또한 실험2에서 hidden size를 감소하는 경향성 속 예외적으로 증가한 800보다, 명확하게 증가했다가 감소하는 경향성의 경계점인 200을 적용하면 결과가 달라졌을 수도 있다. 층마다 다른 dropout rate를 적용한다면 현재 실험4의 결과보다 dropout를 적용하는 것이 더 정확도를 증가시켰을 가능성도 있고, epoch수를 5로 고정하는 것이 아니라 각 실험별로 overfitting의 기준을 정해 각각 overfitting이전까지 학습시킬 수도 있을 것이다.

## 출처
- 코드에 표시한 부분 및 디버깅에 생성형 AI를 활용했습니다.
