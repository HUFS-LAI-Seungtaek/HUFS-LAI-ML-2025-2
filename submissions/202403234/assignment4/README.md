# Assignment 4: Data Collection & Analysis
**Project Name:** 일정 자동 분류 및 우선순위 예측 모델  
**Author:** 202403234 양지현

---

## 1. 데이터 출처 및 수집 방식
본 프로젝트는 일정 문장을 기반으로 카테고리(과제/시험/발표/기타)와 우선순위(High/Medium/Low)를 자동 예측하는 모델을 만드는 것을 목표로 한다.  
실제 학기 중 작성했던 일정 텍스트 약 10건을 기반으로, 유사한 패턴을 반영해 총 50개의 학습용 일정을 구성하였다.

- **데이터 출처:** 실제 일정 + 패턴 기반 생성(Augmentation)
- **Notebook:** `data-analysis.ipynb`

---

## 2. 데이터 구성
데이터는 총 50개 일정으로 구성되며, 각 일정은 다음 6가지 feature로 표현된다.

| Feature | 설명 |
|--------|------|
| text | 사용자 일정 문장 |
| due_date | 마감일 (YYYY-MM-DD) |
| days_left | 오늘(2025-11-26) 기준 남은 일수 |
| contains_keyword | 긴급·중요 키워드 포함 여부(1/0) |
| category | 과제 / 시험 / 발표 / 기타 |
| priority | High / Medium / Low |

이 값들은 모두 머신러닝 모델 훈련 시 feature로 사용될 수 있도록 전처리된 형태로 저장하였다.

---

## 3. EDA 요약 결과

###  3-1. Target 변수 분포
- **카테고리(category)**: 과제·발표·기타가 고르게 분포되어 있어 특정 카테고리에 치우침이 없음.
- **우선순위(priority)**: High / Medium / Low가 비교적 균형적이어서 모델 학습에 적합함.

###  3-2. 카테고리별 우선순위 경향
Countplot 및 Cross-tabulation 분석 결과:

- 시험과 과제는 High 비율이 비교적 높게 나타남  
- 기타 일정은 Low 비율이 가장 큼  
- 발표는 대부분 Medium 중심으로 분포

→ 즉, 일정 종류에 따라 자연스러운 우선순위 패턴이 존재한다는 것을 확인함.

###  3-3. days_left 분석
- days_left의 평균은 약 9~10일  
- High 우선순위는 days_left가 상대적으로 낮음 (마감 임박)
- Low 우선순위는 days_left가 큰 경향

→ days_left는 우선순위 예측에 매우 유의미한 feature임.

###  3-4. contains_keyword 분석
- contains_keyword = 1 일 때 High 비율이 뚜렷하게 증가  
- contains_keyword = 0 일정은 대부분 Low 또는 Medium

→ “제출”, “발표”, “시험”, “준비” 등의 긴급 표현이 우선순위 판단에 중요한 역할을 함.

---

## 4. 시각화 결과 요약
Notebook에서 다음과 같은 시각화가 수행되었다.

- Category & Priority bar chart  
- Category vs Priority Countplot  
- days_left Distribution Histogram  
- contains_keyword Countplot  
- Priority vs days_left Boxplot

시각화 전반에서 **텍스트 특징 + 날짜 기반 변수의 조합이 우선순위 예측에 강한 설명력을 갖는 것**을 관찰할 수 있었다.

---

## 5. 결론 

EDA 결과 일정 데이터는 다음과 같은 특성을 가진다:

- category와 priority는 비교적 고르게 분포되어 학습용으로 적합함  
- days_left와 contains_keyword는 우선순위를 구분할 수 있는 핵심 feature  
- 일정 문장(text)은 표현 다양성이 높아 rule-based 방법만으로는 한계 존재