# Assignment 4: Data Collection and Analysis

## 1. Project Overview
이 프로젝트는 **TOEFL Writing Task 1 (Integrated Writing)** 점수 향상을 위한 개인 분석 과제입니다.
나의 현재 에세이 수준(`My_Writing`)을 객관적으로 진단하고, 목표 점수(24점) 달성을 위해 보완해야 할 취약점을 파악하는 것을 목표로 합니다.

## 2. Dataset Description
- **File**: `data/toefl_assignment4.csv`
- **Size**: 60 samples (20 Topics × 3 Versions)
- **Labels**:
    - `My_Writing`: 제가 과거에 작성했던 초안입니다. 딱 20분내 쓰고 제출해서 문법 오류가 조금 있습니다.. (Target for improvement)
    - `ETS_Model`: ETS 평가 기준에 부합하는 만점 답안 (Benchmark)
    - `AI_Reference`: gemini를 활용해 생성한 답안

## 3. Analysis Method
Python(`pandas`, `seaborn`)을 활용하여 다음 항목을 분석했습니다. 분석하는 과정에서 코드는 gemini의 도움을 받았습니다.
1. **Text Quality**: 정규표현식(Regex)을 이용한 대소문자 오류(Capitalization) 및 전치사 오용(Preposition misuse) 패턴 탐지
2. **Correlation**: 에세이 길이(Word Count) 및 오류 빈도가 점수(Score)에 미치는 영향 분석

## 4. Key Findings
- **Score Gap**: 나의 현재 평균 점수는 **약 21점**으로, 목표 점수인 **24점**과 약 3점의 격차가 있습니다.
- **Error Analysis**: 20분 제한 시간 내 작성으로 인해 **문장 시작 시 소문자를 사용하는 실수(Capitalization Error)**가 가장 빈번하게 관찰되었습니다.
- **Correlation**: 분석 결과, 이러한 기초적인 문법 오류가 많을수록 점수가 하락하는 강한 상관관계가 확인되었습니다.

## 5. Conclusion & Action Plan
단순히 문장을 길게 쓰는 것보다 **기본적인 문법(대소문자, 전치사)**을 지키는 것이 점수 향상의 지름길임을 확인했습니다.

**[Future Plan]**
1. 에세이 작성 시 **마지막 2분**은 반드시 남겨두어 문장 첫 글자 대문자 여부를 검토합니다.
2. 단어 수를 ETS 모범 답안 수준으로 늘리고, 반복되는 단어를 줄이는 **Paraphrasing** 연습을 병행할 계획입니다.