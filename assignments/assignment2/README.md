# Assignment 2: MNIST 손글씨 숫자 분류

## 📋 과제 개요

이 과제에서는 PyTorch를 사용하여 MNIST 데이터셋의 손글씨 숫자를 분류하는 Multi-Layer Perceptron (MLP) 모델을 구현하고 학습합니다.

### 학습 목표
- PyTorch를 이용한 기본적인 신경망 구현
- 데이터 로딩 및 전처리 과정 이해
- 모델 훈련 및 평가 과정 체험
- 예측 결과 시각화 및 분석
- 하이퍼파라미터 튜닝 실험

## 🚀 시작하기

### 1. Repository Fork 및 Clone

```bash
# 1. GitHub에서 이 repository를 fork하세요
# 2. fork한 repository를 로컬에 clone
git clone https://github.com/YOUR_USERNAME/HUFS-LAI-ML-2025-2.git
cd HUFS-LAI-ML-2025-2

# 3. 원본 repository를 upstream으로 추가
git remote add upstream https://github.com/HUFS-LAI-Seungtaek/HUFS-LAI-ML-2025-2.git
```

### 2. 과제 파일 복사

⚠️ **중요**: `assignments` 디렉토리는 과제 템플릿 제공용이므로, 실제 작업은 `submissions` 디렉토리에서 진행해야 합니다.

```bash
# submissions 디렉토리에 본인의 학번 폴더 생성
mkdir -p submissions/YOUR_STUDENT_ID/assignment2

# 과제 파일을 submissions 폴더로 복사
cp assignments/assignment2/ml-mnist.ipynb submissions/YOUR_STUDENT_ID/assignment2/
```

## 📁 디렉토리 구조

```
submissions/YOUR_STUDENT_ID/assignment2/
├── README.md                    # 본인의 실험 결과 및 분석 보고서
├── ml-mnist.ipynb            # 메인 과제 노트북
└── experiments/                 # (선택사항) 추가 실험 파일들
    ├── hyperparameter_tuning.ipynb
    ├── model_comparison.ipynb
    └── results/
        ├── training_plots.png
        └── confusion_matrix.png
```

## 🎯 과제 수행 가이드

### 1. 기본 구현 완료하기
- `ml-mnist.ipynb` 노트북의 모든 셀을 실행하여 기본 모델 학습
- 각 섹션의 설명을 읽고 코드 이해하기
- 결과 그래프 및 시각화 확인

### 2. 실험 수행하기
노트북의 "6. 과제 및 실험" 섹션에서 제안된 (혹은 본인만의) 실험들을 수행한다. 아래는 예시.
경향성을 파악할 수 있을 수준으로 다양하게 실험해 보는 것을 추천. 
관련해서 계속 코드를 반복하기 보다는 이런 실험들을 자동화 할 수 있는 코드를 작성하는 것이 장려됨. 

#### 🔧 실험 1: 하이퍼파라미터 튜닝
- [ ] 학습률 변경 (`1e-2`, `1e-4` 등)
- [ ] 은닉층 크기 조정 (`50`, `200` 등)
- [ ] 에포크 수 증가 (`5`, `10` 등)

#### 🏗️ 실험 2: 모델 구조 개선
- [ ] 은닉층 추가 (3층, 4층 신경망)
- [ ] 다른 활성화 함수 적용
- [ ] Dropout 추가

#### 📈 실험 3: 성능 분석
- [ ] Confusion Matrix 생성
- [ ] 클래스별 정확도 분석
- [ ] 오분류 패턴 분석

### 3. 결과 문서화
`submissions/YOUR_STUDENT_ID/assignment2/README.md` 파일에 다음 내용 작성:

```markdown
# MNIST 분류 실험 결과

## 기본 모델 성능
- 최종 테스트 정확도: XX.XX%
- 훈련 시간: X분 XX초

## 실험 결과
### 실험 1: [실험명]
- 변경사항:
- 결과:
- 분석:

### 실험 2: [실험명]
- 변경사항:
- 결과:
- 분석:

## 결론 및 인사이트
- 가장 효과적인 개선 방법:
- 관찰된 패턴:
- 추가 개선 아이디어:
```

## 📤 제출 방법

### 1. 변경사항 커밋
```bash
cd submissions/YOUR_STUDENT_ID/assignment2/
git add .
git commit -m "Complete MNIST assignment experiments"
git push origin main
```

### 2. Pull Request 생성
1. GitHub에서 본인의 fork repository로 이동
2. "New Pull Request" 클릭
3. **Base repository**: `HUFS-LAI-Seungtaek/HUFS-LAI-ML-2025-2`
4. **Base branch**: `main`
5. **PR 제목**: `2nd Assignment by [학번] (이름)`
6. **PR 설명**에 주요 실험 결과 요약 작성

### 3. 제출 체크리스트
- [ ] `ml-mnist.ipynb` 모든 셀 실행 완료
- [ ] 최소 2개 이상의 실험 수행
- [ ] 실험 결과를 README.md에 문서화
- [ ] 올바른 디렉토리 구조 (`submissions/학번/assignment2/`)
- [ ] PR 제목 형식 준수
- [ ] 불필요한 파일 제외 (`.ipynb_checkpoints/`, `__pycache__/` 등)

## 🔧 개발 환경 설정

### 로컬 환경 설정

#### 필요한 패키지 설치
```bash
pip install torch torchvision datasets matplotlib numpy jupyter
```

#### GPU 사용 (선택사항)
- CUDA가 설치된 환경에서는 자동으로 GPU를 사용합니다
- CPU에서도 정상적으로 실행됩니다

### Google Colab 사용하기 🚀

로컬 환경 설정이 어렵거나 GPU가 필요한 경우 Google Colab을 권장합니다.

#### 1. Colab에서 노트북 열기
1. [Google Colab](https://colab.research.google.com/) 접속
2. GitHub 탭 클릭
3. Repository URL 입력: `https://github.com/YOUR_USERNAME/HUFS-LAI-ML-2025-2`
4. `assignments/assignment2/ml-mnist.ipynb` 선택하여 열기

#### 2. 런타임 설정
```python
# Colab 환경에서 GPU 사용 설정
# 런타임 → 런타임 유형 변경 → 하드웨어 가속기: GPU 선택
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Current device: {torch.cuda.get_device_name()}")
```

#### 3. 필요한 패키지 설치 (Colab용)
```python
# 대부분의 패키지는 이미 설치되어 있지만, 필요시 실행
!pip install datasets
```

#### 4. 작업 완료 후 다운로드
- Colab에서 작업한 노트북을 다운로드: 파일 → .ipynb 다운로드
- 로컬의 `submissions/YOUR_STUDENT_ID/assignment2/` 폴더에 저장
- Git을 통해 커밋 및 Push

#### ⚠️ Colab 사용 시 주의사항
- 일정 시간 후 런타임이 초기화될 수 있으니 정기적으로 저장하세요
- 무료 GPU 사용 시간에 제한이 있습니다
- 최종 제출은 반드시 본인의 GitHub repository에서 해야 합니다

## 🤝 도움이 필요할 때

1. **Git 관련 문제**: [GitHub 공식 문서](https://docs.github.com) 참조
2. **PyTorch 관련 질문**: [PyTorch 공식 문서](https://pytorch.org/docs/) 확인
3. **과제 관련 질문**: eClass 혹은 GitHub Issues 를 통해 문의. 답변이 없다면 수업 시간 또는 이메일로 문의.

---

- **마감일**: 2025년 10월 3일 (금요일) 오후 11시 59분
- **제출 방식**: GitHub Pull Request
- **문의**: seungtaek.choi@hufs.ac.kr