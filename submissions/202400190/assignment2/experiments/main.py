import torch
import itertools
import pandas as pd
import torch.nn as nn
from model import MLP, MLP_Advanced
from data import get_data_loaders
from trainer import train_and_evaluate
from utils import set_seed, plot_experiment_results, plot_class_accuracy, plot_confusion_matrix
from result import performance_results_test


def run_experiments():

    # 하이퍼파라미터 조정 -> 모델 구조 개선 -> 최종 평가 순으로 진행합니다.

    set_seed(11) # 재현성을 위해 시드를 11로 고정합니다.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"사용 디바이스: {device}")
    
    # --- 기본 모델 성능 측정 ---
    # 원본 노트북의 파라미터로 기준 성능을 측정합니다.
    print("\n--- 기본 모델 성능 측정 시작 ---")
    baseline_params = {
        'lr': 1e-3, # Changed from 'learning_rate' to 'lr'
        'hidden_size': 100,
        'epochs': 3,
        'batch_size': 128
    }
    print(f"기본 파라미터: {baseline_params}")
    print(f"데이터셋 분할 : Train(55000), Validation(5000), Test(10000)")

    # 기본 모델 학습을 위한 데이터 로더 생성
    train_loader_base, val_loader_base, _ = get_data_loaders(
        batch_size=baseline_params['batch_size'], 
        test_batch_size=1000, 
        seed=11
    )
    
    # 기본 모델 생성 및 학습
    baseline_model = MLP(hidden_size=baseline_params['hidden_size'])
    baseline_result = train_and_evaluate(
    baseline_model,
    train_loader_base,
    val_loader_base,
    lr=baseline_params['lr'],
    epochs=baseline_params['epochs'],
    device=device
    )
    
    print("\n--- 기본 모델 성능 ---")
    print(f"최고 검증 정확도: {baseline_result['val_acc']:.2f}%")
    print(f"훈련 시간: {baseline_result['time']:.2f}초")
    print("------------------------\n")

    # --- 실험 1: 하이퍼파라미터 튜닝 (Grid Search) ---
    
    # 실험할 하이퍼파라미터 후보입니다.
    
    print("\n--- 실험 1: 하이퍼파라미터 튜닝 시작 ---")
    param_grid = {
        'lr': [1e-2, 1e-3, 1e-4], 
        'hidden_size': [50, 100, 200],
        'epochs': [3, 5, 10],
        'batch_size': [64, 128, 256]
    }
    
    results = []
    
    # 모든 파라미터 조합을 생성합니다.
    param_keys = param_grid.keys()
    param_values = param_grid.values()
    param_combinations = [dict(zip(param_keys, v)) for v in itertools.product(*param_values)]
    
    for i, params in enumerate(param_combinations):
        print(f"\n[{i+1}/{len(param_combinations)}] 실험 시작: {params}")
        model = MLP(hidden_size=params['hidden_size'])
        train_loader_exp, val_loader_exp, _ = get_data_loaders(batch_size=params['batch_size'], seed=11)
        result = train_and_evaluate(
            model,
            train_loader_exp,
            val_loader_exp,
            lr=params['lr'],
            epochs=params['epochs'],
            device=device
        )
        result.update(params)
        results.append(result)

    results_df = pd.DataFrame(results) # results -> *
    csv_filename = "hyperparameter_tuning_results.csv"
    results_df.to_csv(csv_filename, index=False) # index=False는 DataFrame 인덱스를 CSV에 쓰지 않도록 합니다.

    print(f"\n하이퍼파라미터 튜닝 결과가 {csv_filename} 파일로 저장되었습니다.")
    print()


    # 가장 성능이 좋았던 조합을 바탕으로 모델 구조 개선 실험을 진행합니다.
    best_run = max(results, key=lambda x: x['val_acc']) # results -> *
    best_params = best_run.copy()
    
    # 결과를 시각화합니다.
    plot_experiment_results(results, baseline_result['val_acc']) # results -> *

    
    # --- 실험 2: 모델 구조 개선 ---

    print("\n--- 실험 2: 모델 구조 개선 시작 ---")
    print(f"기본 모델 (실험 1 Best Model) 성능: {best_run['val_acc']:.2f}%")
    
    train_loader_best, val_loader_best, test_loader_final = get_data_loaders(
        batch_size=best_params['batch_size'], seed=11
    )
    
    experiment2_results = {'baseline': {'val_acc': best_run['val_acc'], 'params': {}}}

    # 실험 2-1: 은닉층 추가
    print("\n[실험 2-1] 은닉층 추가 (1개 -> 3개)")
    deeper_model = MLP(hidden_size=best_params['hidden_size'], num_hidden_layers=3)
    deeper_result = train_and_evaluate(
        deeper_model, train_loader_best, val_loader_best, 
        lr=best_params['lr'], epochs=best_params['epochs'], device=device # Changed from 'learning_rate' to 'lr'
    )
    experiment2_results['deeper'] = {'val_acc': deeper_result['val_acc'], 'params': {'num_hidden_layers': 3}}

    # 실험 2-2: 활성화 함수 변경
    for act_fn in ['sigmoid', 'tanh']:
        print(f"\n[실험 2-2] 활성화 함수 변경 (ReLU -> {act_fn.capitalize()})")
        act_model = MLP(hidden_size=best_params['hidden_size'], activation_fn=act_fn)
        act_result = train_and_evaluate(
            act_model, train_loader_best, val_loader_best, 
            lr=best_params['lr'], epochs=best_params['epochs'], device=device # Changed from 'learning_rate' to 'lr'
        )
        experiment2_results[act_fn] = {'val_acc': act_result['val_acc'], 'params': {'activation_fn': act_fn}}

    # 실험 2-3: 드롭아웃 추가
    print("\n[실험 2-3] 드롭아웃 추가 (p=0.5)")
    dropout_model = MLP(hidden_size=best_params['hidden_size'], dropout_p=0.5)
    dropout_result = train_and_evaluate(
        dropout_model, train_loader_best, val_loader_best, 
        lr=best_params['lr'], epochs=best_params['epochs'], device=device # Changed from 'learning_rate' to 'lr'
    )
    experiment2_results['dropout'] = {'val_acc': dropout_result['val_acc'], 'params': {'dropout_p': 0.5}}

    # 추가 실험: 은닉층 추가 + 드롭아웃 추가 + 하이퍼파라미터 변경
    print("\n*[추가 실험] 은닉층 추가 + 드롭아웃 추가 + 하이퍼파라미터 변경")

    new_model_config = { # 앞서 진행한 실험을 바탕으로 하이퍼파라미터도 일부 조정합니다.
        'lr': 0.0005,
        'hidden_size': 200,
        'epochs': 20,
        'batch_size': 64,
        'num_layers': 3,
        'dropout_rate': 0.2 # 드롭아웃의 비율을 작게 조정하였습니다.
    }

    model_exp2_4 = MLP_Advanced(
        input_size=784,
        hidden_size=new_model_config['hidden_size'],
        num_classes=10,
        num_layers=new_model_config['num_layers'],
        dropout_rate=new_model_config['dropout_rate']
    ).to(device)

    result_exp2_4 = train_and_evaluate(
        model=model_exp2_4,
        train_loader=train_loader_best, 
        val_loader=val_loader_best,     
        lr=new_model_config['lr'],
        epochs=new_model_config['epochs'], 
        device=device
    )

    experiment2_results['advanced_dropout'] = {
        'val_acc': result_exp2_4['val_acc'], 
        'params': {
            'num_hidden_layers': new_model_config['num_layers'], # 저장된 config 값 사용
            'dropout_p': new_model_config['dropout_rate'], # 저장된 config 값 사용
            'lr': new_model_config['lr'], # 추가된 LR과 Epoch도 저장하여 최종 모델에 반영될 수 있도록 함
            'epochs': new_model_config['epochs']
        }
    }


    # --- 실험 3: 최종 모델 성능 평가 ---
    
    print("\n--- 최종 모델 성능 평가 (실험 3) 시작 ---")

    # 실험 2에서 가장 성능이 좋았던 모델 구조를 최종 모델로 선정합니다.
    best_structure_name = max(experiment2_results, key=lambda k: experiment2_results[k]['val_acc'])
    final_model_val_acc = experiment2_results[best_structure_name]['val_acc']

    print(f"\n실험 2에서 가장 성능이 좋았던 모델은 '{best_structure_name}' 모델입니다. (검증 정확도: {final_model_val_acc:.2f}%)")
    
    final_params = best_params.copy()
    final_params.update(experiment2_results[best_structure_name]['params'])
    
    print(f"최종 모델 파라미터: {final_params}")
    final_model = MLP(
        hidden_size=final_params.get('hidden_size'),
        num_hidden_layers=final_params.get('num_hidden_layers', 1),
        activation_fn=final_params.get('activation_fn', 'relu'),
        dropout_p=final_params.get('dropout_p', 0.0)
    )
    
    print("\n최종 모델을 다시 학습하고 테스트 데이터셋으로 평가합니다.")
    train_and_evaluate(final_model, train_loader_best, val_loader_best, lr=final_params['lr'], epochs=final_params['epochs'], device=device)
    
    print("\n최종 모델의 테스트 데이터셋에 대한 Confusion Matrix:")
    classes = list(range(10)) # 또는 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    plot_confusion_matrix(final_model, test_loader_final, device, classes)

    print("\n--- 모든 실험 완료 ---")

if __name__ == '__main__':
    run_experiments()