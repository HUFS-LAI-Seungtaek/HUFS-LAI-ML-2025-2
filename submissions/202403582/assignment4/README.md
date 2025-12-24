# 4th Assignment: Data Collection and Analysis
본 문서는 Assignment 4 제출물의 README(분석 결과 요약본)입니다.  
이 프로젝트는 AI Hub “한국어 대학 강의 데이터”를 기반으로, 이후 Assignment 5에서 사용할  
**강의자료 자동 요약 및 핵심 포인트 추출기** 모델의 데이터 이해를 위한 탐색적 분석(EDA)을 수행했습니다.

---

# 1. 데이터 개요

## 1-1. 데이터 출처
- AI Hub: 한국어 대학 강의 데이터  
- 링크: https://www.aihub.or.kr/aihubdata/data/view.do?dataSetSn=71627

## 1-2. 사용한 데이터 범위
전체 TL.zip(라벨 데이터셋) 중 다음 조건에 해당하는 데이터만 사용함.

- TL.zip.part0 / TL.zip.part1 병합 → TL.zip 생성  
- TL.zip 내부에서 **eng/comp/** (컴퓨터통신) 카테고리만 선택적 추출  
- 각 JSON 파일에서 `06_transcription → 1_text`(문장 단위 전사 텍스트)만 수집  
- (lecture_id, major, sentence) 구조의 CSV로 정제하여 사용

## 1-3. 최종 데이터 파일
- 파일명: `comp_sentences.csv`  
- 크기: 약 **15MB**  
- 문장 수: **122,144개**  
- 고유 lecture_id: **367개**  
- 컬럼: `lecture_id`, `major`, `sentence`

---

# 2. 분석 환경
- 환경: Google Colab, Python 3  
- 주요 라이브러리: Pandas, Matplotlib, re, collections  
- Notebook 파일: `data-analysis.ipynb`

---

# 3. 수행한 EDA 요약

## (1) 데이터 로드 및 기본 정보 확인
- 데이터 크기: (122144, 3)  
- 모든 컬럼 object 타입  
- 강의별 문장 수 분포 다양

**의미**  
→ 데이터 규모·구조 파악을 통해 이후 모델 입력 크기, batch size, split 전략 등을 설계할 수 있음.

---

## (2) 결측치 및 중복 검사
- 결측치: **0건**  
- 중복 문장: **2,909건 (약 2.3%)**

**발견**  
→ 중복 문장이 존재하므로 모델 학습 시 특정 문장의 가중치가 과도해질 수 있음.  
→ Assignment 5에서 deduplication 또는 down-sampling 고려 필요.

---

## (3) 문장 길이 분석
- 평균: **46.9자**  
- 중앙값: **36자**  
- 최소: **1자**  
- 최대: **567자**  
- 75 percentile: **62자**

**해석**  
→ max_length는 128~256 token 수준으로 설정해도 적절  
→ 극단적 길이(outlier) 존재 → truncate 기준 필요

<img width="589" height="455" alt="image" src="https://github.com/user-attachments/assets/098337ff-04c0-4098-b09f-9a45774ba001" />

- 문장 길이 히스토그램

---

## (4) 강의(lecture_id) 단위 분포 분석
describe() 기반 강의별 문장 수 통계:

- lecture_id 총 **367개**  
- 최소: **76문장**  
- 최대: **1,433문장**  
- 평균: **332.8문장**

이는 **강의 간 문장 수가 크게 차이나는 불균형 구조**를 나타냄.

**발견 및 영향**  
→ 특정 강의가 데이터의 상당 부분을 차지  
→ 모델이 특정 강의 스타일에 편향될 위험  
→ stratified split, down/oversampling 고려 필요

<img width="549" height="374" alt="image" src="https://github.com/user-attachments/assets/a71be173-5106-4990-933b-0b2ac60595a7" />

- 전체 boxplot

<img width="841" height="470" alt="image" src="https://github.com/user-attachments/assets/4b547aab-310e-47e3-9951-9ef3a8cfd29d" />

- lecture별 문장 수 히스토그램

---

## (5) 자주 등장하는 단어 분석
정규식 기반 tokenizer로 한글/영문/숫자 토큰화 후 빈도 계산.

### Top 20 단어 (빈도수 포함)
1. 이 — 19,574  
2. 그래서 — 15,183  
3. 이제 — 14,305  
4. 어 — 13,986  
5. 자 — 12,975  
6. 이렇게 — 12,867  
7. 그 — 12,844  
8. 우리가 — 11,534  
9. 수 — 10,540  
10. 이런 — 10,205  
11. 있는 — 9,668  
12. 뭐 — 9,353  
13. 하는 — 5,731  
14. 때 — 5,726  
15. 지금 — 5,606  
16. 그리고 — 5,503  
17. 있습니다 — 5,445  
18. 요 — 5,327  
19. 그러면 — 5,249  
20. 어떤 — 4,876  

**발견 및 의미**
- filler words 비중 높음 → stopword 처리 필요  
- 전문 용어("신호", "필터", "주파수")도 등장 → 도메인 반영 양호  
- 전처리 시 구어체 제거 또는 중요도 조정이 효과적

---

# 4. 데이터 품질 문제 요약

## (1) 중복 문장 존재
→ 모델 편향 발생 가능  
→ deduplication 필요

## (2) 강의 간 문장 수 불균형 (76 ~ 1433문장)
→ 강의 간 문장 수 차이가 크므로
→ train/validation split 시 강의 단위 불균형을 고려해야 함

## (3) filler word 과다  
→ 불용어 리스트 커스터마이징 필요

## (4) 긴 문장 outlier 존재  
→ max_length 초과 위험  
→ truncate/분할 전략 필요

---

# 5. 향후 모델링에의 영향 (Assignment 5 대비)

EDA 결과는 다음 의사결정에 직접 활용됨:

1. **Tokenizer max_length 설정**  
   → 길이 통계 기반으로 128~256 범위 적절  
2. **데이터 샘플링 전략**  
   → 강의 간 불균형 해소 필요  
3. **텍스트 전처리 규칙 설계**  
   → filler words 제거, 중복 제거, 긴 문장 처리  
4. **학습/검증 Split 전략**  
   → lecture_id 기준 stratified split 가능  

---

# 6. 결론

본 EDA는 향후 “강의자료 자동 요약 및 핵심 포인트 추출기” 모델 구축을 위한  
데이터 품질, 구조, 분포, 전처리 방향성을 명확히 파악하는 과정이다.

- 문장 수 충분  
- 결측/중복 적음  
- 도메인 용어 반영  
- 전처리 난이도 낮음  

이 데이터는 NLP 모델링에 매우 적합한 고품질 데이터이며,  
Assignment 5에서 효과적인 모델 설계를 가능하게 한다.
