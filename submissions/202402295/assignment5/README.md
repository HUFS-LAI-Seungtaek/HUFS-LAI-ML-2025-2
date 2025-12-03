# Assignment 5: Model Training and Evaluation

## 1. 프로젝트 개요
- 프로젝트 주제: 관심 뉴스 예측 (사용자가 관심 있을 법한 뉴스 분류)
- 데이터: 제목 + 요약을 합쳐서 텍스트로 사용, 라벨: 관심 있음(1) / 관심 없음(0)

## 2. 모델 아키텍처
- 모델 타입: Feedforward Neural Network (PyTorch)
- 입력 차원: TF-IDF 벡터 차원 (max_features=10000)
- 히든 레이어: 256 units, ReLU activation
- Dropout: 0.3
- 출력 레이어: 2 units (관심 있음 / 관심 없음)

## 3. 데이터셋 분할
- Train / Validation / Test = 70% / 15% / 15%

## 4. 학습 과정
- Loss: CrossEntropyLoss
- Optimizer: Adam, lr=0.001
- Epochs: 10
- Batch size: 32
- 학습 곡선 및 정확도 시각화 포함
- Validation 성능 모니터링 포함

## 5. 평가 지표
- Accuracy, Precision, Recall, F1-score
- Test set에서 최종 평가 수행
- 결과:

| Metric     | Score  |
|------------|-------|
| Accuracy   | 0.87037 |
| Precision  | 0.916031 |
| Recall     | 0.833333 |
| F1-score   | 0.872727 |

## 6. 모델 가중치 및 벡터화기 위치
- `news_model.pth` : https://drive.google.com/file/d/1WDD0Ptkqn5x7lXXlvPmp4IQSkIs3HIEW/view?usp=drive_link
- `tfidf.pkl` : https://drive.google.com/file/d/14s9YqXzfvoHSCDcAdr02MZ1pceL9LIRG/view?usp=drive_link

## 7. 특이사항 및 한계
- 실제 사용자 뉴스 선호 데이터가 없고 직접 붙이기엔 양이 너무 많기 때문에(1800개 뉴스) Ground Truth 라벨을 카테고리로 1차 키워드로 2차 분류하여 0과 1로 라벨링 진행( 0: 선호 안함 1: 선호함)
- 데이터가 소량이라 모델이 과적합(overfitting) 경향 있음
- 실제 뉴스 데이터보다는 샘플 뉴스(임의로 만든 뉴스)로 inference 테스트
- 모델 개선 시 더 큰 데이터셋과 더 큰 모델이 필요할 것으로 생각됨
