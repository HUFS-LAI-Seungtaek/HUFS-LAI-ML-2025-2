# MNIST 분류 실험 결과

## 기본 모델 성능
- 최종 테스트 정확도: 97.19%

## 실험 결과
### 실험 1: [learning rate 변경]
- 변경사항: 
```python
learning_rates = [1e-1, 1e-2, 1e-3, 1e-4]

for learning_rate in learning_rates:
    print(f"learning_rate={learning_rate} : 학습 실행")
    # 모델, 손실함수, 최적화기 설정
    model = MLP().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    # 이하 훈련 루프
```
 위 간단한 반복문 코드를 이용해 4개의 learning ratres(1e-1, 1e-2, 1e-3, 1e-4)를 이용해 훈련을 시켰다.
 
- 결과: 
```
learning_rate=0.1 : 학습 실행
Epoch [1/3], Loss: 1.7841, Train Accuracy: 61.08%
  Test Accuracy: 66.31%
Epoch [2/3], Loss: 1.2467, Train Accuracy: 58.38%
  Test Accuracy: 55.35%
Epoch [3/3], Loss: 1.2987, Train Accuracy: 56.17%
  Test Accuracy: 37.31%
  === learning_rate=0.1 : 훈련 완료 ===

learning_rate=0.01 : 학습 실행
Epoch [1/3], Loss: 0.2458, Train Accuracy: 92.63%
  Test Accuracy: 94.90%
Epoch [2/3], Loss: 0.1624, Train Accuracy: 95.34%
  Test Accuracy: 96.06%
Epoch [3/3], Loss: 0.1408, Train Accuracy: 95.95%
  Test Accuracy: 95.52%
=== learning_rate=0.01 : 훈련 완료 ===

learning_rate=0.001 : 학습 실행
Epoch [1/3], Loss: 0.3162, Train Accuracy: 90.89%
  Test Accuracy: 95.33%
Epoch [2/3], Loss: 0.1436, Train Accuracy: 95.84%
  Test Accuracy: 96.43%
Epoch [3/3], Loss: 0.1013, Train Accuracy: 97.02%
  Test Accuracy: 96.91%
=== learning_rate=0.001 : 훈련 완료 ===

learning_rate=0.0001 : 학습 실행
Epoch [1/3], Loss: 0.7882, Train Accuracy: 81.58%
  Test Accuracy: 90.14%
Epoch [2/3], Loss: 0.3413, Train Accuracy: 90.66%
  Test Accuracy: 91.72%
Epoch [3/3], Loss: 0.2810, Train Accuracy: 92.08%
  Test Accuracy: 92.89%
=== learning_rate=0.0001 : 훈련 완료 ===
```

| learning_rate | Train_accuracy | Test_accuracy | epochs |
| :-----------: | :------------: | :-----------: | :----: |
|     1e-1      |     56.17%     |    37.31%     |   3    |
|     1e-2      |     95.95%     |    95.52%     |   3    |
|     1e-3      |     97.02%     |    96.91%     |   3    |
|     1e-4      |     92.08%     |    92.89%     |   3    |
- 분석:
1e-1의 learning rate로 학습을 시킨 결과, epoch가 증가함에 따라 test accuracy가 크게 감소하는 모습을 보였다. learning rate는 경사하강법에서, optimum에 다가가기 위한 step size이다. 하지만 1e-1은 값이 너무 크기 때문에, optimum에 수렴하지 못하고 발산했다고 볼 수 있다. 반면 learning rate가 1e-4일 때는 learning rate가 1e-2, 1e-3일 때 test accuracy가 95%~96% 인 것에 비해 test accuracy가 92.89%로 하락했다. 그 이유는 learning rate가 너무 작아 학습이 충분히 진행되지 못하여 optimum에 도달하지 못했기 때문에 accuracy가 낮게 나왔음을 유추할 수 있다.

```python
for learning_rate in learning_rates:
    repetition = 3
    sum_of_accuray = 0 # n번 반복하여 나오는 best_accuracies의 평균을 구하기 위함.

    for i in range (repetition):
    # 이하 기존과 동일
    
	    sum_of_accuray += best_test_acc
		print(f"=== learning_rate={learning_rate} : {i+1}번째 훈련 완료  ===")

	  print(f" learning_rate={learning_rate}일때의 accuracy 평균={sum_of_accuray / repetition:.2f}")
```

| learning_rate | Mean Test Accuracy (3 trials) | epochs |
| :-----------: | :---------------------------: | :----: |
|     1e-1      |            58.25%             |   3    |
|     1e-2      |            95.75%             |   3    |
|     1e-3      |            97.05%             |   3    |
|     1e-4      |            92.67%             |   3    |

또한 위의 코드로 learning_rate가 각각 1e-1, 1e-2, 1e-3, 1e-4일 때의 회 반복 실험을 수행하여 best_test_accuracy의 평균값을 측정히여 learning_rate의 변화에 따른 accuracy의 경향성을 확인했다. 단일의 수행이 아니라 여러번 실험을 수행하고 평균으로 나타냈기 때문에 앞서 확인했던 너무 작거나 큰 learning rate는 오히려 성능을 떨어트린다는 해석의 신뢰도를 보강할 수 있다.
추가적으로 learning rate가 1e-1일 때 기존보다 test accuracy가 상승한 이유는, 기존의 코드와는 다르게 반복실험을 수행하며 test accuracy가 감소하면 학습을 중단하는 early stopping도 추가했기 때문에, loss가 본격적으로 발산하기 전 학습이 종료되었기 때문인 것으로 생각한다.

### 실험 2: [epoch 수정]
- 변경사항:
epoch = 5, epoch = 10으로 수정하여 test accuracy에 변동이 있는지 확인해보았다.

- 결과:
```
learning_rate=0.001, epoch=5 : 학습 실행
	Test Accuracy: 97.30%
=== learning_rate=0.001 : 훈련 완료 ===

learning_rate=0.001, epoch=10 : 학습 실행
Epoch [10/10], Loss: 0.0244, Train Accuracy: 99.28%
Test Accuracy: 97.81% 
=== learning_rate=0.001 : 훈련 완료 ===
```

| epochs | Test_accuracy | learning_rate |
| :----: | :-----------: | :-----------: |
|   3    |    96.91%     |     1e-3      |
|   5    |    97.30%     |     1e-3      |
|   10   |    97.81%     |     1e-3      |
- 분석:
learning rate를 1e-3으로 설정한 상태로, epoch를 3, 5, 10 으로 변경하여 학습을 진행하니, test accuracy가 각각 96.91%, 97.30%, 97.81%로 점차 상승하는 경향을 보였다. 이는 데이터에 대한 반복학습의 수가 증가하여 모델이 데이터에 대해 더욱 충분히 학습하였고, 이에 optimum에 더 근접하게 수렴할 수 있었기 때문으로 보인다.
1e-4의 learning rate로 설정하고 epoch를 10까지 학습을 진행하니, epoch가 3일때 보다 충분한 학습이 이루어 져, optimum을 향해 추가적으로 움직일 수 있었으므로 test accuracy가 95.42%로 epoch가 3이었을 때에 비해 2.53%p 증가했다. 이 결과를 통해 epoch가 증가함에 따라 데이터에 대해 충분한 학습이 가능하므로, optimum에 더 가까이 수렴할 수 있며, 그에 따라 accuracy가 향상될 수 있다는 위의 해석을 보강한다.


### 실험 3: [은닉층 크기 조정]
- 변경사항:
```python
class MLP(nn.Module):
    def __init__(self, input_size=784, hidden_size=50, num_classes=10):
    # 이하 동일
    
class MLP(nn.Module):
    def __init__(self, input_size=784, hidden_size=200, num_classes=10):
    # 이하 동일
```

- 결과:
```
learning_rate=0.001, epoch=10 : 학습 실행 # hidden_size=50
 Test Accuracy: 97.06% 
=== learning_rate=0.001 : 훈련 완료 ===

learning_rate=0.001, epoch=10 : 학습 실행 # hidden_size = 200
10. Test Accuracy: 97.85% 
=== learning_rate=0.001 : 훈련 완료 ===
```

- 분석:
지금까지 실험한 learning rate 중 1e-3으로 설정했을 때 test accuracy가 가장 높았으므로 앞으로의 실험에 있어 learning rate는 1e-3으로 고정하고 진행하였다. 이 실험 전까지는 은닉층의 크기가 100으로 고정되어 있었다. 이번 실험3[은닉층 크기 조절]에서 은닉층의 크기가 100에서 50으로 줄었을 때는 test accuracy가 97.06%로, 0.75%p 감소했다. 반면, 은닉층의 크기가 100에서 200으로 늘었을 때는 test accuracy가 97.85%로 0.04%p 증가했다. 이는 은닉층의 크기가 커짐에 따라 더 다양하고 자세한 features를 뽑아낼 수 있기 때문에 accuracy가 소폭 상승 할 수 있었던 것으로 유추한다.

| hidden_size | Test_accuracy | learning_rate |
| ----------- | :-----------: | :-----------: |
| 50          |    97.06%     |     1e-3      |
| 100         |    97.81%     |     1e-3      |
| 200         |    97.85%     |     1e-3      |
### 실험 4:[은닉층 추가]
- 변경사항:
```python
class MLP(nn.Module):
    def __init__(self, input_size=784, hidden_size=200, num_classes=10):
        super(MLP, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),  # 784 -> 100
            nn.ReLU(),                          # 활성화 함수
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes)
            # 100 -> 10
        )
```
- 결과:
```
learning_rate=0.001, epoch=10 : 학습 실행 
Epoch [1/10], Loss: 0.2702, Train Accuracy: 92.08% 1. Test Accuracy: 95.94% 
Epoch [2/10], Loss: 0.1059, Train Accuracy: 96.73% 2. Test Accuracy: 96.87%
Epoch [3/10], Loss: 0.0715, Train Accuracy: 97.79% 3. Test Accuracy: 97.55%
Epoch [4/10], Loss: 0.0502, Train Accuracy: 98.40% 4. Test Accuracy: 97.80% 
Epoch [5/10], Loss: 0.0413, Train Accuracy: 98.66% 5. Test Accuracy: 97.11%
Epoch [6/10], Loss: 0.0318, Train Accuracy: 98.99% 6. Test Accuracy: 98.02% 
Epoch [7/10], Loss: 0.0260, Train Accuracy: 99.13% 7. Test Accuracy: 97.90% 
Epoch [8/10], Loss: 0.0237, Train Accuracy: 99.21% 8. Test Accuracy: 97.75%
Epoch [9/10], Loss: 0.0204, Train Accuracy: 99.31% 9. Test Accuracy: 97.61% 
Epoch [10/10], Loss: 0.0190, Train Accuracy: 99.31% 10. Test Accuracy: 98.14% 
=== learning_rate=0.001 : 훈련 완료 ===
```
- 분석:
은닉층의 크기를 200으로 설정하고, 은닉층 하나를 추가하여 3층 신경망으로 실험을 진행했다. Train accuracy는 epoch가 증가함에 따라 99.31%까지 지속적으로 증가했지만, epoch 6부터 test accuracy는 오히려 98.02%에서 97.xx%으로 정확도가 낮아지는 결과를 확인했다. Train accuracy는 증가하지만, test accuracy가 낮아지는 이 상황은 overfitting이 발생했다고 판단할 수 있다. 은닉층이 증가함에 따라 모델이 더 복잡해져 신경망의 성능이 향상될 수 있으나, 과할 경우 overfitting이 발생하여 train dataset이 아닌 새로운 data가 들어오면 더 낮은 성능이 발생할 수 있다는 것을 위를 통해 입증할 수 있다.

```python
	    # Early Stopping
        if test_acc > best_test_acc:
            best_test_acc = test_acc
        else:
            print(f"Test Accuracy가 감소 : 훈련을 종료합니다. best_accuracy={best_test_acc}") # 한 epoch 전 모델을 저장해야 가장 뛰어난 성능의 모델을 저장할 수 있으나, 간단한 실험이 목적이므로 모델 저장은 생략함
            break
```
이러한 overfitting 문제를 해결하기 위해선 일단 early stopping을 이용할 수 있겠다. Early stopping은 overfitting이 시작되면, 이를 감지하고 학습을 중단해 test accuracy가 떨어지는 것을 방지하는 방법이다. 한 에포크마다 모델을 저장하여, stop된 에포크의 한 에포크 이전의 모델을 최종적으로 저장하여 사용해야 최고 성능의 모델을 이용할 수 있으나, 현재는 모델을 학습시켜 이를 이용하는 것이 목적이 아니라, 실험이 목적이므로, 모델 저장의 부분들은 생략하고 overfitting이 시작되면 학습을 멈추는 부분만 구현해 보았다.
```
learning_rate=0.001, epoch=10 : 학습 실행 
Epoch [1/10], Loss: 0.2685, Train Accuracy: 92.11% 
1. Test Accuracy: 96.11% 
Epoch [2/10], Loss: 0.1028, Train Accuracy: 96.86% 
2. Test Accuracy: 96.55% 
Epoch [3/10], Loss: 0.0705, Train Accuracy: 97.72% 
3. Test Accuracy: 97.15% 
Epoch [4/10], Loss: 0.0512, Train Accuracy: 98.34% 
4. Test Accuracy: 97.62% 
Epoch [5/10], Loss: 0.0404, Train Accuracy: 98.67% 
5. Test Accuracy: 97.76% 
Epoch [6/10], Loss: 0.0339, Train Accuracy: 98.84% 
6. Test Accuracy: 97.87%
Epoch [7/10], Loss: 0.0270, Train Accuracy: 99.09% 
7. Test Accuracy: 97.67% 
Test Accuracy가 감소 : 훈련을 종료합니다. best_accuracy=97.87
```
그 결과 epoch 6에서 epoch7로 넘어가는 과정에서 test accuracy가 97.87%에서 97.67로 감소하자, 학습을 중단하고 나오는 것을 확인할 수 있다.

## 결론 및 인사이트
너무 작거나 큰 learning rate를 이용한 경우엔, optimum에 수렴하지 못하고 학습이 종료되거나 발산하여 학습이 제대로 이루어지지 못하는 모습을 보였다. Epoch가 늘어남에 따라 test_accuracy가 늘어나긴 했으나, 일정 구간을 넘어서 부턴 성능향상이 둔화하고, 수렴하는 모습을 보였다. 따라서 고정된 learning rate를 이용하는 것이 아니라, 학습 초기엔 상대적으로 큰 learning rate를 시작하되, 학습이 진행됨에 따라 learning rate를 줄여나가는 adaptive learning rate를 이용한다면, 더 성능을 높일 수 있을 것이라 생각한다.

뿐만 아니라, 은닉층의 크기가 커지고, layers가 많아짐에 따라 다양하고 풍부한 features을 뽑아낼 수 있으므로 성능이 향상되는 것을 기대할 수 있으나. 과도할 경우 overfitting이 발생하여, train_accuracy는 계속 상승하는 반면, test_accuracy는 오히려 줄어들어 성능이 떨어지는 현상을 발견했다. 따라서 overfitting이 감지되면 학습을 중단하는 early stopping과 dropout을 적용해 overfitting을 방지하는 방안들을 도입하여, 성능이 떨어지지 않게 할 수 있을 것이다.