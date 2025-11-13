import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from datasets import load_dataset

def get_data_loaders(batch_size, test_batch_size=1000, val_split=5000, seed=11):
    
    # MNIST 데이터셋을 불러오고, 훈련/검증/테스트 데이터 로더를 생성합니다.

    # 재현성을 위해 표준 정규화 값을 사용합니다.
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)) 
    ])

    def transform_fn(batch):
        # 28x28 이미지를 784 크기의 1차원 벡터로 변환합니다.
        images = [transform(img).view(-1) for img in batch["image"]]
        return {"image": torch.stack(images), "label": torch.tensor(batch["label"])}

    # 데이터셋 로딩
    # trust_remote_code=True는 Hugging Face Hub의 데이터셋 스크립트 실행을 허용합니다.
    full_train_dataset_raw = load_dataset("mnist", split='train')
    test_dataset_raw = load_dataset("mnist", split='test')

    # 훈련 데이터셋을 훈련용과 검증용으로 분할합니다 (55k / 5k)
    # stratify_by_column을 사용하여 클래스 비율을 유지합니다.
    split_dataset = full_train_dataset_raw.train_test_split(test_size=val_split, stratify_by_column='label', seed=seed)
    train_dataset_raw = split_dataset['train']
    val_dataset_raw = split_dataset['test']
    
    # 각 데이터셋에 transform 적용
    train_dataset = train_dataset_raw.with_transform(transform_fn)
    val_dataset = val_dataset_raw.with_transform(transform_fn)
    test_dataset = test_dataset_raw.with_transform(transform_fn)

    # 데이터 로더 생성
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=test_batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=test_batch_size, shuffle=False)
    
    return train_loader, val_loader, test_loader