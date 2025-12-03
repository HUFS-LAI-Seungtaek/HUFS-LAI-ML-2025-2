# Assignment 5: Model Training & Evaluation 

## 모델 아키텍쳐
파이프라인 개요
- 입력: OCR 결과 텍스트(ocr_text)
- 카테고리 분류
1. 전처리: 소문자화, 숫자/기호 정리, 불용어 최소 제거
2. 특징: TF-IDF(uni+bi-gram, max_features=30k, min_df=2)
3. 분류기: Logistic Regression (GridSearchCV, C∈{0.5,1,2}, class_weight='balanced')
- 금액 추출
1. 정규식으로 모든 숫자 후보 탐색(쉼표/원 표기 포함)
2. 후보 주변의 키워드 거리(합계/총액/받은금액/결제/원 등), 숫자 길이/포맷/행 위치 등을 특징으로 생성
3. LightGBM Ranker로 후보를 점수화해 Top-1 선택
4. (Fail-safe) 랭커 미동작 시 ‘합계/받은금액’ 키워드 가장 근접 숫자 채택
- 일자 추출
1. 정규식으로 날짜 후보(YYYY[-./ ]?MM[-./ ]?DD, YY.MM.DD, MM/DD) 수집
2. ‘승인/결제/일시’ 등 트리거 키워드 근접도와 포맷 가중치로 스코어링 → 최고 점수 1개 선택
3. 연도 누락 시 문서 내 연도 힌트/현재 연도로 보정, 최종 포맷은 YYYY-MM-DD

## 평가 지표 및 성능 결과
- 카테고리: 다수/소수 간 불균형에서 Macro-F1로 모니터링. 편의점↔식비, 카페↔식비 등 의미 유사군 혼동이 주원인.
- 금액: 합계/받은금액/공급가액/부가세가 공존할 때도 랭커가 대부분 올바른 합계를 선택.
- 일자: YY.MM.DD / MM/DD와 같이 연도가 생략된 영수증에서 오차가 주로 발생.

## 모델 가중치 저장 위치
- 레포 포함(소형, <10MB):
submissions/202403480/assignment5/models/
├─ tfidf_vectorizer.joblib
├─ clf_category_lr.joblib
├─ lgbm_amount_ranker.txt
└─ date_rules.json
- Google Drive 폴더 링크: ~~~~~~~

## 학습/평가 과정에서의 특이사항 및 한계


카테고리: TF-IDF + LR ↔ SBERT/KoBERT 대체 실험,

금액: 랭커 특징 강화 + 규칙 앙상블,

일자: 레이아웃 단서 추가 및 파서 커버리지 확장.
