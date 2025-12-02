# 데이터 분석 및 발견 사항
## 데이터 구성
- 총 65,927개의 동사들로 구성되어 있다.
- 데이터는 verb(변형된 형태의 동사), mood(법), tense(시제), person(인칭,수) 총 4개의 주요 속성들로 구성되어 있다.
- 결측값은 존재하지 않는다.
## 라벨 간 특징
- 라벨 간 교차분포를 확인해볼 때 어떠한 특정 조합에만 데이터가 몰려있지 않고 발생할 수 있는 모든 경우에 데이터가 잘 분포되어 있음을 확인할 수 있다.

- Mood(법)
  - indicative(직설법), subjunctive(접속법), imperative(명령법) 세 종류가 있다.
  - indicative가 가장 많고 imperative가 가장 적다.

- Tense(시제)
  - present(현재), present_perfect(현재 완료), pluperfect(과거 완료), future_perfect(미래 완료), future(미래), imperfect(불완료 과거), preterite_anterior(전과거), conditional(가정미래), conditional_perfect(가정미래 완료), preterite(과거) 총 10개의 시제가 있다.
  - 10개의 시제 중 present가 가장 많다.

- Person(인칭, 수)
  - 1sg, 2sg, 3sg, 1pl, 2pl, 3pl 6가지의 인칭이 존재한다.
  - 데이터가 고르게 분포되어 있지만 1인칭이 비교적 적다.
## 동사 길이 및 라벨 간 관계
- 동사 길이
  - 대부분의 동사 변화형이 5~10글자 내에 분포되어 있다.
  - 특이값은 거의 없다.

- 라벨 간 관계
  - 상관계수를 볼 때 verb_len과 mood_id 사이에서 법에 따라 동사의 길이가 약간 달라지는 경향이 있음을 볼 수 있다.
  - 대부분의 속성들이 서로 상관관계가 매우 낮다. 이를 통해 각 라벨들이 서로 독립적임을 알 수 있다.
## 데이터 품질 문제 및 개선점
- Indicative에 비해 Imperative의 데이터 수가 부족하여 Imperative 시제의 학습이 잘 이루어지지 않을 수 있다.
- 필요 시 Imperative의 데이터를 더 수집할 예정이다.
