# 1. 프로젝트 요약 및 모델 설계

## 1.1 프로젝트 목표

Assignment 4에서 수집한 Logan Allen 투수의 투구 데이터를 기반으로, 현재 경기 상황(볼/스트라이크 카운트, 주자 유무 등)이 주어졌을 때 다음 투구 구종을 예측하는 분류(Classification) 모델을 학습 및 평가한다.

## 1.2 모델 아키텍처 및 선택 이유

모델명: Scikit-learn RandomForestClassifier (랜덤 포레스트 분류기)

선택 이유:

적합성: 투구 데이터는 정형 데이터에 해당하며 랜덤 포레스트는 이러한 유형의 데이터에서 높은 예측력과 안정성을 보입니다.

투명성: 복잡한 딥러닝 모델에 비해 해석이 용이하며 학습 과정의 재현 가능성 확보가 쉽습니다.

속도: 적은 데이터셋을 학습하고 추론하는 속도가 매우 빠릅니다.

## 1.3 데이터 분할

총 데이터 수: 약 111개 (Logan Allen 투수의 2024년 5월 투구 중 정제된 데이터 기준)

분할 비율:

Train (학습): 약 77개 (약 69%)

Validation (검증): 약 11개 (약 10%)

Test (평가): 약 23개 (약 21%)

특징량(Feature): balls, strikes, on_1b, on_2b, on_3b, outs_when_up, inning

타겟(Target): pitch_type (Label Encoding을 통해 수치화)

# 2. 평가 지표 및 성능 결과

## 2.1 주요 평가 지표 (Test Set 기준)

*정확도 (Accuracy): 0.4783*

정밀도 (Precision): 0.2810

재현율 (Recall): 0.2788

F1-Score: 0.2747

## 2.2 특이사항 및 한계 분석

모델의 직구(FF) 편향:

정확도(Accuracy)가 47%로 낮게 나왔으며, 혼동 행렬 분석 결과 모델이 **직구(FF)**에 과도하게 편향되어 있음이 확인됨

원인 추정: 데이터셋 크기(N=111)가 매우 작고, 직구(FF) 투구 수가 다른 변화구보다 많아 모델이 직구를 안전한 예측값으로 선택하는 경향을 보임

낮은 F1-Score:

F1-Score가 0.27로 매우 낮게 측정되었는데, 이는 **스플리터(FS)**나 **싱커(SI)**와 같이 테스트셋에 거의 등장하지 않는 구종에 대한 정밀도(Precision)와 재현율(Recall)이 0으로 계산되어 평균을 크게 낮췄기 때문

향후 개선 방향:

더 많은 투구 데이터(최소 수천 개)를 확보하거나 데이터 불균형 문제를 해결하기 위한 오버샘플링(Oversampling) 기법을 적용해야 실제 사용 가능한 성능을 확보할 수 있을 것으로 예상



# 3 모델 가중치 저장 위치 

구글 드라이브 링크: https://drive.google.com/file/d/1KyAOJpEhmm20pPSIEdQA_y2ECM8q4UWY/view?usp=sharing

모델명: pitcher_model.pkl

인코더명: pitch_type_encoder.pkl

