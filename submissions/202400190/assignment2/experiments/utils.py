
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import torch
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pandas as pd
import random
import numpy as np
import torch

def set_seed(seed):
    # 재현성 확보를 위해 시드를 고정합니다.

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False



def plot_training_results(train_losses, train_accuracies, test_accuracies, nb_epochs):
    
    # Loss와 Accuracy을 나타내는 곡선을 그립니다.
    epochs_range = range(1, nb_epochs + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Loss plot
    ax1.plot(epochs_range, train_losses, 'b-', marker='o', linewidth=2, markersize=8)
    ax1.set_title('Training Loss', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Loss', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(epochs_range)

    # Accuracy plot
    ax2.plot(epochs_range, train_accuracies, 'g-', marker='s', linewidth=2,
             markersize=8, label='Train Accuracy')
    ax2.plot(epochs_range, test_accuracies, 'r-', marker='^', linewidth=2,
             markersize=8, label='Test Accuracy')
    ax2.set_title('Accuracy Comparison', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Accuracy (%)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=11)
    ax2.set_xticks(epochs_range)
    ax2.set_ylim(80, 100)

    plt.tight_layout()
    plt.savefig('training_curves.png')
    print("훈련 곡선이 training_curves.png 파일로 저장되었습니다.")
    plt.show()


def plot_experiment_results(experiment_results, baseline_acc):
    
    # 하이퍼파라미터 튜닝 실험의 결과를 시각화합니다.

    results_df = pd.DataFrame(experiment_results)

    # Validation accuracy를 기준으로 정렬합니다.
    results_df = results_df.sort_values(by='val_acc', ascending=False).reset_index(drop=True)

    print("--- Experiment Results Summary (Top 10) ---")
    print(results_df.head(10))

    # Plotting results
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    # Plot 1: Accuracy vs. Configuration Index
    axes[0].plot(results_df.index, results_df['val_acc'], marker='o', linestyle='-')
    axes[0].axhline(y=baseline_acc, color='r', linestyle='--', label=f'Baseline Accuracy ({baseline_acc:.2f}%)')
    axes[0].set_title('Validation Accuracy by Experiment', fontsize=14)
    axes[0].set_xlabel('Experiment Index (Sorted by Accuracy)', fontsize=12)
    axes[0].set_ylabel('Validation Accuracy (%)', fontsize=12)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2 & 3: Impact of two parameters on accuracy (example: lr and hidden_size)
    
    if 'lr' in results_df.columns and 'hidden_size' in results_df.columns:
        pivot_lr_hs = results_df.pivot_table(values='val_acc', index='lr', columns='hidden_size')
        sns.heatmap(pivot_lr_hs, annot=True, fmt=".2f", cmap="viridis", ax=axes[1])
        axes[1].set_title('Accuracy Heatmap (LR vs Hidden Size)', fontsize=14)
        axes[1].set_xlabel('Hidden Size', fontsize=12)
        axes[1].set_ylabel('Learning Rate', fontsize=12)

    if 'epochs' in results_df.columns and 'batch_size' in results_df.columns:
         pivot_epochs_bs = results_df.pivot_table(values='val_acc', index='epochs', columns='batch_size')
         sns.heatmap(pivot_epochs_bs, annot=True, fmt=".2f", cmap="viridis", ax=axes[2])
         axes[2].set_title('Accuracy Heatmap (Epochs vs Batch Size)', fontsize=14)
         axes[2].set_xlabel('Batch Size', fontsize=12)
         axes[2].set_ylabel('Epochs', fontsize=12)


    plt.tight_layout()
    plt.savefig('hyperparameter_tuning_results.png')
    print("\n하이퍼파라미터 튜닝 결과가 hyperparameter_tuning_results.png 파일로 저장되었습니다.")
    # plt.show()


def plot_class_accuracy(class_correct, class_total, title="Class-wise Accuracy"):
    
    #Plots the accuracy for each class.
    
    accuracy_by_class = [(class_correct[i] / class_total[i] * 100) if class_total[i] > 0 else 0 for i in range(10)]
    classes = [str(i) for i in range(10)]

    plt.figure(figsize=(10, 6))
    
    sns.barplot(x=classes, y=accuracy_by_class, hue=classes, palette='viridis', legend=False)
    plt.ylim(0, 100)
    plt.title(title, fontsize=14)
    plt.xlabel('Digit Class', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('class_accuracy_comparison.png')

    print("\n클래스별 정확도 비교 결과를 class_accuracy_comparison.png에 저장했습니다")
    plt.show() 


def plot_confusion_matrix(model, data_loader, device, classes):
    
    # 모델과 데이터 로더를 사용하여 Confusion Matrix를 계산하고 그립니다.
    
    model.eval()
    all_labels = []
    all_predictions = []

    with torch.no_grad():
        for batch in data_loader:
            imgs = batch["image"].to(device)
            labels = batch["label"].to(device)

            outputs = model(imgs)
            _, predicted = torch.max(outputs, 1)

            all_labels.extend(labels.cpu().numpy())
            all_predictions.extend(predicted.cpu().numpy())

    cm = confusion_matrix(all_labels, all_predictions, labels=classes)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)

    fig, ax = plt.subplots(figsize=(10, 10))
    disp.plot(cmap=plt.cm.Blues, ax=ax)
    ax.set_title('Confusion Matrix', fontsize=14)
    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.set_ylabel('True Label', fontsize=12)

    plt.savefig('confusion_matrix.png')
    print("\nconfusion matrix가 confusion_matrix.png 파일로 저장되었습니다.")

