## 1. 데이터 개요 (Data Overview)
- **데이터 소스**: Python `FastF1` 라이브러리 (Official F1 Data & Ergast API)
- **CSV**: `Year, Round	GrandPrix	SC_Count, VSC_Count	Red_Flag_Count, Chaos_Score	Lead_Changes, Gap_Std_Dev	Position_Gains_Total`
- **수집 기간**: 2021시즌 ~ 2025시즌 (총 5개년)
- **데이터 크기**: 5.37KB , 총 122개의 경기(레이스) 데이터 (결측치 없음)

## 2. 주요 변수 설명 (Feature Description)
단순 기록 데이터가 아닌, 경기의 역동성을 수치화하기 위해 파생 변수(Feature Engineering)를 생성했습니다.

| 변수명 | 설명 | 데이터 타입 |
|---|---|---|
| `Chaos_Score` | SC(3점), VSC(1점), Red Flag(5점) 발생 횟수에 가중치를 둔 혼란도 지수 | Int (Derived) |
| `Position_Gains_Total` | 드라이버들의 순위 상승(Grid vs Finish) 횟수 총합 (추월 활성도) | Int (Derived) |
| `Lead_Changes` | 경기 중 선두 드라이버가 교체된 횟수 (우승 경쟁 치열함) | Int |
| `Gap_Std_Dev` | 1위와 2위 간 시간 격차의 표준편차 (낮을수록 치열한 접전) | Float |

## 3. 데이터 분석 결과 (EDA Insights)

### 3.1 상관관계 분석 (Correlation)
<img width="936" height="825" alt="image" src="https://github.com/user-attachments/assets/0444f5f4-e4eb-4e7e-8ae3-3fb7de77a2cd" />

- **Chaos와 Action의 관계**: `Chaos_Score`와 `Position_Gains_Total` 간에는 **약한 양의 상관관계**(0.22)가 확인되었습니다.
  - **해석**: 사고(Chaos)가 발생하면 차량 간격이 줄어들어 변수가 생기지만, 이것이 무조건적인 대량 추월로 이어지지는 않습니다. 오히려 세이프티 카 상황에서의 랩 소모가 추월 기회를 제한할 수도 있음을 시사합니다.
- **선두 경쟁의 독립성**: `Lead_Changes`는 다른 변수들과 상관관계가 낮아, 중위권의 사고 여부와 무관하게 최상위권의 퍼포먼스에 의해 결정되는 독립적인 재미 요소임이 확인되었습니다.

### 3.2 연도별 트렌드 (Seasonality)
<img width="1006" height="558" alt="image" src="https://github.com/user-attachments/assets/f187dd98-1935-44c4-90f5-4ead56448a97" />

- **2021년 (High Variance)**: 타이틀 경쟁이 가장 치열했던 해로, 혼란도(Chaos)의 변동폭(IQR)이 가장 크고 평균 점수도 높았습니다.
- **2023년 (Extreme Outlier)**: 레드불의 독주로 전반적인 경기는 안정적(Median 3.0)이었으나, **호주 GP**(Chaos Score 31)라는 역대급 혼란 경기가 발생하여 데이터의 최대치(Max)를 기록했습니다.
- **2024년 (Clean Racing)**: 맥라렌과 메르세데스의 컨스트럭터 경쟁이 치열했음에도 혼란도 중앙값은 **2.0**(최저)을 기록했습니다. 이는 사고보다는 순수한 전략과 레이스 페이스로 승부가 갈린 **수준 높은 시즌**이었음을 보여줍니다.

### 3.3 서킷별 특성 (Circuit Analysis)
<img width="1176" height="558" alt="image" src="https://github.com/user-attachments/assets/b4f81907-5118-4b5f-8bf3-f3d1d48759d6" />

- **러시아 GP**: 데이터상 추월 지수가 1위로 나타났으나, 이는 2021년 우천 상황(Rain)에서 단 1회 개최된 데이터이므로 통계적 대표성이 부족함(Sample Size Bias)을 확인했습니다.
- **라스베이거스 GP**: 2023~2025년 3회 개최 데이터에서 꾸준히 상위권의 추월 지수를 기록하여, 긴 직선 구간을 활용한 '검증된 액션 서킷'임을 입증했습니다.

## 4. 데이터의 한계 및 향후 계획 (Limitations & Future Work)

### 4.1 데이터의 한계 (Limitations)

1.  **지표의 과소평가** (Net vs Gross Overtakes)
    - **한계**: 현재 사용된 `Position_Gains` 변수는 출발(Grid)과 도착(Finish) 순위만을 비교한 'Net 지표'입니다. 레이스 도중 드라이버끼리 수차례 순위를 주고받은 치열한 경기나, 피트 스톱 전략으로 인한 일시적 순위 변동(Gross Overtakes)은 반영되지 않습니다.
    - **영향**: 실제로는 추월이 60회 일어난 경기라도, 최종 순위 변동이 적다면 데이터상으로는 '지루한 경기'로 과소평가될 위험이 있습니다. (예: 2024 라스베이거스 GP 실제 추월 약 60회 vs 데이터 집계 35회)

2.  **정성적 데이터의 부재**(Contextual Data Missing)
    - **한계**: 현재 모델은 `SC_Count`(횟수)는 알 수 있지만, **누가, 언제, 왜** 사고를 냈는지는 알지 못합니다.
    - **영향**: 챔피언십 경쟁자끼리의 충돌(높은 도파민)과 하위권의 단순 차량 고장(낮은 도파민)을 동일한 '1회'로 처리하므로, 팬들이 느끼는 드라마틱함을 완벽하게 수치화하기엔 한계가 있습니다.

3.  **표본의 부족 및 불균형**(Small & Imbalanced Sample)
    - **한계**: 5년 치 전수 데이터를 수집했음에도 총 데이터는 약 100~120개로, 머신러닝(특히 딥러닝)을 적용하기에는 표본이 적은 편입니다. 특히 라스베이거스 등 **신규 서킷**은 데이터가 2~3개뿐이라 통계적 유의성을 확보하기 어렵습니다.

### 4.2 향후 계획 (Assignment 5)
- **Feature Selection**: 다중공선성 문제를 피하기 위해 개별 사고 횟수(`SC`, `RedFlag`) 대신 통합 변수인 `Chaos_Score`를 사용할 예정입다.
- **Model Strategy**: 데이터의 시계열적 특성(연도별 트렌드)과 서킷별 편차를 반영할 수 있는 **Random Forest Regressor** 모델을 사용하여, 실제 팬들의 평점(Excitement Rating)을 예측하는 모델을 학습시킬 예정입니다.

## 5. 결론 (Conclusion)

1.  **데이터 파이프라인 및 Feature 검증**:
    - `FastF1` 라이브러리를 활용해 5년 치(2021~2025) 전 경기 데이터를 안정적으로 확보했습니다.
    - 특히, 도메인 지식을 바탕으로 설계한 `Chaos_Score`와 `Position_Gains` 등의 파생 변수가 경기의 성격(혼란 vs 안정)을 잘 설명하고 있음을 확인했습니다.

2.  **데이터 기반의 핵심 인사이트 도출**:
    - "Chaos는 변수를 만들지만, Overtake를 보장하지는 않는다"는 사실을 데이터(약한 양의 상관관계, 0.22)로 입증했습니다.
    - **2021년**과 **2024년**의 비교를 통해, 단순한 사고 횟수뿐만 아니라 시즌별 라이벌 구도와 경기 양상이 데이터 분포에 명확히 반영됨을 발견했습니다.

3.  **머신러닝 모델링을 위한 준비 완료**:
    - 데이터의 결측치가 없고(Clean Data), 변수 간의 관계가 논리적으로 설명 가능함을 확인했습니다.
    - 이를 바탕으로 `Assignment 5`에서는 `Chaos_Score`, `Lead_Changes` 등의 Feature를 사용하여, 실제 팬들의 평점을 예측하는 'Excitement Predictor' 모델 설계를 진행할 예정입니다.
