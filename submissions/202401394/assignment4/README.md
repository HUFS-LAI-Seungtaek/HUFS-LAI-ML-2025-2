# Assignment 4: Data Collection & Analysis
- **Project Name:** 맞춤형 팀플 및 과제 부담 최소화 강의 필터링 시스템 
- **Author:** 202401394 박의진

---

## 1. 데이터 출처 및 수집 방식
본 프로젝트는 한국외국어대학교 25-1~25-2 교양(83), 전공선택(15), 기초(2) 강의의 강의계획서 텍스트를 `data-extract.ipynb`를 이용해 추출하여,
팀플과 과제가 상대적으로 많은 강의를 텍스트 분류를 통해 점수를 매기고, 필터링하는 시스템이다.
가장 최근 시점 데이터인 25-1, 25-2 한국외국어대학교 교양, 전공선택, 기초 강의 계획서 100건의 데이터로 진행하였고, 
수집은 크롤링이 아닌 실제 pdf 다운로드 후 csv로 필요한 CourseTitle,	Classification 등을 추출하였다

- 데이터 출처: 한국외국어대학교 종합정보시스템 강의계획서
- Notebook: `data-analysis.ipynb`

## 1-1. 최종 데이터 파일
- 파일명: `Hufs_Syllabus_Data.csv`  
- 크기: 약 **115KB**  
- 강의 수 : 100개 (전공 15, 교양 83, 기초 2)
- 컬럼: `CourseTitle`, `Classification`, `CourseDescription`, 'AssignmentScore', 'EtcScore', 'TeachingMethods', 'OtherNotes'

---

## 2. 데이터 구성
데이터는 총 100개의 강의계획서에서 추출한 텍스트로 구성되며, csv의 텍스트는 다음 7가지 feature로 표현된다.

| Feature | 설명 |
|--------|------|
| CourseTitle | 강의 교과명 |
| Classification | 전공(선택)/교양/기초 |
| CourseDescription | 교과목개요 및 학습목표(팀플 여부 판단을 위함) |
| AssignmentScore | 학습평가방식(100) 중 과제 비율 |
| EtcScore | 학습평가방식(100) 중 발표 및 토론, 프로젝트, 수업참여도 비율 |
| TeachingMethods | 수업운영방식(과제, 팀플 여부 판단을 위함) |
| OtherNotes | 기타안내 및 유의사항(위 목적과 동일) |

CourseTitle과 Classification은 필터링 시스템의 마지막 필터링을 위해 추출한 feature이며,
AssignmentScore, EtcScore는 학습평가방식에서 공식적으로 언급된 feature로 머신러닝 때에 바로 사용가능하다.
CourseDescription, TeachingMethods, OtherNotes에선 긴 길이의 문장형 텍스트로 추출하였기 때문에, 추후 전처리 과정에서
팀플, 과제의 빈도를 파악할 수 있는 텍스트를 분류 기준으로 점수를 선정할 계획입니다.

---

### 2-1. 분석 환경
- 환경: Google Colab, Python 3  
- 주요 라이브러리: Pandas, Matplotlib, numpy, seaborn, koreanize_matplotlib
- Notebook 파일: `data-analysis.ipynb`
- **데이터 분석**은 gemini 3 pro 모델을 활용하여 ipynb 코드를 생성해, 분석을 진행하였습니다.
---

## 3. EDA 요약 결과
### 3-1. Target 변수 분포 (배점 구조 분석)
프로젝트 핵심인, '과제 부담'과 '팀플 유무'를 파악하기 위해 `AssignmentScore`와 `EtcScore`의 분포를 분석했습니다.
* `AssignmentScore`: 대체로 **10% ~ 30%** 구간에 집중되어 있으며,
  0인 강의도 일부 존재하나,대부분 과제가 포함되어 있습니다.
* `EtcScore`:**0인 강의가 많지만(팀플이 없을 확률 높음)**, 점수가 존재하는 경우 10%~20% 구간에 분포하며
최대 50%까지 할당된 강의도 있어 팀플 비중의 편차가 있음을 보입니다.
