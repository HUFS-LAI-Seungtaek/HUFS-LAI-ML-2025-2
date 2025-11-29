# 학습률 실험: lr만 바뀌고 epochs는 3을 사용하였습니다.
csv_path_lr, summaries_lr = run_experiments(
    mode="lr",
    lr_list=[1e-4, 3e-4, 1e-3],   # 바꾸고 싶은 lr 리스트
    baseline_epochs=3,
    batch_size=128,
    test_batch_size=1000,
    seed=42,
    results_dir="./exp_results",
    csv_name="mnist_lr_exps.csv",
    save_best_ckpt=True
)

# 에포크 실험: epochs만 바뀌어야 합니다.  (lr은 baseline_lr 사용)
csv_path_ep, summaries_ep = run_experiments(
    mode="epochs",
    epoch_list=[1, 3, 5],         # 바꾸고 싶은 epoch 리스트
    baseline_lr=1e-3,
    batch_size=128,
    test_batch_size=1000,
    seed=42,
    results_dir="./exp_results",
    csv_name="mnist_epoch_exps.csv",
    save_best_ckpt=True
)

# 결과 확인 (요약)
print("\nLR experiments summary:", summaries_lr)
print("\nEpoch experiments summary:", summaries_ep)