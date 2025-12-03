# Assignment 5: Model Training and Evaluation

## 파일 구조 설명
```
assignment5/
├── data/
|	├── training.csv		        # 데이터증강 전 training 데이터셋
|	├── training_aug.csv		    # 데이터증강한 데이터셋
|	├── val.csv			            # validation 데이터셋
|	└── test.csv			        # evaluation.ipynb에서 사용하는 테스트용 데이터셋
├── training_optimized5.ipynb       # (필수) 모델 학습 코드
├── val_results_v5.ipynb		    # validation의 시각화 코드
├── val_results_v5.csv		        # training_optimized_v5의 validation결과를 저장해서 val_results_v5.ipynb로 시각화 할 때 불러오기 위함.
├── evaluation.ipynb                # 모델 평가 코드 및 test set 추론 결과의 자세한 시각화
├── inference.ipynb                 # 모델 추론 코드 및 시각화
└── README.md 	                    # 프로젝트 요약 및 결과
```
### 실험 설계
- 사용 모델: Klue RoBERTa Small
- RoBERTa의 한국어 특화 경량모델로 데이터셋의 크기가 작아서 사용했다.
- train, validation, test 비율
	- train : validation : test = 8 : 1 : 1
   	- 데이터셋은 데이터 출처별로 시계열로 분리해 train, validation, test에 출처의 비율이 일정하도록 했다.
	- Assignment4에서 제출한 데이터셋에서 마지막에 데이터 출처(공지, 학사, 장학, IEL, LAI)를 붙인 데이터셋으로 다시 제작했다.
		- 학습 시에는 출처를 사용하지 않지만 데이터의 불균형이 존재하여 출처별 정확도 비교를 하기 위해 시각화 과정에만 사용했다.
- 모델 가중치 링크: https://drive.google.com/drive/folders/1P15TGD68mdmAd64ef7VWVsMK-DQjJq61?usp=sharing
	- 코드에 사용한 코랩 경로: `/content/drive/MyDrive/assignment5/saved_model_v5`
- 학습 방법
	- 관련도, 중요도를 multi-head 방식으로 따로 학습을 진행하는 방식을 사용했다. 
		- 관련도가 0인 경우(없는 경우) 어떠한 형태로든 알림이 오지 않고, 중요도에 따라 알림의 방식을 달리 설정할 것이기 때문에 학습 과정을 분리했다.

## 정확도를 높이기 위한 과정
- 실험 결과 (나머지 실험들도 `val_results_v5.ipynb`와 동일한 형식으로 시각화 했지만 분량이 많아 세부 결과는 생략)

| 구분 | 실험1 | 실험2 | 실험4 | 실험5 |
|------|-------|-------|-------|-------|
| Accuracy | 0.7259 | 0.6074 | 0.7111 | 0.7407 |
| Macro Precision | 0.5758 | 0.4408 | 0.7236 | 0.7013 |
| Macro Recall | 0.5921 | 0.4036 | 0.7056 | 0.7681 |
| Macro F1 | 0.5720 | 0.4169 | 0.7104 | 0.7199 |

- Evaluation 방식
	- 중요도의 경우 데이터셋의 개수가 중요도 2 > 1> 0 순으로 많았지만 중요도 2인 데이터를 맞추는 것이 더 중요하다. 또한 클래스별 편차도 심해서 macro방식을 사용했다.

- 실험별 수치 및 변경사항

| | 실험1 | 실험2 | 실험4 | 실험5 |
|---|---|---|---|---|
| 데이터 증강 여부 | x | x | o | o |
| dropout rate | x | 0.1 | 0.1 | 0.2 |
| learning rate | 2e-5 | 3e-5 | 3e-5 | 2e-5 |
| epoch 수 | 10 | 10 | 10 | 10 |
| batch size | 16 | 16 | 16 | 16 |
| weight decay* | 0.02 | 0.02 | 0.02 | 0.05 |
| warmup ratio* | 0 | 0.1 | 0.1 | 0.1 |
| scheduler type* | linear | cosine | cosine | cosine |
| hidden layer dimension | 768 | 768 | 768 | 768 |
| max token length | 512 | 512 | 512 | 512 |
| stride | 128 | 128 | 128 | 128 |
| early stopping | 2 | 2 | 2 | 2 |

- 데이터 증강
	- 기존 데이터셋은 학습 데이터셋이 1082개였다. 출처별 데이터셋 개수 편차가 심했고 정확도를 포함한 다른 macro 수치들에서도 차이가 심했다.
	- 데이터 증강 방식: `train.csv`에서 임의의 문장부호들을 기존 텍스트 길이의 15% 길이만큼 추가하는 코드를 사용해서 정확도가 낮은 출처인 ‘장학’과 ‘IEL’은 데이터 1개당 3개씩 증강했고, 나머지 출처인 ‘공지’, ‘학사’, ‘LAI’는 기존 데이터 1개당 1개씩 증강해서 `train_aug.csv`를 제작해 3364개의 학습 데이터셋을 제작했다.
- *가 붙은 항목인 weight decay, warmup ratio, scheduler type는 더 성능이 좋은 모델을 만들기 위해 실험1부터 또는 실험2부터 추가한 것들이다.
	- weight decay: overfitting을 방지하기 위한 기법으로, 모델 가중치가 너무 커지는 것을 방지했다. 실험1 이전에 학습을 진행하며 loss값을 보니 오버피팅이 발생하는 것이 보여 추가적으로 넣었다.
	- warmup ratio: learning rate를 0부터 최대 학습률까지 점진적으로 증가시키는 부분의 비율로, 학습 초기 모델 가중치를 안정시키기 위해 실험2부터 사용했다.
	- scheduler type: 학습 후반으로 갈수록 loss가 줄어들도록 learning rate를 낮추는 방법으로, 최적점 주변에서 더 세밀한 탐색을 가능하게 한다. Accuracy를 더 높여보기 위해 실험2부터 cosine으로 설정해 주었다. (설정 안하면 자동으로 linear 사용)
- 추가적으로 learning rate와 dropout rate를 조절해 가며 모델 성능 변화를 확인했다.
- 실험 1 -> 실험2: 오버피팅이 발생한 것이 보여 learning rate를 높이고 dropout를 적용했고 다른 최적화 방식들도 추가했지만 오히려 성능이 감소했다. 
- 실험2 -> 실험4: 데이터셋이 충분하기 않았다고 생각해서 실험3부터(README에는 미포함) 데이터 증강을 사용했다. 데이터 증강 후 성능이 좋아졌다.
- 실험 4 -> 실험 5: 성능을 더 향상시키려 해보았다. Dropout rate를 0.01에서 0.02로 늘리고 learning rate를 3e-5에서 2e-5로 감소시키고 weight decay를 0.02에서 0.05로 늘려 안정성을 확보하며 성능을 향상시키려 했다. 데이터 증강을 해도 오버피팅의 위험이 있다고 생각하여 dropout rate를 증가했고, learning rate를 줄여서 더 안정적으로 학습을 진행하도록 했다. Weight decay를 늘려서 모델 가중치가 불필요하게 커지는 것을 억제하려 했다. 실제로 성능이 향상했다.

## 최종 실험인 `training_optimized5.ipynb`와 test인 `evaluation.ipynb`의 성능 비교

- 전체 성능 평가

| | 실험5 validation | test |
|---|---|---|
| Accuracy | 0.7407 | 0.7538 |
| Macro precision | 0.7013 | 0.7374 |
| Macro recall | 0.7681 | 0.7468 |
| Macro-F1 score | 0.7199 | 0.7387 |

- 여기에는 관련도, 중요도를 따로 표기하지 않았다(`val_results_v5.ipynb`, `evaluation.ipynb` 보시면 있습니다)
	- 관련도 따로, 중요도 따로 평가하면 합한 것보다 성능이 좋게 나온다. 전체의 경우 관련도와 중요도를 모두 맞혀야 정답으로 인정되기 때문이다.

- 카테고리별 성능 비교(관련도, 중요도 합친 것)

| 실험5 validation | 데이터 개수 | Accuracy | Macro precision | Macro recall | Macro F1 |
|---|---|---|---|---|---|
| 공지 | 44 | 0.6818 | 0.7481 | 0.5821 | 0.6213 |
| 장학 | 30 | 0.8 | 0.65 | 0.7333 | 0.6631 |
| IEL | 20 | 0.6 | 0.6 | 0.675 | 0.5925 |
| LAI | 23 | 0.7391 | 0.5119 | 0.4821 | 0.4938 |
| 학사 | 18 | 0.9444 | 0.75 | 0.6667 | 0.7 |
| 전체 | 135 | 0.7407 | 0.7013 | 0.7681 | 0.7199 |

| test | 데이터 개수 | Accuracy | Macro precision | Macro recall | Macro F1 |
|---|---|---|---|---|---|
| 공지 | 44 | 0.75 | 0.6476 | 0.6377 | 0.6373 |
| 장학 | 31 | 0.7097 | 0.7071 | 0.5889 | 0.6147 |
| IEL | 21 | 0.6667 | 0.6875 | 0.7312 | 0.6824 |
| LAI | 24 | 0.7083 | 0.6612 | 0.687 | 0.6691 |
| 학사 | 18 | 1 | 1 | 1 | 1 |
| 전체 | 138 | 0.7536 | 0.7374 | 0.7468 | 0.7387 |

- Accuracy: 데이터 증강을 하기 전 성능이 좋지 않았던 IEL이 증강 후에도 가장 낮은 정확도를 보였고, LAI가 장학보다 낮은 정확도를 보였다. Train, val, test 모두 데이터셋의 개수가 적어서 그런 것 같다. 오히려 학사의 데이터셋 개수가 가장 적지만 가장 높은 정확도를 보인 이유는 관련도, 중요도 패턴이 상대적으로 일관적이라서 (관련도1, 중요도2인 것이 많음) 그런 것이라 생각된다.
- Accuracy, Macro-F1 score 사이의 괴리: Accuracy와 Macro-F1 score의 경향성이 달랐다. 데이터 불균형이 심해 true negative의 비율 차이가 F1 score에 영향을 크게 미친 것 같다. 
- 실험5 validation, test 성능의 차이: 대부분 출처별로 test의 성능이 validation의 성능보다 좋았다. 시계열 분할을 사용해서 최근과 과거 데이터 사이의 패턴 차이 때문이라고 생각된다. 장학의 경우 test가 성능이 더 좋지 않았는데, 데이터셋 개수가 적은 데다가 데이터 수집을 할 때 확인한 바로는 최근 장학금 공지의 경우 이전 장학금 공지 본문의 내용에 비해 형식이 약간 다른 공지들이 있었던 것이 이유같다.

