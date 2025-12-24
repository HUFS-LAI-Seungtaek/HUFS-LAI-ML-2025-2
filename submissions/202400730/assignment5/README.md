# Assignment 5: Model Training Report

## 1. Model Architecture
* **Model:** Random Forest Classifier (Scikit-learn)
* **Input Features:** 수면시간, 식사여부, 스트레스, 주종(One-Hot Encoding), 음주량
* **Output:** 숙취 발생 여부 (0: Safe, 1: Hangover)

### 3. 주요 성능 (Evaluation Results)
데이터셋의 클래스 비율을 확인한 결과 불균형(Imbalance) 가능성이 있어, 단순 정확도(Accuracy) 외에 불균형 데이터에 강건한 지표를 함께 평가했습니다.

- **Accuracy:** 0.6000
- **Balanced Accuracy:** 0.7500
- **Macro F1-Score:** 0.5833
- **Insight:** 데이터 양이 적지만(50건), Random Forest 모델이 컨디션과 음주량의 복합적인 관계를 잘 학습하여 유의미한 예측 결과를 보여줍니다.

## 3. Model Weights Link
* [https://drive.google.com/file/d/1afMO_Ca0660h2V5LvfGwl97RGiyHRZLY/view?usp=sharing]