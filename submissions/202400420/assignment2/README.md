# MNIST 분류 실험 결과


## Experiment Environment Log
- **Code Version(Git)** 46a4e1b
- **Python Version** 3.13.7
- **Key Libraries** torch(2.8.0), torchvision(0.23.0), datasets(4.1.1), matplotlib(3.10.6), numpy(2.3.3)
- **Random Seed** 42 
- **operating system(운영체제)** Windows 11 Home
- **CPU** 13th Gen Intel(R) Core(TM) i5-1340P, 1900Mhz, 12 코어, 16 논리 프로세서
- **RAM(메모리)** 16.0GB
- **GPU** not used (CPU training)

Log에 필요한 항목의 종류 및 확인 방법에 대해 생성형AI(Gemini)의 도움을 받음


## 기본 모델 성능 (교수님 배포)
epoch=3, dropout 코드 없음, validation set 세팅 안 함
- 최종 훈련 Loss: 0.1045
- 최종 훈련 정확도: 96.91%
- 최종 테스트 정확도: 96.83%
- 훈련 시간: 30.46초
- 과적합 정도: 0.08%


## 실험 결과

### 실험 1: [Epoch Quantity Modification 에포크 수 조정]
- 변경사항: "3-1 하이퍼 파라미터 설정" 중 5번째 줄 변수 nb_epochs를 linear하게 증가시키며 경향을 살펴봄 (2부터 20까지)

- 결과: test accuracy가 가장 높은 epoch 8(train accuray(98.91%) 및 test accuracy(97.92%))까지 두 accuracy모두 linear하게 증가. 이후 에포크 9에서부터 test accuracy가 하락하기 시작하지만(97.71%), train accuracy는 계속 증가(98.96%).

- 분석: 테스트 정확도가 하락하기 시작하는 시점인 epoch 9 이전인 **epoch 8**에서 최적의 학습 성능을 가짐. 이후 훈련 데이터에 과적합하여 overfitting이 발생함.

- 실험 결과를 시각적으로 나타낸 그래프는 기존 코드로 생성한 결과를 인용하였음. (results 폴더 안의 1_epoch_quantity_modification_graph.png)



### 실험 2: [Dropout Addition 드롭아웃 기능 추가]
- 변경사항 1: Epoch를 8로 고정(Experiment1로부터 epoch가 8일 때 가장 높은 성능을 기록했으므로)
- 변경사항 2: dropout percent linear하게 증가 (0,10,20,30,40(%))

- 결과 1 (과적합 억제효과): Dropout percent를 0퍼센트에서 40퍼센트까지 증가시켰을 때 과적합정도(훈련정확도-테스트정확도)는 1.21퍼센트에서 -1.28까지 지속적으로 감소하며 overfitting 현상을 억제하는 것이 확인됨. 
- 결과 2 (최적의 Dropout percent): 최종 테스트 정확도는 Dropout percent **10%**일 때 97.93%로 가장 높고, 이후로는 Dropout percent가 높아짐에 따라 40%일 때 최종 테스트 정확도 97.52%까지 점차 하락한다.

- 분석 1: Dropout 기능을 추가했을 때 비활성화 시키는 비율과 과적합정도는 반비례 관계를 보이며, 과적합을 억제하는데 효과가 있음.
- 분석 2: 최종 테스트 정확도는 Dropout percent 10%일 때 가장 높으므로 Dropout이 적절한 수준일 때 모델이 가장 높은 성능을 보이며, 과도하게 Dropout percent가 높을 때는 오히려 underfitting 현상을 발생시켜 성능 저하를 불러올 수 있음.

- 실험 한계: 이번 실험을 설계하는 과정에서 "Dropout코드를 추가하고 비율을 0로 설정했을 때의 학습 결과"가 "Dropout 코드를 추가하지 않은 상태에서의 학습 결과"와 같아야 한다고 가설을 세웠지만, 어떤 조치를 취해도 두 결과가 미세하게 다른 문제를 해결하지 못하였음. (디버깅을 이틀 내내 했습니다ㅠㅠ) 따라서 본 실험의 분석은 Dropout 코드를 추가한 모델 내에서의 비율 조정에 따른 상대적인 성능 비교만 의미를 가질 것으로 보임.

- 실험 결과를 시각적으로 나타낸 그래프는 생성형AI(chatGPT)로 제작함.
(results 폴더 안의 2_dropout_addition_graph.png)



### 실험 3: [Validation Set Partition 검증 데이터 분리]
- 변경사항 1: Epoch을 8로 고정하여 1차 실험 후, 각자 시행 중 validation accuracy가 가장 높은 epoch으로 재실험
- 변경사항 2: 원본 Train Data 60,000개 중 일부 비율을 validation data로 분할 (분할 비율 1/24(train 57,500개, validation 2,500개), 1/12(train 55,000개, validation 5,000개), 1/6(train 50,000개, validation 10,000개))

- 결과 1(최고 validation accuracy): 분할 비율 1/24에서 97.44%(epoch 7), 1/12에서 97.32%(epoch 5), 1/6에서 97.22%(epoch 6)

- 결과 2(최고 validation accuracy가 나타난 epoch에서의 test accuracy): 분할 비율 1/24에서 97.48%(epoch 7), 1/12에서 97.38%(epoch 5), 1/6에서 97.21%(epoch 6)

- 분석 1: **test data의 양이 많을 수록 test accuracy가 높고**, 이것은 test data의 양과 모델의 성능이 비례한다는 것을 알 수 있음. 

- 분석 2: train data, test data 두 가지 데이터만 갖고 모델의 최고 성능 epoch 지점을 찾고 early stopping을 진행하는 것 보다는 validation data를 도입해서 성능을 측정해야함. 최적의 epoch이 data양과 정비례하는 것이 아니기 때문.

- 실험 결과를 시각적으로 나타낸 그래프 및 히트맵은 생성형AI(chatGPT)로 제작함. (results 폴더 안의 3_validation_set_partition_graph.png 및 3_validation_set_partition_heatmap.png)



## 결론 및 인사이트
- 가장 효과적인 개선 방법: 세가지 실험 중 모델 성능 향상에 가장 효과적이었던 방법은 experiment2의 Dropout 기능을 통한 Regulation을 시행하는 것으로, 10%의 Dropout percent를 적용했을 때 test accuracy 97.93%의 가장 높은 성능을 기록함. 또한 experiment1에서는 epoch를 8로 늘렸을 때 test accuracy 97.92%로 가장 높은 성능을 보였고, 이후에는 overfitting 현상으로 오히려 성능이 저하되었음. experiment3에서는 train data의 양에 비례하여 모델 성능이 향상됨.

- 관찰된 패턴:
1. experiment1을 통해 가장 높은 성능을 갖는 고유의 epoch 횟수가 존재함을 확인함. 또한 이 횟수를 넘어선 과도한 훈련은 오히려 overfitting을 발생시켜 새로운 데이터에 대해 적응하지 못하는 현상이 나타남.

2. experiment2를 통해 적절한 Regulation 방법을 사용하여 overfitting과 underfitting을 막고 최적의 성능을 끌어내는 적절한 trade-off를 고려해야한다는 것을 확인.

3. experiment3를 통해 데이터의 양과 모델의 성능이 정비례한다는 것을 확인. 또한 적절한 early stopping 지점 확인을 위해서는 validation set 도입을 통한 적절한 data split이 필수임을 확인.

- 추가 개선 아이디어: Validation Set이 분리된 모델에 다시 실험 1,2의 과정(Dropout 적용 후 최적의 epoch 횟수를 탐색)을 거쳐 최적화 과정을 종합하여 성능을 평가해볼 수 있음. 이는 각 실험 결과에서 얻은 인사이트를 모두 적용시켜 보는 최종 단계가 될 것으로 보임.