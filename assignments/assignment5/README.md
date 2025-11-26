# 5th Assignment: Model Training and Evaluation

## 과제 개요

이번 과제는 Assignment 4에서 수집 및 분석한 데이터를 기반으로 **모델을 직접 설계하고 학습시키며 평가**하는 단계입니다.

좋은 데이터에서 시작된 좋은 모델은 **명확한 평가 기준**이 필요합니다. 이 과제의 핵심은:
- 모델 설계 및 학습 과정의 투명성
- 평가 지표와 프로토콜의 명시성
- 학습된 모델의 재현 가능성

### 전체 프로젝트 구성

| Assignment | 주제 | 설명 |
|-----------|------|------|
| Assignment 3 | Project Proposal | 프로젝트 주제 설정 및 제안서 작성 |
| Assignment 4 | Data Collection and Analysis | 데이터 수집 및 분석 |
| **Assignment 5** | **Model Training and Evaluation** | **모델 학습 및 평가** |
| Assignment 6 | Real Usage and Final Report | 실제 사용 및 최종 보고서 |

### Assignment 5의 목표

- 모델 아키텍처를 설계하고 구현합니다.
- 데이터셋을 Train/Validation/Test 로 분할합니다.
- 모델을 학습시킵니다.
- 평가 지표와 평가 프로토콜을 명확하게 정의합니다.
- 학습된 모델 가중치를 저장하고 공유합니다.
- 저장된 모델을 로드하여 추론하는 코드를 작성합니다.

### TL;DR

| 항목 | 설명 |
|------|------|
| **학습 코드** | `training.ipynb` - 모델 설계, 학습, 체크포인트 저장 |
| **평가 코드** | `evaluation.ipynb` - 평가 지표 및 성능 평가 |
| **추론 코드** | `inference.ipynb` - 저장된 모델 로드 및 예시 추론 |
| **모델 가중치** | Google Drive 또는 HuggingFace에 업로드 |
| **평가 기준** | inference 코드로 모델을 직접 평가 가능해야 함 |

---

## 제출 방법

`submissions/{학번}/assignment5/` 디렉토리에 학습, 평가, 추론 코드를 제출하세요.

### 제출 구조

```
submissions/{학번}/assignment5/
├── training.ipynb              # (필수) 모델 학습 코드
├── evaluation.ipynb            # (필수) 모델 평가 코드
├── inference.ipynb             # (필수) 모델 추론 코드 (예시값 포함)
├── README.md                   # (필수) 프로젝트 요약 및 결과
└── (선택) eval_dataset/        # 평가용 데이터셋 (작은 경우만)
```

### 제출 단계

1. [https://github.com/HUFS-LAI-Seungtaek/HUFS-LAI-ML-2025-2](https://github.com/HUFS-LAI-Seungtaek/HUFS-LAI-ML-2025-2) 접속
2. 본인의 Fork repository에서 작업
3. **세 개의 Notebook 파일 작성** (Google Colab 또는 Jupyter Notebook 사용 가능):
   - `training.ipynb`: 모델 설계, 학습, 가중치 저장
   - `evaluation.ipynb`: 평가 지표 정의 및 성능 평가
   - `inference.ipynb`: 모델 로드 및 추론 예시
4. **모델 가중치 저장**:
   - Google Drive: 공개 폴더 생성 후 링크 제공
   - HuggingFace Hub: 모델 업로드 후 URL 제공
5. **README.md 작성**:
   - 모델 아키텍처 설명
   - 평가 지표 및 성능 결과
   - 모델 가중치 저장 위치
6. 제출 후 PR 생성
   - Title: `5th Assignment by {학번} ({영어 이름})`
   - Description에 모델 가중치 링크와 주요 성능 지표 포함

---

## 평가 기준

### Assignment 5 평가 기준

이 과제는 다음 항목들을 **정량적으로 평가**합니다.

#### 1. 제출 구조 완성 (필수)
- PR이 정상적으로 생성되고 merge 가능한 상태
- 세 개의 필수 Notebook 파일 제출:
  - `training.ipynb`
  - `evaluation.ipynb`
  - `inference.ipynb`
- `README.md` 제출

#### 2. Training
- **모델 설계의 적절성**: 프로젝트에 맞는 모델 선택
- **데이터셋 분할의 명확성**: Train/Validation/Test 분할 비율 명시
- **학습 과정의 투명성**:
  - Loss, 성능 지표를 epoch별로 추적
  - 학습 곡선 시각화
  - Validation 성능 모니터링
- **재현 가능성**: 모델 가중치를 저장하고 복원 가능

#### 3. Evaluation

- 평가 지표가 명확하게 정의되고 계산되어야 합니다. 
- 문제 유형에 맞는 지표를 선택하고, 각 지표의 정의와 계산 코드가 명시적으로 드러나야 합니다. 
- 주요 성능 수치는 (되도록) 정리된 표 형태로 표현되어야 합니다. 
- Test set에서만 최종 평가를 수행하고, 평가 과정이 단계별로 명확해야 합니다. 
- 필요에 따라 여러 번의 실험이나 cross-validation을 고려할 수 있습니다.

#### 4. Inference 평가
- **모델 가중치 접근성**: Google Drive 혹은 HuggingFace에서 접근 가능해야함
- **추론 코드의 완전성**: 모델 로드부터 결과 출력까지 독립적으로 실행 가능해야함
- **예시값 포함**: 최소 3개 이상의 실제 추론 예시 제시 (주제와의 관련성에 대해 다시 한번 생각해주세요)
- **재현성**: inference 코드만으로도 모델 실제 실행 및 평가가 가능해야 합니다

#### 5. README.md 평가

README.md에는 모델 아키텍처에 대한 설명과 평가 지표 및 성능 결과가 정리되어 있어야 합니다.

모델 가중치의 저장 위치가 명시되어야 하며, 학습 및 평가 과정에서 발견한 특이사항과 한계 등을 기록하는 것이 좋습니다.

### 제출 시 주의사항

**PR 형식 불일치로 merge가 불가능한 경우 0점 처리됩니다.**

**감점 사유:**
- 필수 파일 누락 (training, evaluation, inference)
- 평가 지표 누락 또는 불명확
- 모델 가중치 누락 또는 접근 불가
- Inference 코드에 예시값 미포함

---

## FAQ

**Q: 모델 성능이 좋지 않으면 어떻게 하나요?**
A: 성능 자체보다는 **평가 과정의 명확성과 데이터 분석의 충실성**을 중심으로 평가합니다. 저성능의 원인을 분석하고 이를 README에 기록하면 좋습니다.

**Q: Inference 코드의 "예시값"은 어떤 형태여야 하나요?**
A: 실제 데이터셋의 샘플이거나, 프로젝트에 맞는 새로운 입력값으로 모델을 실행하는 코드입니다. 결과가 출력되고 해석되어야 합니다.

**Q: 모델 가중치가 너무 커서 저장할 수 없으면?**
A: Google Drive 또는 HuggingFace Hub에 업로드하세요. Inference 코드에서 다운로드 받아 사용하는 방식을 권장합니다.

**Q: 여러 모델을 시도했는데, 어느 것을 제출해야 하나요?**
A: 가장 좋은 성능의 모델을 제출하세요. 다른 시도들은 README나 training.ipynb에 간단히 기록해도 좋습니다.

**Q: HuggingFace는 어떻게 사용하나요?**
A: HuggingFace Hub에 가입 후 모델을 업로드하면, `huggingface_hub` 라이브러리로 쉽게 로드할 수 있습니다. 공식 문서를 참조하세요.

**Q: Balanced Accuracy, Macro F1 등의 지표는 필수인가요?**
A: 클래스 불균형이 있다면 필수입니다. 균형잡힌 데이터라면 일반 Accuracy/F1로 충분합니다.

**Q: 평가 데이터셋을 GitHub에 올려도 되나요?**
A: 작은 데이터셋(<10MB)은 올려도 좋습니다. 크거나 저작권 이슈가 발생할 수 있다면 Google Drive 링크로 제공해주세요.

---

## 제출 마감

- **마감일**: 2025-12-3 (2 weeks)
- **제출 방법**: GitHub Pull Request
- **지각 제출**: 마감일 이후 제출 시 0점 처리.

---

## 핵심 체크리스트

제출 전 다음을 확인하세요:

- [ ] `training.ipynb`: 모델 학습 및 가중치 저장 완료
- [ ] `evaluation.ipynb`: 평가 지표, 프로토콜, 데이터 분석 포함
- [ ] `inference.ipynb`: 모델 로드 + 예시 3개 이상 실행
- [ ] 모델 가중치: Google Drive/HuggingFace에 업로드 및 공개 설정
- [ ] `README.md`: 모델 설명, 성능, 데이터셋 분석, 링크 포함
- [ ] PR 생성: 제목 및 설명 포함
- [ ] 코드 실행: 다른 환경에서도 실행 가능한지 확인

---

마지막으로, 이 과제는 **"모델을 어떻게 평가할 것인가"**에 대한 깊이 있는 사고가 가장 중요합니다. 좋은 평가 없이는 좋은 모델도 증명할 수 없습니다.
