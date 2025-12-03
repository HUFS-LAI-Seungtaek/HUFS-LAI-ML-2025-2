# 📝 TOEFL Writing Automated Scorer (Assignment 5)

## 📌 Project Overview
이 프로젝트는 Assignment 4에서 수집한 60개의 TOEFL 에세이 데이터를 활용하여, **AI가 에세이 점수(0~30점)를 자동으로 예측하는 모델**을 개발하는 과제입니다.
최신 NLP 모델인 **DeBERTa-v3-small**을 기반으로 Fine-tuning을 진행하였으며, 학습 과정에서 RMSE 손실 함수를 사용하여 점수 예측 모델을 구축했습니다.

## 🏗️ Model Architecture
- **Base Model:** `microsoft/deberta-v3-small`
- **Task:** Regression (Sequence Classification with `num_labels=1`)
- **Input:** Tokenized Essay Text (Max Length: 512)
- **Output:** Predicted Score (Float, 0.0 ~ 30.0)
- **Loss Function:** MSE (Mean Squared Error)

## 📂 Data Split Strategy
데이터의 재현성을 위해 `random_state=42`를 고정하여 분할하였습니다.
- **Train Set (80%):** 48개 (모델 학습)
- **Validation Set (10%):** 6개 (학습 중 성능 모니터링 및 Best Model 선정)
- **Test Set (10%):** 6개 (최종 성능 평가용, 학습 미참여)

## 📊 Evaluation Results
Test Set에 대한 최종 평가 결과는 다음과 같습니다.

| Metric | Value | Description |
|--------|-------|-------------|
| **RMSE** | **18.43** | 실제 점수와 평균적으로 약 18점의 오차가 발생함 |
| **Pearson Corr** | **-0.73** | 예측 점수와 실제 점수 간의 상관관계가 낮음 |

### 🧐 Performance Analysis & Limitations (성능 분석 및 한계점)
평가 결과, 모델이 모든 입력에 대해 **약 7~8점 부근의 고정된 값을 예측**하는 **Underfitting(과소적합)** 현상이 관찰되었습니다.

1.  **데이터 부족:** 전체 데이터가 60개로 매우 적어, Transformer 기반의 거대 모델이 점수 분포를 충분히 학습하지 못했습니다.
2.  **학습 불안정:** 적은 데이터로 인해 학습 과정에서 Loss가 충분히 수렴하지 못하고 특정 값(Bias)에 고착화된 것으로 보입니다.
3.  **Inference 보정:** 이러한 한계를 극복하기 위해, `inference.ipynb`에서는 예측된 Raw Score에 스케일링(Scaling)을 적용하는 후처리 로직을 도입하여 데모를 구현했습니다.

## 🚀 How to Run
1. **Training:** `training.ipynb` 실행 → 모델 학습 및 Google Drive 저장
2. **Evaluation:** `evaluation.ipynb` 실행 → Test Set 성능 평가 및 그래프 확인
3. **Inference:** `inference.ipynb` 실행 → 예시 에세이 3개 채점 시연

## 🔗 Model Weights
- **Google Drive Link:** https://drive.google.com/drive/folders/1LHIkyg9RINsgZLtxzqcNckyULZO6SKGP?usp=sharing
