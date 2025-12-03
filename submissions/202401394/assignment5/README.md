# 맞춤형 팀플 및 과제 부담 최소화 강의 분류 시스템
## 모델 아키텍처 설명
- 한국외국어대학교 강의계획서의 비정형 텍스트를 입력으로 받아,
  해당 강의의 팀플 유무 (:Classification) 와 과제 부담 지수(:Regression)를
  각각 예측하는 DistilKoBERT 모델을 설계하였습니다.
### Input
- 강의계획서의 `교과목명`, `수업개요`, `수업운영방식`, `기타안내`
  4가지 항목을 하나의 긴 텍스트 시퀀스로 결합
- `monologg/distilkobert`의 토크나이저를 사용하여 한국어 텍스트를 토큰화
  (Max Length = 128, Truncation/Padding 적용)
### Pre-trained Encoder
- DistilKoBERT :적은 데이터셋(100건)에서의 과적합 방지와 빠른 추론 속도를 위해,
  `monologg/kobert` 가 아닌 경량화한 `monologg/distilkobert` (28.4M params)를 인코더로 사용
- Task 1: Teamplay Classification (`model.pt`)
  Context Vector를 입력받아 팀플 여부(0: 없음, 1: 있음)를
  예측하는 Linear Classification Layer를 통과
- Task 2: Burden Score Regression (`burden_model.pt`)
  Context Vector를 입력받아 과제 부담 점수(0~100)를
  예측하는 Linear Regression Layer를 통과
### Loss Function & Optimization
- Loss Function:
  - Classification: `CrossEntropyLoss`
  - Regression: `MSELoss` (Mean Squared Error)
- Optimization:
  - Optimizer: `AdamW` (Learning Rate = 5e-5)
  - Batch Size: 16
  - Epochs: 10
  - Dataset Split: Train(80) / Val(10) / Test(10) (Stratified Split 적용)

## 평가 지표 및 성능 결과
### 평가 지표
- Accuracy (정확도): 전체 테스트 데이터 중 팀플 유무를 정확히 맞춘 비율
- Recall (재현율): 실제 팀플이 있는 강의 중 모델이 팀플이 있다고 정확히 예측한 비율 (**본 프로젝트의 핵심 지표**: 학생 입장에서 팀플 수업을 피하는 것이 목적이므로 False Negative를 줄이는 것이 중요)
- Precision (정밀도): 모델이 팀플이 있다고 예측한 강의 중 실제 팀플인 비율
- F1-Score: Precision과 Recall의 조화 평균

### 성능 결과 (Test Set 기준)
- Accuracy: 0.6000
- Recall: 0.8333 
- Precision: 0.6250
- F1-Score: 0.7143

* accuracy가 더 증가한 model도 사용해봤지만, 이후 inference에서 과적합의
결과를 도출하는 경향이 드러나 accuracy가 0.6000인 모델 기준으로 작성하였습니다.
  
## 모델 가중치 저장 위치
- Teamplay Model: `/content/model.pt`
  (https://drive.google.com/file/d/1hcl250N4eFpdCpxIZlJNLQAv5FJpUvRX/view?usp=sharing)
- Burden Model: `/content/burden_model.pt`
  (https://drive.google.com/file/d/1fCQ8Qr_GxJtcqAn7l91_Bf64GdDfRyyC/view?usp=sharing)
  
## 발견한 문제
- 데이터 부족으로 인한 과적합 및 일반화 한계
  - 총 100건의 데이터로 학습을 진행하여 Train Accuracy(97%)와 Test Accuracy(60%) 간의 차이가 발생
  - 한국외대 강의계획서 특성상 "팀 프로젝트"라는 표현보다
    "조별 활동", "조별 모임" 등의 표현이 혼재되어 사용되는데,
    데이터가 적어 이러한 동의어 관계를 완벽히 일반화하는 데 한계가 있었음
    실제 inference 결과
- [Scenario 1]
  📄 내용:  수업개요: 본 수업은 100% 팀 프로젝트 중심으로 진행됩니다. 
      ...
  🤖 팀플 예측: 🚨 팀플 있음 (확률: 52.7%)
  📉 과제 부담: 18.7점 -> 매우 낮음 (꿀강)

- [Scenario 3]
  📄 내용:  수업개요: 매주 영화를 감상하고 자유롭게 감상평을 나누는 수업입니다.
  ...
  🤖 팀플 예측: 🍀 팀플 없음 (확률: 40.1%)
  📉 과제 부담: 19.8점 -> 매우 낮음 (꿀강)
  
- 팀플 예측은 원활하게 이루어지나, 과제 부담 지수에서 큰 차이로
예측하지 못하는 것으로 파악됨

- **텍스트 모호성 문제**
  - "조별 과제는 없으나..." 와 같이 부정문이 포함된 경우나,
  - "팀 단위 학습을 권장하나 평가는 개인별로..." 와 같은 복합적인 문맥에서 모델이 혼동하는 케이스가 발견
    이는 향후 데이터 증강(Data Augmentation)과 모델 파라미터 튜닝을 통해 개선 가능할 것으로 보임




