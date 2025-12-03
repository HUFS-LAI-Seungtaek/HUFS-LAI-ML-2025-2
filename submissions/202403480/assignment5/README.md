# Assignment 5: Model Training & Evaluation 

## 모델 아키텍쳐
전체 파이프라인 구성
1. 소문자 변환
2. 특수문자/기호 제거
3. 불용어 제거
4. 가격(숫자) 추출 및 feature 활용
5. 한글/영문/숫자만 남기기
-문서 벡터화
1. TfidfVectorizer
2. uni-gram + bi-gram
3. max_features = 30,000
4. min_df = 2
5. 사용자 정의 stop_words 적용
-학습한 후보 모델
1. Logistic Regression
2. Linear SVM
3. Multinomial Naive Bayes
4. Random Forest
-최종 선택 모델
1. Logistic Regression (class_weight='balanced')
-이유
1. 데이터 수가 매우 적은 환경에 강함
2. 불균형 데이터에 안정적
3. inference 속도가 빠르고 재현이 쉬움
-하이퍼파라미터
1. GridSearchCV
2. C = [0.5, 1, 2]
3. penalty = 'l2'
4. max_iter = 500

## 평가 지표 및 성능 결과
-데이터셋 구성
1. 총 샘플 수: 27개
2. 데이터 분할:
3. Train: 18
4. Validation: 4
5. Test: 5
-모델별 Validation 성능 비교
(모델 / Validation Accuracy)
1. Logistic Regression / 1.0000
2. Linear SVM / 1.0000
3. Naive Bayes / 1.0000
4. Random Forest / 1.0000
➡ 최종 선택 모델: Logistic Regression
-Test Set 평가 결과 (최종 모델)
1. Confusion Matrix (Test) - 식비: 3개 모두 정확히 예측, 편의점/마트: 2개 모두 정확히 예측
➡ 모든 테스트 샘플 100% 정확히 분류
-Cross-Validation (5-Fold)
각 Fold Accuracy:
1. Fold 1: 1.0000
2. Fold 2: 1.0000
3. Fold 3: 1.0000
4. Fold 4: 0.8000
5. Fold 5: 0.8000
➡ 5-Fold 평균 Accuracy: 0.92 (데이터가 적어 Fold 4, 5에서 조금 떨어진 모습이 나타남)
-Inference 결과 예시 (실제 예측 문장 5개)
(입력 문장 → 예측 카테고리)
1. 알촌에서 식비 8300원 결제 → 식비
2. CU에서 2400원 편의점 결제 → 편의점/마트
3. 매머드익스프레스에서 카페 3400원 → 카페
4. 동경규동에서 식비 9000원 사용 → 식비
5. 죠스아이스크림 1500원 구매 → 편의점/마트
➡ 추론 코드 정상 작동

## 모델 가중치 저장 위치
-Google Drive 저장 경로
1. 모델 가중치(model.pkl) - /content/drive/MyDrive/receipt_model/model.pkl
2. 벡터라이저(vectorizer.pkl) - /content/drive/MyDrive/receipt_model/vectorizer.pkl
3. 구글 드라이브 링크 : https://drive.google.com/drive/folders/1rLx0oEWyW9YmSxm6n9CmpoPZwhgrCSm5?usp=sharing

## 학습/평가 과정에서의 특이사항 및 한계
-데이터셋 크기가 매우 작음 (총 27개)
1. 원본 수집 데이터가 27개로 매우 적어 충분한 일반화가 어려움
2. 모든 모델(Logistic Regression / SVM / Naive Bayes / RandomForest)이 validation accuracy가 1.0으로 나타났는데, 이는 실제로는 과적합(overfitting) 가능성이 큼
3. Train/Test가 매우 작기 때문에 성능을 객관적으로 판단하기 어려움
-특정 클래스의 데이터 수가 균형적이지 않음
1. 식비(=식사 관련) 데이터가 많고, 카페 / 편의점 데이터는 상대적으로 적은 등 데이터 개수 불균형으로 이로 인해 stratified split 과정에서 오류가 발생함.
2. 클래스 불균형 때문에 특정 fold에서 cross-validation accuracy가 낮게 나오는 현상 있음
-OCR 텍스트의 품질이 고르지 않음
1. OCR 결과가 정확하지 않은 경우가 상당히 많았음. 철자 이상, 띄어쓰기 이상, 업체명 오인식 등 존재. 결국 많은 부분을 수동으로 정제하여 CSV를 만드는 과정이 필요했음.
2. 더 좋은 데이터 품질을 위해 OCR 모델 개선 또는 이미지 전처리 필요하다고 생각함.
-모델 비교 실험은 유의미하나, 데이터가 적어 차이를 설명하기 어려움
1. Logistic Regression / SVM / Naive Bayes / RandomForest 모두 Validation Accuracy = 1.0이 나옴. 이는 실제로는 모델 간 차이가 거의 없다는 뜻이 아니라 데이터가 너무 적어서 차이를 드러낼 여지가 없음.
2. Cross-validation에서도 fold에 따라 오차가 크게 변동
