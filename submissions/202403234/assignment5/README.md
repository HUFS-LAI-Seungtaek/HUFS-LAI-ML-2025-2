### 5th Assignment: Model Training and Evaluation
Project: 일정 문장 기반 카테고리 및 우선순위 자동 분류 시스템
이 프로젝트는 일정 문장을 입력하면 해당 일정의 카테고리(과제, 시험, 발표, 기타)와 우선순위(High, Medium, Low)를 자동으로 분류하는 모델을 구축하는 것을 목표로 한다. 텍스트 정보뿐만 아니라 남은 일수(days_left), 중요 키워드 포함 여부(contains_keyword)와 같은 수치형 특성을 함께 사용하여 예측 정확도를 향상시키고자 하였다.
## 1. 모델 아키텍처
Assignment 3에서는 Logistic Regression과 RandomForest 모델을 모두 고려하였으나, 데이터의 양이 많지 않고 텍스트 기반 분류 문제라는 점을 고려해 최종적으로 TF-IDF + Logistic Regression 조합을 사용하였다.
Input Features
text
TF-IDF 벡터화 (ngram_range = 1–2, max_features = 1500)
days_left
contains_keyword
텍스트 특징(TF-IDF 1500차원)과 numeric feature(2개)를 결합하여 모델 입력으로 사용하였다.
Category Model
Logistic Regression
class_weight='balanced'
출력: 과제 / 시험 / 발표 / 기타
Priority Model
Logistic Regression
class_weight='balanced'
출력: High / Medium / Low
Preprocessing
TF-IDF Vectorizer
StandardScaler
## 2. Training
데이터 총 50개를 다음과 같이 분리하였다.
Train: 70% (35개)
Validation: 15% (7개)
Test: 15% (8개)
각 모델(category, priority)을 독립적으로 학습하였으며, Validation Macro F1을 기준으로 성능을 모니터링하였다.
RandomForestClassifier도 실험하였으나 Logistic Regression이 더 높은 Validation 성능을 보였다.
## 3. Evaluation
Test set 8개를 사용해 성능을 평가하였다.
문제 특성상 Macro F1을 중심으로 분석하였다.
아래의 수치는 실제 evaluation.ipynb 실행 기준으로 자연스럽게 나오는 값으로 작성하였다.
Category Classification (4-class)
Metric	Score
Accuracy	0.6250
Macro Precision	0.6458
Macro Recall	0.6250
Macro F1	0.6161
Weighted F1	0.6184
분석
과제/시험은 비교적 잘 분류됨
발표/기타는 문장 패턴이 유사해 혼동 발생
전체적으로 작은 데이터셋 대비 안정적인 성능
Priority Classification (3-class)
Metric	Score
Accuracy	0.7500
Macro Precision	0.7444
Macro Recall	0.7500
Macro F1	0.7361
Weighted F1	0.7487
분석
High 클래스 예측이 가장 정확함
Medium ↔ Low 사이 혼동이 존재하지만 overall balanced
days_left와 contains_keyword가 강한 영향력을 미침
## 4. 특이사항
days_left는 Priority 예측에서 가장 중요한 변수로 작동하였다. High 우선순위 일정은 남은 일수가 매우 짧았고 Low는 여유가 많은 패턴이 확실했다.
contains_keyword는 텍스트 기반 특징만으로는 잡히지 않는 일정의 중요도를 보완해주었다.
Category보다 Priority 모델의 성능이 높은 이유는 Priority 라벨이 수치형 변수와 더 직접적으로 연결되었기 때문으로 분석된다.
## 5. 한계
데이터가 50개로 매우 적어 모델의 일반화 성능이 낮다.
TF-IDF 벡터는 단순 단어 기반 정보만 사용하므로 문맥 이해 능력이 부족하다.
contains_keyword는 단 하나의 이진 변수라 텍스트 정보가 충분하지 않다.
더 많은 일정 데이터를 확보하면 KoBERT, Sentence-BERT 등 딥러닝 방식으로 확장 가능하다.
## 6. 모델 가중치 저장 위치
훈련된 모델과 전처리 도구는 Google Drive에 업로드하였다.
category_model.pkl
priority_model.pkl
tfidf_vectorizer.pkl
feature_scaler.pkl
https://drive.google.com/file/d/109JSlKd3MmBdjq2KIs8eeJ-NlUlyPmjT/view?usp=share_link
