# Assignment 5: Model Training Report

## 1. Model Architecture
* **Model:** Random Forest Classifier (Scikit-learn)
* **Input Features:** 수면시간, 식사여부, 스트레스, 주종(One-Hot Encoding), 음주량
* **Output:** 숙취 발생 여부 (0: Safe, 1: Hangover)

## 2. 주요 성능 (Evaluation Results)
데이터셋의 클래스 비율을 확인한 결과 불균형(Imbalance) 가능성이 있어, 단순 정확도(Accuracy) 외에 불균형 데이터에 강건한 지표를 함께 평가했습니다.

- **Accuracy:** 0.7000 
- **Balanced Accuracy:** 0.7083 
- **Macro F1-Score:** 0.6970
- **Insight:** Balanced Accuracy가 Accuracy와 큰 차이가 없는 것으로 보아, 특정 클래스에 편향되지 않고 골고루 잘 맞추는 모델임을 확인했습니다.


## 3. Model Weights Link
* [https://drive.google.com/file/d/1afMO_Ca0660h2V5LvfGwl97RGiyHRZLY/view?usp=sharing]