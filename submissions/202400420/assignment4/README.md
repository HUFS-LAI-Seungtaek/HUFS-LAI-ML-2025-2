# Assignment 4: Data Collection and Analysis

## 1. 데이터 수집 방법
- 기존 계획: training data를 Amazon.de 또는 독일국립도서관 홈페이지에서 크롤링하고, validation 및 test data는 실제 오스트리아 도서관의 도서 목록을 사용하려고 했었지만 다음과 같은 문제가 발생하였음
    - 홈페이지 크롤링: 데이터 정제 문제, 저작권 문제 존재
    - training/validation/test dataset 중복 제거의 어려움: 오스트리아 도서관이 갖고 있는 도서 목록은 ISBN이 존재하지 않아 고유 번호 비교를 통한 중복 제거가 힘듦
    - 독일국립도서관 홈페이지 제공 독일어 도서 dataset(Bibliographic data of DNB): 11GB에 달하는 거대한 MARC21-xml파일로 데이터를 처리할 하드웨어 부족

- 수정 계획: Huggingface에 베를린시립도서관이 opensource로 제공하는 도서 목록 dataset을 이용하여 validation, train, test set을 모두 구성. https://huggingface.co/datasets/SBB/ARK-Metadata
    - **다국어**(영어, 독일어, 라틴어)가 혼용되어 있는 dataset으로 학습시 다국어 지원 pre-trained model필요
    - **실제 오스트리아 도서관의 도서 자원**도 독일어, 한국어, 영어가 혼용되어 있어 실제 환경과 유사한 data set으로 평가됨.
    - 실제 오스트리아 도서관과 dataset에서의 언어별 도서 비율이 유사한지는 확인되지 않음 (dataset에 한국어 도서는 존재하지 않음 확인됨)


## 2. 데이터 파싱 및 정제
1. 기본 제공 형식인 parquet파일을 csv파일로 파싱

2. 기존의 DDC 코드 기반 분야 분류 체계를 새로 정의한 4가지 문학, 어학, 역사, 사회과학(Literatur,Sprachwissenschaft, Geschichte,Sozialwissenschaften)으로 분류. 

3. 종교, 철학 등 광범위한 범위를 포함하고 있는 기타(Sonstiges) record는 모델의 혼란을 방지하고 학습 성능을 높이기 위하여 삭제함


## 3. 분석결과 요약
1. data 크기 및 품질: 데이터는 총 28525개 도서이며 결측치 없음.

2. 언어별 data 분포: **독일어 외 언어 비중이 55% 이상**으로 모든 언어 처리가 가능한 다국어 지원 pre-trained model 사용 필요(mBERT 등)

3. subject 분포: DDC 코드를 기반으로 4개의 분야로 매핑되어 매핑 오류는 희박할 것으로 예상. 구성 비율은 역사 33.24%, 문학31.51%, 사회과학26.95%, **어학8.29%**로 어학에서 클래스 불균형이 관찰됨. 클래스 가중치 부여 혹은 오버샘플링 고려 필요

4. subject에서 토크나이저 최대 입력 길이: 136문자 이상, 20단어 이상 (pre-trained Model의 최대 시퀀스 길이를 고려하여 해당 기준이상으로 토크나이저의 max_seq_length 설정 필요)


## 4. 기타
- 파이썬 코드 생성에 있어 Gemini의 도움을 받았음