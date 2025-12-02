
# 실험에 있어서는 반복 실행이 핵심이라고 알고 있으며 반복 실행을 자동화 하는 알고리즘의 필요성을 느껴 run_experiments 함수의 pipline을 LLM의 도움을 받아 참고 작성하였습니다.

# loss와 관련된 데이터들이 나온 이후로는 데이터 분석의 영역으로 넘어가는 것이라고 생각합니다. 많은 데이터 분석 tool들이 csv 형식의 파일과 친숙하기에 해당 형식으로 로그가 저장되도록 합니다.
import math

def run_experiments(
    mode: str = "lr",
    lr_list: List[float] = None,
    epoch_list: List[int] = None,
    baseline_lr: float = 1e-3,
    baseline_epochs: int = 3,
    batch_size: int = 128,
    test_batch_size: int = 1000,
    seed: int = 42,
    results_dir: str = "./exp_results",
    csv_name: str = "results.csv",
    save_best_ckpt: bool = True
) -> Tuple[str, List[Tuple]]:
    """
    mode: 'lr' 또는 'epochs'
    반환: (csv_path, summaries) where summaries = list of (exp_name, lr, epochs, best_val_acc, ckpt_path_or_None)
    """
    assert mode in ("lr", "epochs")
    os.makedirs(results_dir, exist_ok=True)
    csv_path = os.path.join(results_dir, csv_name)

    if lr_list is None:
        lr_list = [1e-4, 3e-4, 1e-3, 3e-3]
    if epoch_list is None:
        epoch_list = [1, 3, 5]

    # CSV 헤더
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["exp_name", "mode", "value", "epoch", "train_loss", "val_loss", "val_acc", "elapsed_sec", "ckpt"])

    # 공통 로더
    train_loader, test_loader = make_loaders(batch_size=batch_size, test_batch_size=test_batch_size)

    criterion = nn.CrossEntropyLoss()
    summaries = []

    if mode == "lr":
        for lr in lr_list:
            exp_name = f"lr_{lr}"
            print(f"\n=== 실험: {exp_name} | epochs={baseline_epochs} ===")
            set_seed(seed)
            model = MLP().to(device)
            optimizer = optim.Adam(model.parameters(), lr=lr)
            best_val_acc = -math.inf
            best_ckpt = None
            start_total = time.time()

            for ep in range(1, baseline_epochs+1):
                t0 = time.time()
                train_loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
                val_loss, val_acc = evaluate(model, test_loader, criterion, device)
                elapsed = time.time() - t0

                # 출력
                print(f"[{exp_name}] Ep {ep}/{baseline_epochs} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.2f}%")

                # CSV 기록
                with open(csv_path, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([exp_name, "lr", lr, ep, round(train_loss,6), round(val_loss,6), round(val_acc,3), round(elapsed,3), ""])

                # 체크포인트 저장 (최고 val_acc)
                if save_best_ckpt and val_acc > best_val_acc:
                    best_val_acc = val_acc
                    best_ckpt = os.path.join(results_dir, f"{exp_name}_best.pth")
                    torch.save({"model_state": model.state_dict(), "lr": lr, "epoch": ep, "val_acc": val_acc}, best_ckpt)

            total_elapsed = time.time() - start_total
            summaries.append((exp_name, lr, baseline_epochs, best_val_acc if best_val_acc!=-math.inf else None, best_ckpt))
            print(f"완료: {exp_name} | best_val_acc={best_val_acc:.2f}% | total_elapsed={total_elapsed:.1f}s | ckpt={best_ckpt}")

    else:  # mode == 'epochs'
        for epochs in epoch_list:
            exp_name = f"ep_{epochs}"
            print(f"\n=== 실험: {exp_name} | lr={baseline_lr} ===")
            set_seed(seed)
            model = MLP().to(device)
            optimizer = optim.Adam(model.parameters(), lr=baseline_lr)
            best_val_acc = -math.inf
            best_ckpt = None
            start_total = time.time()

            for ep in range(1, epochs+1):
                t0 = time.time()
                train_loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
                val_loss, val_acc = evaluate(model, test_loader, criterion, device)
                elapsed = time.time() - t0

                # 에포크별 출력
                print(f"[{exp_name}] Ep {ep}/{epochs} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.2f}%")

                # CSV 기록
                with open(csv_path, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([exp_name, "epochs", epochs, ep, round(train_loss,6), round(val_loss,6), round(val_acc,3), round(elapsed,3), ""])

                # 체크포인트 저장 (최고 val_acc)
                if save_best_ckpt and val_acc > best_val_acc:
                    best_val_acc = val_acc
                    best_ckpt = os.path.join(results_dir, f"{exp_name}_best.pth")
                    torch.save({"model_state": model.state_dict(), "lr": baseline_lr, "epoch": ep, "val_acc": val_acc}, best_ckpt)

            total_elapsed = time.time() - start_total
            summaries.append((exp_name, baseline_lr, epochs, best_val_acc if best_val_acc!=-math.inf else None, best_ckpt))
            print(f"완료: {exp_name} | best_val_acc={best_val_acc:.2f}% | total_elapsed={total_elapsed:.1f}s | ckpt={best_ckpt}")

    # 요약 출력
    print("\n=== 전체 요약 ===")
    for s in summaries:
        print(f"{s[0]} | lr={s[1]} | epochs={s[2]} | best_val_acc={s[3]} | ckpt={s[4]}")

    print(f"\nCSV 저장 경로: {csv_path}")
    return csv_path, summaries