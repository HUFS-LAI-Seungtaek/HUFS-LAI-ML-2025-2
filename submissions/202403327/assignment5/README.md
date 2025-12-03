# Assignment 5: Model Training Report

## 1. Model Architecture

본 프로젝트에서는 문맥을 기반으로 단어를 **Noun(0) / Verb(1)** 두 클래스로 분류하는 **Naive Bayes 기반 이진 분류 모델**을 설계하였다.

### Input Features

* **TF-IDF (Term Frequency-Inverse Document Frequency)** 기반 텍스트 벡터
* 불용어(Stopwords) 제거 적용

### Model

* **Algorithm**: Multinomial Naive Bayes (Scikit-learn `MultinomialNB`)

* **Reason for Selection**: 데이터셋 크기가 작고(200개), 텍스트 분류에서 빠르고 준수한 성능을 보장하는 베이스라인 모델임.

* **Hyperparameters**: Default settings (alpha=1.0)

### Output

* **0**: Noun (명사)

* **1**: Verb (동사)

## 2. Evaluation Results

테스트셋 40개(각 클래스 20개)를 사용해 모델을 평가한 결과는 다음과 같다.

### Classification Report

| Class | Precision | Recall | F1-score | Support | 
 | ----- | ----- | ----- | ----- | ----- | 
| **Class 0 (Noun)** | 0.67 | 0.90 | 0.77 | 20 | 
| **Class 1 (Verb)** | 0.85 | 0.55 | 0.67 | 20 | 
| **Average / Total** | **0.76** | **0.72** | **0.72** | **40** | 

### Overall Metrics

* **Accuracy**: 0.7250

* **Macro Avg F1**: 0.72

* **Weighted Avg F1**: 0.72

### Confusion Matrix

|  | Predicted 0 (Noun) | Predicted 1 (Verb) | 
 | ----- | ----- | ----- | 
| **Actual 0 (Noun)** | **18** | 2 | 
| **Actual 1 (Verb)** | 9 | **11** | 

### Insight

* **Noun(Class 0)** 은 Recall(0.90)이 높아 대부분 잘 찾아내지만, **Verb(Class 1)** 는 Recall(0.55)이 낮아 실제 동사를 명사로 잘못 예측하는 경향(False Negative)이 강하다.

* 전체 정확도는 **72.5%** 이며, 향후 성능 향상을 위해서는 동사(Verb) 클래스의 특징을 더 잘 포착할 수 있도록 데이터 증강이나 모델 파라미터 튜닝이 필요하다.

## 3. Model Weights

학습된 모델 가중치 파일은 아래 링크를 통해 구글 드라이브에서 다운로드할 수 있으며, Inference 시 로드하여 사용할 수 있다.

* **Download Link:** [Google Drive Link](https://drive.google.com/file/d/1JUN2MLdzNX_gHntvkUtT5DIe2Z1pmJuP/view?usp=drive_link)

## 4. File Descriptions

본 제출물은 다음 구조로 이루어져 있다.

* **`training.ipynb`**: 데이터 전처리, 모델 설계 및 학습, 최종 가중치 저장.

* **`evaluation.ipynb`**: 저장된 모델을 로드하여 Test set에 대한 성능 평가 및 시각화.

* **`inference.ipynb`**: 실제 새로운 문장을 입력하여 모델이 올바르게 분류하는지 확인하는 추론 코드.

* **`README.md`**: 프로젝트 개요, 모델 구조 및 성능 분석 보고서.
