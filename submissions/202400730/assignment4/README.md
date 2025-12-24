# Assignment 4: Data Collection and Analysis Report

**Project Name:** Smart Drinking Coach (개인 맞춤형 안전 음주량 예측)
**Author:** 202400730 (Kyungmin Oh)

## 1. 개요 및 데이터 수집 전략
이 프로젝트는 사용자의 컨디션에 따라 다음 날 숙취가 발생하지 않는 '안전 음주량'을 예측하는 것을 목표로 합니다. 단기간에 대량의 실제 음주 데이터를 확보하는 것은 물리적으로 불가능하므로, **하이브리드(Hybrid) 데이터 수집 전략**을 채택했습니다.

### 1) 데이터 수집 방법 (Hybrid Approach)
* **Step 1. Ground Truth (실제 데이터):** 본인의 최근 음주 경험을 복기하여 5건의 핵심 데이터를 확보했습니다. (예: "잠을 4시간 자고 소주 2병을 마셨더니 숙취가 심했다")
* **Step 2. Data Augmentation (데이터 증강):** 실제 데이터에서 관찰된 패턴(수면 부족 시 주량 감소, 식사 시 주량 증가 등)을 로직화하여, 이를 기반으로 시뮬레이션 데이터 45여 건을 생성해 총 50건의 데이터셋을 구축했습니다.

### 2) 데이터셋 구성
* **파일명:** `drinking_data.csv`
* **총 데이터 수:** 50 Samples
* **타겟 변수(Target):** `hangover` (0: 숙취 없음/Safe, 1: 숙취 있음/Danger)

## 2. 데이터 구조 (Data Dictionary)

| 컬럼명 | 데이터 타입 | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| `sleep_hours` | Float | 전날 수면 시간 (단위: 시간) | 주요 컨디션 지표 |
| `meal_before` | Integer | 음주 전 식사 여부 | 0: 공복, 1: 식사함 |
| `stress_level` | Integer | 당일 스트레스 지수 (1~10) | 높을수록 컨디션 저하 |
| `drink_type` | Object (String) | 마신 술의 종류 | Soju, Beer, Mix(소맥) |
| `amount` | Float | 마신 술의 양 (소주 병 환산 기준) | **핵심 입력 변수** |
| `hangover` | Integer | **숙취 발생 여부 (Label)** | **0: Good, 1: Bad** |

## 3. 탐색적 데이터 분석 (EDA) 결과 요약

`data-analysis.ipynb`를 통해 분석한 주요 내용은 다음과 같습니다.

### 1) 기초 통계 및 분포
* **Class Balance:** 전체 데이터 중 숙취 발생(1)과 미발생(0)의 비율이 비교적 균형을 이루고 있어, 특정 클래스로의 편향(Bias) 없이 모델 학습이 가능함을 확인했습니다.
* **수치형 변수:** 음주량(`amount`)은 0.5병에서 4.0병 사이로 분포하며, 평균적으로 2병 내외에서 숙취 발생 여부가 갈리는 경향을 보입니다.

### 2) 주요 상관관계 (Correlation)
* **Amount vs Hangover:** 가장 강력한 양의 상관관계를 가집니다. 즉, 많이 마실수록 숙취 확률은 정직하게 올라갑니다.
* **Sleep vs Hangover:** 뚜렷한 음의 상관관계를 보입니다. 수면 시간이 7시간 이상인 경우, 평소보다 과음하더라도 숙취가 발생하지 않는 케이스가 존재했습니다.
* **Drink Type:** 시각화 결과, 단일 주종(Soju, Beer)보다 섞어 마신 경우(`Mix`)에 더 적은 양으로도 숙취가 발생하는 경향이 확인되었습니다.

## 4. 향후 계획 (Assignment 5: Model Training)

수집된 데이터를 바탕으로 머신러닝 분류 모델을 구축할 예정입니다.

1.  **데이터 전처리:**
    * 범주형 변수인 `drink_type`(Soju, Beer, Mix)에 대해 **One-Hot Encoding**을 적용합니다.
    * 수치형 변수(`sleep_hours`, `amount`)에 대해 모델 성능 향상을 위한 스케일링(StandardScaler)을 고려합니다.
2.  **모델 선정:**
    * **Logistic Regression:** 각 컨디션 변수가 숙취 확률에 미치는 영향력(가중치)을 해석하기 위해 사용합니다.
    * **Random Forest:** 비선형적인 관계(예: 특정 주종과 수면 시간의 복합적 영향)를 잘 포착하기 위해 비교 모델로 사용합니다.
3.  **목표:** Test Set에 대해 정확도(Accuracy) 85% 이상의 분류 성능을 달성하여, 실생활에서 신뢰할 수 있는 가이드라인을 제공합니다.