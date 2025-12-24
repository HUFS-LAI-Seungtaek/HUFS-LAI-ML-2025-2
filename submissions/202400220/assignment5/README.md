## 1. 프로젝트 개요

이 프로젝트는 한국어 입력 문장을 단순히 영어로 번역하는 것을 넘어, 제 영어 문체가 대사와 행동 묘사에 담기도록 모델을 파인튜닝하는 것입니다.

주 목적은 파파고의 딱딱한 직역체를 제하고 제 문체를 담는 것이며, 특히 대사와 지문(행동 묘사)을 구분하여 지문은 `*action*` 형태로 출력하는 것입니다.

---

## 2. 모델 아키텍처

- **베이스 모델:** `Helsinki-NLP/opus-mt-ko-en`
- **모델 타입:** Encoder-Decoder (Seq2Seq) Transformer

---

## 3. 데이터셋 분석

- **데이터 크기:** 100쌍 (Intent, Machine Translation, My Translation)
- **입력:** 한국어 의도 (Korean Intent)
- **출력:** 내 문체가 반영된 영어 번역 (My Translation)
- **특징:**
  - 기계 번역(평균 약 11.6 단어) 대비 제 번역(평균 약 10.7 단어)이 좀 더 간결합니다.
  - 문장의 약 80% 이상에서 `*smile*`, `*look at him*` 등의 행동 묘사가 포함됩니다.
  - 'Okay' 보다는 'Cool', 'Yes' 보다는 'Yeah' 등 구어체를 선호하는 경향을 보입니다.

---

## 4. 학습 환경

- **환경:** Google Colab (T4 GPU)
- **하이퍼파라미터:**
  - **에포크:** 12 (early stopping 적용)
  - **배치 사이즈:** 16
  - **학습률:** 2e-5
  - **옵티마이저:** AdamW
  - **가중치 감쇠:** 0.01
  - **손실 함수:** Cross-Entropy Loss

**학습 특이사항:**
- `EarlyStoppingCallback(patience=5)`을 적용하여 Validation Loss가 더 이상 개선되지 않는 25 Epoch 시점에서 학습을 조기 종료하고, 과적합을 방지했습니다.

---

## 5. 평가 및 성능

모델의 성능은 **BLEU Score**를 통해 정량적으로 평가하고, 스스로 결과를 검토하며 정성적으로도 평가하였습니다.

### 결과
- BLUE Score 기준 49.77로, 데이터가 100개로 적음에도 불구하고 높은 점수를 기록했습니다.
- 제가 판단했을 때에도 대사와 지문을 잘 구별하여 적절한 곳에 `*`표시를 사용하는 것을 확인할 수 있었습니다.

| Input (Korean) | Target (Human) | Model Output | Analysis |
|----------------|----------------|--------------|
| **난 애가 아니야. 기다릴 수 있어.** | I'm not a child. I can wait. `*chuckle softly*` | I'm not a child. I can wait. `*chuckle softly*` | 대사와 지문이 완벽히 일치합니다.
| **좋아. 따라갈게.** | Cool. I'll follow you. `*smile, then start walk with him*` | Okay. I'll follow you. `*smile, then start walking with him*` | 'Cool'을 'Okay'로 번역했으나, 뒷부분 행동 묘사는 정확했습니다. |
| **나도 먹기 시작한다** | `*I start eating as well*` | `*I start eating*` | 지문 사이에 대사가 올 때에도 *을 잘 삽입하였습니다. (전문은 평가 코드 확인) |

---

## 6. 모델

학습된 모델 가중치와 토크나이저는 Hugging Face Hub에 업로드되어 누구나 사용할 수 있습니다.

- 링크: https://huggingface.co/pilan2/cai-translator