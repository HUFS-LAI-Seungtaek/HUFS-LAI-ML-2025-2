# 5th Assignment: Model Training and Evaluation
**Project: 타격 지표 기반 타자의 타격 유형 자동 분류를 통한 이사만루 육성 가이드 시스템**
- 사용자가 타격 지표(타석, 타수, 안타, 2루타, 3루타, 홈런, 삼진, 볼넷)를 입력합니다.
- MLP 모델이 입력된 타격 지표로 계산한 파생 변수(H_Ratio, 2B_3B_Ratio, HR_Ratio, SO_Ratio, BB_Ratio)를 입력으로 받아 타자의 타격 유형을 결정합니다.
- 타자의 타격 유형에 맞는 이사만루 육성 가이드를 제시합니다.

## 1. 모델 아키텍처
- Assignment 3에서는 Random Forest Classifier 구조를 고려했으나, 최종적으로 MLP (Multi-Layer Perceptron) 구조를 채택했습니다.

- **Input Layer**
  - 사용자가 입력한 타격 지표를 바탕으로 계산한 5개의 파생 변수(H_Ratio, 2B_3B_Ratio, HR_Ratio, SO_Ratio, BB_Ratio)를 입력으로 받습니다.

- **Hidden Layer 1** (64 nodes)
  - 5개의 입력 특성을 64차원으로 확장하여 데이터 내에 숨겨진 복잡하고 비선형적인 패턴을 학습합니다.
  - 활성화 함수로 ReLU를 사용하여 기울기 소실 문제를 방지합니다.

- **Dropout** (0.3)
  - 수집한 데이터셋이 195개로 작은 점을 고려하여, 과적합을 방지하기 위해 Dropout 비율을 30%로 설정하여 적용합니다.

- **Hidden Layer 2** (32 nodes)
  - 1차로 학습된 특징들을 32차원으로 압축하여 분류에 필요한 가장 핵심적인 정보만을 추출합니다.
  - 마찬가지로 활성화 함수로 ReLU를 사용하여 기울기 소실 문제를 방지합니다.

- **Output Layer** (3 nodes)
  - 최종적으로 3가지 타자 유형(GAP, POWER, CONTACT)에 대한 예측 점수를 출력합니다.
  - 이후 Argmax 연산을 통해 가장 점수가 높은 클래스를 최종 타자 유형으로 결정합니다.

- **Loss Function**
  - 클래스 불균형 문제가 있는 점을 고려하여, Weighted CrossEntropyLoss를 사용합니다.

- **Optimizer**
  - Adam을 사용하고, Learning Rate는 0.001입니다.

## 2. training
- 수집한 데이터셋이 작은 점을 고려하여, K-Fold Cross Validatoin을 사용했습니다.
- 전체 데이터셋의 80%(156개)에 해당하는 Train/Validation Set을 4개로 분할하여 4-Fold Cross Validation을 수행했습니다.
- Best 모델을 선택하는 기준은 클래스 불균형 문제가 있는 점을 고려하여, Validation Macro F1을 사용했습니다.
- 결과적으로 Fold 3의 Epoch 23 시점의 모델이 Validation Macro F1 0.9451을 기록하여 Best 모델로 선정되었습니다.

## 3. evaluation (평가 지표 및 성능 결과)
- 전체 데이터셋의 20%(39개)에 해당하는 Test Set을 사용했습니다.
- 타자 유형별 평가 지표로는 Precision, Recall, F1을 사용했습니다.
  - GAP: Precision 0.8333 / Recall 0.6522 / F1 0.7317
  - POWER: Precision 0.7000 / Recall 0.8750 / F1 0.7778
  - Contact: Precision 0.5455 / Recall 0.7500 / F1 0.6316
- 종합 평가 지표로는 Macro Precision, Macro Recall, Macro F1, Weighted F1, Accuracy, Top-2 Accuracy를 사용했습니다.
  - Macro Precision: 0.6929
  - Macro Recall: 0.7591
  - Macro F1: 0.7137
  - Weighted F1: 0.7206
  - Accuracy: 0.7179
  - Top-2 Accuracy: 1.0000

## 4. 학습 및 평가 과정에서 발견한 특이사항
- 모델의 1순위 예측값과 2순위 예측값 내에 정답이 포함될 확률인 Top-2 Accuracy가 1.0000을 기록했다는 점이 매우 고무적이라 생각합니다. 이는 비록 1순위 예측이 빗나가더라도, 모델이 정답을 유력한 차순위 후보로 항상 고려하고 있음을 의미하기 때문에 좋은 모델이라고 볼 수 있습니다.
- evaluation 결과를 히트맵으로 시각화하여 분석한 결과, 완전히 반대 성향이라고 볼 수 있는 POWER와 CONTACT 간의 오분류는 단 한 건도 발생하지 않았습니다. 즉, POWER와 CONTACT의 중간 성향이라고 볼 수 있는 GAP과의 경계에서만 오분류가 발생한다고 볼 수 있습니다.

## 5. 학습 및 평가 과정에서 발견한 한계
- 사용한 데이터셋의 크기가 작았기 때문에 모델의 성능 결과를 극대화하지 못했다고 생각합니다. 더 큰 데이터셋을 사용한다면 모델의 성능을 향상시킬 수 있을 것이라 생각합니다.
- evaluation 결과를 히트맵으로 시각화하여 분석한 결과, GAP과 CONTACT 간의 오분류가 가장 빈번하게 발생했습니다. POWER 유형은 HR_Ratio가 강력한 변별력을 제공하는 반면, CONTACT와 GAP 유형을 가르는 지표들은 상대적으로 변별력이 낮아 모델이 완벽한 분류 성능을 달성하는 데 한계가 있었다고 생각합니다.

## 6. 모델 가중치 저장 위치
- Hugging Face에 모델 가중치인 best_batter_classifier.pth와 스케일러인 scaler.pkl을 업로드했습니다.
- 링크: https://huggingface.co/ohsj611/batter_classifier/tree/main
