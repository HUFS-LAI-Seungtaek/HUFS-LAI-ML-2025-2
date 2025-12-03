# CS_Insight: News Topic Classifier for CS Majors

본 프로젝트는 텍스트의 맥락을 분석하여 **CS 전공자에게 유의미한 기술 정보(CS_Insight)** 를 능동적으로 필터링하는 머신러닝 분류 모델입니다.

## 1. 모델 아키텍처 (Model Architecture)

본 프로젝트는 단순한 키워드 매칭을 넘어, 텍스트 내의 **단어 간 상호작용(Feature Interactions)** 을 학습하여 정교한 분류를 수행하기 위해 **TF-IDF 임베딩과 다층 퍼셉트론(MLP)을 결합한 파이프라인**을 설계하였습니다. 
### 1.1 모델 선정 이유 
단순 선형 모델(Logistic Regression 등) 대신 **MLP(Neural Network)** 를 채택한 이유는 다음과 같습니다. 

1. **비선형적 문맥 학습 (Non-linear Context Learning):** 자연어 데이터는 단어 하나가 독립적으로 작용하기보다, 단어 간의 **조합(Combination)** 이 의미를 결정합니다. (예: 'Apple'은 'Pie'와 쓰이면 음식, 'Chip'과 쓰이면 기술) 선형 모델은 이러한 특징을 잡아내기 어렵지만, MLP는 **은닉층(Hidden Layer)** 을 통해 단어 간의 복잡한 비선형 관계를 학습할 수 있습니다. 

2. **정교한 결정 경계 (Decision Boundary):**  `Technology`와 `CS_Insight`는 의미적으로 매우 인접해 있어 단순한 선형 경계로 구분하기 어렵습니다. MLP의 다층 구조는 이러한 모호한 경계면을 더 유연하게 분리해냅니다. 

3. **학습 과정의 추적 (Monitoring):**  반복 학습(Epoch)에 따른 **Loss Curve**를 시각화하여, 모델의 수렴 과정과 과적합(Overfitting) 시점을 명확하게 파악하고 제어하기 위함입니다.
### 1.2 파이프라인 구조 (Pipeline Structure)

전처리부터 분류까지 하나의 흐름으로 처리되도록 `sklearn.pipeline`을 사용하였습니다.

1. **입력 (Input):** 뉴스 헤드라인 (Text)
    
2. **특성 추출 (Feature Extraction): `TfidfVectorizer`**
    
    - **Max Features:** 3000 (상위 3,000개 단어만 사용하여 차원 축소)
        
    - **Stopwords:** English (불용어 제거로 노이즈 감소)
        
3. **분류기 (Classifier): `MLPClassifier` (Multi-Layer Perceptron)**
    
    - **Hidden Layers:** 2개 층 `(128, 64)` - 복잡한 텍스트 패턴 학습을 위한 깊이 확보
        
    - **Activation:** `ReLU` - 비선형성 확보
        
    - **Optimizer:** `Adam` - 효율적인 가중치 업데이트
        
    - **Training:** Max 200 Epochs (with **Early Stopping**)
        

### 1.3 학습 전략 (Training Strategy)

- **Stratified Split:** 데이터 불균형을 고려하여 Train/Validation/Test 분할 시 각 클래스의 비율을 일정하게 유지하였습니다.
    
- **Loss Monitoring:** 학습 과정의 투명성을 위해 Epoch별 Loss Curve를 추적하여 과적합(Overfitting) 발생 지점을 모니터링했습니다.
    

## 2. 평가 지표 및 성능 결과 (Evaluation)

### 2.1 평가 프로토콜 (Protocol)

- **평가 데이터:** 학습에 관여하지 않은 **Test Set (전체의 20%)** 에서만 최종 평가를 수행하였습니다.
    
- **핵심 지표 선정:** **Macro F1-Score**
    
    - **선정 이유:** 데이터셋 내 `Economy` 클래스는 많고 `CS_Insight`는 적은 **클래스 불균형(Class Imbalance)** 문제가 존재합니다. 단순 정확도(Accuracy)는 다수 클래스에 편향될 수 있으므로, 모든 클래스의 성능을 동등하게 평균 내는 Macro F1-Score를 메인 지표로 삼았습니다.
        

### 2.2 정량적 성능 결과 (Performance Results)

- **Overall Accuracy:** 57.32%
    
- **Macro F1-Score:** **0.5957**
    

|Class|Precision|Recall|F1-Score|비고|
|---|---|---|---|---|
|**CS_Insight**|**0.89**|**0.73**|**0.80**|**Target Class (최고 성능)**|
|Economy|0.42|0.40|0.41|-|
|Politics|0.54|0.58|0.56|-|
|Society|0.56|0.61|0.58|-|
|Technology|0.62|0.62|0.62|-|

## 3. 특이사항 및 한계점 분석 (Analysis & Limitations)

테스트 데이터셋(82개 샘플)을 대상으로 모델의 일반화 성능을 평가한 결과, 다음과 같은 유의미한 인사이트를 도출하였습니다.

### 3.1 정량적 평가 결과 (Quantitative Results)

- **Overall Accuracy:** 57.32%
    
- **Macro F1-Score:** **0.5957** (클래스 불균형을 고려한 핵심 지표)
    

### 3.2 핵심 성과: 타겟 클래스(`CS_Insight`)의 고성능 달성

본 프로젝트의 최우선 목표인 **'CS 전공자를 위한 뉴스 필터링'** 성능은 매우 우수하게 나타났습니다.

- **F1-Score:** **0.80** (전체 카테고리 중 1위)
    
- **Precision (정밀도):** **0.89**
    
    - **의미:** 모델이 *"이것은 CS 뉴스다"*  라고 예측했을 때, **실제로 정답일 확률이 89%** 에 달함을 의미합니다.
        
    - **결론:** 사용자(CS 전공자)에게 불필요한 노이즈(오분류된 뉴스)를 최소화하고, 신뢰도 높은 정보를 제공할 수 있음을 입증하였습니다.
        

### 3.3 한계점 및 원인 분석 (Limitations)

반면, `Economy`(0.41)나 `Politics`(0.56) 등 일반 카테고리의 성능은 상대적으로 낮게 측정되었습니다.

1. **도메인 중첩 (Semantic Overlap):** 'Policy(정책)', 'Market(시장)', 'Global(국제)'과 같은 단어들은 정치, 경제, 사회 뉴스에 공통적으로 빈번하게 등장하여 모델의 혼동을 유발했을 것으로 생각합니다.
    
2. **데이터 절대량 부족 (Small Data):** 약 400여 개의 전체 데이터 중, 학습에 사용된 데이터는 약 300여 개에 불과합니다. 이는 일반적인 뉴스 카테고리의 광범위한 어휘(Vocabulary)를 모두 학습하기에는 부족한 양이라고 생각합니다.
    

### 4.4 종합 결론 (Conclusion)

비록 전체 정확도(Accuracy)는 57% 수준이나, **프로젝트의 핵심 타겟인 `CS_Insight` 분류에 성공**했다는 점에서 모델의 효용성은 충분하다고 판단됩니다. 
향후 **RSS 수집 자동화(Automation)** 를 통해 일일 데이터를 지속적으로 누적(Accumulate)한다면, 일반 카테고리의 결정 경계 또한 명확해져 전체적인 성능(Macro F1)이 크게 향상될 것으로 기대됩니다.


## 4. 모델 가중치 저장 위치 (Model Weights)

학습된 모델 파일(`news_classifier_model.pkl`)은 접근성을 위해 Google Drive에 업로드되어 있습니다.

- **저장 방식:** 모델 파이프라인(Model)과 라벨 인코더(Encoder)를 Dictionary 형태로 묶어 저장함.
    
- **접근 방법:** `inference.ipynb` 실행 시 **자동으로 다운로드**되도록 코드가 구현되어 있습니다.
    
- **수동 다운로드 링크:**
    
    - https://drive.google.com/file/d/138_2NXbeGm2wCCaOVeDd12c7hGrm7alE/view?usp=sharing

### ※ Acknowledgment

본 과제 수행 과정에서 데이터 크롤링 및 시각화 코드 구현, 초기 모델링 아이디어 도출을 위해 **Google Gemini**를 활용하였으며, 생성된 코드를 기반으로 프로젝트 의도에 맞게 재구성 및 디버깅을 진행하였습니다.