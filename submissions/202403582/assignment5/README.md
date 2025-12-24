# 5th Assignment: Model Training and Evaluation

---

# 1. 프로젝트 개요

**Project: 강의자료 자동 요약 및 핵심 포인트 추출기**

이 프로젝트는 Assignment 4에서 수집한 **컴퓨터 통신 카테고리의 한국어 대학 강의 전사 데이터(115,890 문장)** 를 기반으로  
강의자료에서 **핵심 문장(1) vs 비핵심 문장(0)** 을 자동으로 분류하는 모델을 구축하는 것이 목표이다.

핵심 목표는 다음과 같다:

- Weak supervision 기반 핵심문장 분류용 baseline 모델 구축
- TF-IDF + Logistic Regression 파이프라인을 재현 가능하게 구현
- 비교 실험(MLP 포함)을 통해 최종 모델 선택

---

# 2. 데이터셋 구성 및 전처리

## 2.1 전체 데이터셋

전체 데이터
- 총 문장 수: **115,890**
- 필드:  
  - `lecture_id`  
  - `major`  
  - `sentence`  
  - `clean_sentence`
- Weak label은 Lecture 단위 TF-IDF 중앙성 기반 자동 생성
  - `weak_train.csv`, `weak_valid.csv`, `weak_test.csv`

직접 라벨링 데이터
- 총 문장 수: **200**
- 필드:  
  - `sent_id`  
  - `sentence`  
  - `label`  
- 랜덤으로 200문장 추출 후, 직접 핵심 문장 여부 라벨링
  - `human_label.csv`

---

## 2.2 중복 제거

- 중복 약 3,000여 개 제거  
- 결과 저장: `comp_sentences_dedup.csv`

---

## 2.3 텍스트 전처리

Training/Infernce 전처리를 완전히 통일:

- 한글/영문/숫자 외 문자 제거
- 소문자화
- Stopwords 제거
- 공백 정규화
- 재결합: `comp_sentences_clean.csv` 에 새로운 `clean_sentence` 컬럼 추가

Stopwords 예시:
```
    # 1) filler / 말버릇
    "어", "음", "자", "뭐", "요", "네", "막", "그냥",
    "근데", "그죠", "거죠", "예",

    # 2) 지시어 (정보 없음)
    "이거", "이게", "이건", "그거", "그게",
    "저거", "요거", "요게", "얘는",

    # 3) 공손/형식적 표현
    "합니다", "되었습니다", "됩니다", "하겠습니다",
    "해주세요", "드릴", "보겠습니다", "할게요",
    "있습니다", "있어요", "있죠",

    # 4) 기능어 (기본 조사)
    "이", "그", "저", "을", "를", "은", "는", "에",
    "에서", "로", "것", "거", "건", "것들",
```

빈도 TOP 300 안에서

1) filler / 말버릇
2) 지시어 (정보 없음)
3) 공손/형식적 표현
4) 기능어 (기본 조사)

들을 선정.

---

# 3. Weak Label 생성 방식

Lecture 단위로 문장들을 묶어:

1) TF-IDF 벡터화  
2) 문장-문장 cosine similarity 계산  
3) 평균 유사도(centrality)를 점수로 사용  
4) 상위 15% (min 3, max 10) 문장을 **weak_label=1**

분포:

| Label | Count |
|-------|-------|
| 0 | 112,220 |
| 1 | 3,670 |

---
# 4. Train / Validation / Test Split

Weak label 기반 Stratified Split로 전체 데이터(115,890문장)를 다음과 같이 분리하였다.

| Dataset | 비율 | 크기 |
|---------|------|-------------|
| **Train** | 80% | 92,712 |
| **Validation** | 10% | 11,589 |
| **Test** | 10% | 11,589 |

- 분리 기준: `weak_label`
- 목적:
  - Validation → 모델 선택
  - Test → 학습/검증 과정에서 완전히 배제된 데이터로 일반화 성능 측정

---

# 5. Feature Engineering (TF-IDF)

모든 모델 학습 과정은 TF-IDF sparse vector를 입력으로 사용한다.

TF-IDF 설정:

```python
TfidfVectorizer(
    max_features=40000,
    ngram_range=(1, 2),
    min_df=5,
    max_df=0.9
)
```

- 약 **33,531 차원**의 sparse 벡터 생성
- 단어 단위 + bi-gram까지 포함
- Training 후 vectorizer 저장:
  - `tfidf_vectorizer.pkl`

---

# 6. 모델 아키텍처

본 프로젝트의 최종 모델은 **TF-IDF 기반 Bag-of-Words 벡터 표현 + Logistic Regression**으로 구성된다.

- **TF-IDF Vectorizer**  
  - max_features=40,000  
  - ngram_range=(1,2)  
  - min_df=5, max_df=0.9  
  - 약 33k 차원의 sparse vector 생성  

- **Logistic Regression Classifier**  
  - class_weight="balanced" (극단적 클래스 불균형 대응)  
  - max_iter=300  
  - decision boundary 기반 linear classifier  
  - 핵심문장(1)에 대한 recall 확보에 유리  

이 아키텍처는 대규모 강의 전사 데이터에서  
“핵심 단어/구 기반으로 독립적 문장 판단”이 필요한 본 과제 성격과 적합하다.


---

# 7. 모델 설계 및 학습

모델 후보는 크게 두 가지를 실험하였다.

---

## 7.1 Logistic Regression (최종 선택 모델)

하이퍼파라미터:

```
max_iter = 300  
class_weight = "balanced"  
n_jobs = -1
```

Validation 성능:

| Metric | Score |
|--------|--------|
| Accuracy | **0.8980** |
| Macro F1 | **0.6182** |
| Balanced Accuracy | **0.7839** |

장점:
- 클래스 불균형 상황에서 안정적인 성능
- minority class의 recall 확보

---

## 7.2 MLPClassifier

하이퍼파라미터:

```
hidden_layer_sizes = (64,)
activation = "relu"
solver = "adam"
batch_size = 1024
max_iter = 10
early_stopping = True
```

Oversampling 적용 (train set minority를 majority와 동일한 개수로 복제)

Validation 성능:

| Metric | Score |
|--------|--------|
| Accuracy | 0.9474 |
| Macro F1 | 0.6109 |
| Balanced Accuracy | 0.6223 |

문제점:
- Accuracy는 높지만 실제 핵심문장(1) recall이 매우 낮은 편  
- Logistic Regression 대비 **불균형에 취약**

---

## 모델 선택 이유

Validation 기준에서 다음 항목을 종합 평가:

- class imbalance 대응력  
- 핵심문장(1) recall 확보 중요성  
- 모델의 일관성과 안정성  
- 추론 속도 및 저장 용이성  

**최종 모델: Logistic Regression**

저장 파일:
```
final_model.pkl
```

---

# 8. 최종 Test 성능 (Weak Label 기준)

최종 선택된 Logistic Regression 모델을 Test Set(11,589문장)에 적용하였다.  
Test 데이터는 학습 및 검증에 *전혀 사용되지 않은* 완전 분리된 데이터이다.

---

## Test 성능 결과

```python
Accuracy:           0.8994
Balanced Accuracy:  0.7846
Macro F1:           0.6200
```

### Classification Report

| Class | Precision | Recall | F1-score | Support |
|-------|-----------|---------|-----------|----------|
| **0 (비핵심)** | 0.99 | 0.91 | 0.95 | 11222 |
| **1 (핵심)** | 0.19 | 0.66 | 0.29 | 367 |

**해석:**
- 모델은 핵심문장(1)을 *놓치지 않는 방향(recall)* 으로 동작  
- 단, weak label의 노이즈 특성상 precision은 낮게 나타남

---

# 9. Human Label(200개) 평가

Weak label은 자동 생성 요약이며 완벽하지 않기 때문에  
직접 라벨링한 **200개 Human Label**로 모델의 실제 적합성을 평가하였다.

---

## Human Test 결과

```python
Accuracy:           0.6900
Balanced Accuracy:  0.5558
Macro F1:           0.5244
```

### Classification Report

| Class | Precision | Recall | F1-score | Support |
|-------|-----------|---------|-----------|----------|
| **0 (비핵심)** | 0.69 | 0.96 | 0.81 | 133 |
| **1 (핵심)** | 0.67 | 0.15 | 0.24 | 67 |

---

## Weak vs Human 비교

| Dataset | Accuracy | Balanced Accuracy | Macro F1 |
|--------|----------|-------------------|-----------|
| **Weak Test** | 0.8994 | 0.7846 | 0.6200 |
| **Human Test** | 0.6900 | 0.5558 | 0.5244 |

---

## 왜 Human 성능이 낮을까?

1) **Weak label 자체의 노이즈**  
   - TF-IDF 중심성 기반 요약 → 문서 구조 중심  
   - Human은 "의미적 핵심"을 기준으로 판단  
   → 기준이 다소 다름

2) **클래스 비율 문제**  
   - Human label에서 핵심문장 1의 비율이 더 높음  
   - Weak label 분포와 달라 모델이 적응하지 못함

3) **모델의 본질적 한계**  
   - TF-IDF Logistic Regression은 맥락 이해가 불가  
   - BERT 기반 문장 임베딩 사용 시 개선 가능

---

# 10. 주요 분석 요약

- Weak 기준에서는 Macro F1이 **0.62**로 준수  
- Human 기준에서는 **0.52**로 하락  
- Weak → Human 전환 시 약 **10~13% 성능 감소**

**결론**:  
Weak supervision 기반 baseline model로는 의미적 핵심문장 추출의 한계가 존재하나,  
전처리/라벨링/Train/Inference 전체 파이프라인 구성에는 성공함.

---

# 11. 추론(Inference)

Inference Notebook(`inference.ipynb`)에서는 다음을 수행한다:

1) Google Drive에서 모델 & 벡터 로드  
2) Training과 동일한 전처리 적용  
3) 단일 문장 / 다중 문장 / 긴 텍스트 자동 분리 추론  
4) 핵심 문장만 필터링해 출력 (threshold 기반)

---

## 11.1 모델 및 벡터 로드

```python
model = joblib.load("final_model.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")
```

---

## 11.2 전처리 함수 (Training과 동일)

```python
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r"[^가-힣a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [t for t in text.split() if t not in stopwords]
    return " ".join(tokens)
```

추가로 Training과 완전히 동일한 stopwords 리스트를 사용하여  
추론 시 데이터 누락 문제를 방지하였다.

---

## 11.3 단일 문장 추론

```python
pred, prob = predict_sentence("이번 알고리즘의 핵심 아이디어는 ...")
```

예시 결과:

```
예측 라벨: 1 (확률: 0.1262)
```

---

## 11.4 여러 문장 리스트(batch) 추론

예시 입력:

```python
example_sentences = [
    "이번 알고리즘의 핵심 아이디어는 데이터를 반복적으로 갱신하는 것입니다.",
    "이 모델의 목적은 입력 문장에서 핵심 정보를 자동으로 추출하는 것입니다.",
    "여기까지 첫 번째 파트 설명이었습니다.",
    "혹시 질문 있으신가요?"
]
```

모델 출력:

| 문장 | 확률 | 예측 |
|------|--------|--------|
| 이번 알고리즘의 핵심 아이디어는… | **0.1262** | **1** |
| 이 모델의 목적은… | 0.0617 | 1 |
| 첫 번째 파트 설명… | 0.0329 | 0 |
| 혹시 질문 있으신가요? | 0.0080 | 0 |

---

## 11.5 긴 텍스트 자동 분리 + 핵심문장 추출 Demo

inference.ipynb에 구현 완료.

사용 흐름:

```
여러 문장을 한 번에 붙여넣으세요 (빈 줄 입력 시 종료)
↓
문장을 자동으로 split
↓
문장별 확률 계산
↓
threshold=0.06 이상만 핵심 문장으로 선택
```

### 데모 입력 예시  
(경사하강법 강의 텍스트 9문장 입력)

### 추출 결과 (4문장)

```
[1] 오늘은 경사하강법의 핵심 아이디어를 살펴보겠습니다. (0.2866)
[2] 학습률은 이동하는 보폭을 조절하는 중요한 하이퍼파라미터입니다. (0.0977)
[3] 학습률이 너무 크면 발산하고, 너무 작으면 속도가 매우 느려집니다. (0.0620)
[4] 우리가 원하는 것은 이 곡선의 최솟값을 찾는 것입니다. (0.2284)
```

---

## 11.6 모델의 추론 정확도 분석

| 구분 | 설명 |
|------|-------|
| 사람 기준 핵심문장 | 4개 |
| 모델이 맞춘 핵심문장 | 2개 |
| 일치율 | **약 50%** |

Weak label 기반 모델이므로 의미 기반 핵심문장과 완전히 일치하지는 않지만,  
기본적인 강의 요약 baseline으로 정상 동작함.

---

## 11.7 Threshold 설정 이유

기본 threshold=0.5 대신 **0.06**을 사용한 이유:

- 클래스 불균형 문제(1이 3%) → 확률이 극도로 낮게 나옴  
- recall 확보를 위해 threshold를 낮게 설정  
- Logistic Regression 확률 분포 분석 후 실험적으로 결정

--- 

# 12. 모델 가중치 및 프로젝트에 사용한 전체 데이터 저장 위치

학습이 완료된 최종 모델과 TF-IDF 벡터는 다음 파일로 저장되어 있다.

| 파일명 | 설명 |
|--------|------|
| `final_model.pkl` | Logistic Regression 모델 |
| `tfidf_vectorizer.pkl` | TF-IDF 벡터라이저 |

모든 데이터 저장 경로 (Google Drive)  
```
https://drive.google.com/drive/folders/18HSH9mSw2qBkw8q-ODQo7X6yus5DKQqw?usp=sharing
```
---

# 13. 프로젝트 한계 및 개선 방향

## 한계점

### 1) Weak label의 태생적 노이즈
- TF-IDF 중심성은 “문서 내에서 다른 문장과 비슷한 문장”을 선택함  
- 하지만 Human은 “의미적으로 중요한 문장”을 선택  
→ 두 기준이 다르다

### 2) 클래스 불균형 문제
- weak_label=1 비율이 **약 3.1%**  
- Logistic Regression이 recall은 확보하지만 precision은 낮음  
- Human 평가에서 성능 하락 원인이 됨

### 3) 모델의 구조적 한계
- TF-IDF Logistic Regression은 **문맥(context)** 을 이해할 수 없음  
- 단어 빈도 기반이라 의미적 핵심 파악에는 무리

---

## 개선 방향

### 1) 더 나은 Weak Label 방법
- BERT / Sentence-BERT로 문장 임베딩 후 centrality 추출

### 2) Human Label 확장
- 200개 → 500~2000개로 확장
- Semi-supervised learning 적용

### 3) Better Classifier 적용
- LightGBM / XGBoost
- RoBERTa / KoBERT 파인튜닝
- Ensemble 기반 threshold 최적화

---

# 14. 재현 (Reproducibility)

본 프로젝트의 학습 코드는 `training.ipynb`에 포함되어 있으며,  
학습 완료 후 생성된 `final_model.pkl`과 `tfidf_vectorizer.pkl`은 별도로 저장되어 있다.  

따라서 **Inference 단계만으로도 완전히 동일한 결과를 재현**할 수 있다.

(즉, inference 코드만으로도 모델 실제 실행 및 평가가 가능하다.)

아래 과정을 그대로 수행하면 모델을 재현할 수 있다.

### Step 1 — 모델 및 벡터 로드
```python
model = joblib.load("final_model.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")
```

### Step 2 — 전처리 함수 적용
Training과 동일한 규칙의 `preprocess()` 함수를 사용해 입력 문장을 정규화한다.

### Step 3 — TF-IDF 변환
```python
vec = tfidf.transform([clean_sentence])
```

### Step 4 — 예측 실행
```python
prob = model.predict_proba(vec)[0][1]
pred = 1 if prob >= threshold else 0
```

### Step 5 — 긴 텍스트 요약(선택)
문장 단위로 자동 분리한 뒤 batch 추론을 수행하여  
threshold 이상인 문장만 핵심 문장으로 필터링한다.

(inference.ipynb에서 체험 가능)

---

# 결론

본 프로젝트는 대규모 강의 전사 데이터 기반으로  
**Weak-supervision 방식의 핵심 문장 자동 추출 모델**을 성공적으로 구축하였다.

- Weak Test Macro F1: **0.62**  
- Human Test Macro F1: **0.52**  
- 전처리 → weak label 생성 → 학습 → 평가 → 추론까지  
  **완전한 파이프라인을 구성했다는 점**이 가장 중요한 성과다.

향후 BERT 기반 모델/더 정교한 weak label/더 큰 human label을 활용한다면  
훨씬 높은 품질의 강의 자동 요약이 가능할 것이다.

---

본 과제 수행 과정에서 training 및 시각화 코드 구현을 위해 ChatGPT를 활용하였으며, 최종 검토 및 작성은 직접 수행하였음을 명시합니다.
