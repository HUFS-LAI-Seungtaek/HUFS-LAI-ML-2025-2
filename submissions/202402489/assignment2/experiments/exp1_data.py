
# MNIST를 다운로드, transform, DataLoader를 정의해 둡니다. 
print("Downloading MNIST (if not cached)...")
mnist = load_dataset("mnist")  # HF datasets

# 표준 MNIST mean/std (튜토리얼에서 나왔던 통계값 도출입니다)
MNIST_MEAN = (0.1307,)
MNIST_STD  = (0.3081,)

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(MNIST_MEAN, MNIST_STD)
])

# flatten(28*28 -> 784) 처리가 필요하다고 알고 있어서 해당 과정이 포함되도록 래퍼라는 개념을 처음 써봤습니다.
class HFDatasetWrapper(Dataset):
    def __init__(self, hf_ds, transform=None):
        self.ds = hf_ds
        self.transform = transform
    def __len__(self):
        return len(self.ds)
    def __getitem__(self, idx):
        item = self.ds[idx]
        img = item["image"]
        lbl = int(item["label"])
        if self.transform:
            img = self.transform(img)
        img = img.view(-1)  # flatten -> (784,)
        return {"image": img, "label": torch.tensor(lbl, dtype=torch.long)}

train_ds = HFDatasetWrapper(mnist["train"], transform=transform)
test_ds  = HFDatasetWrapper(mnist["test"],  transform=transform)

print("Train size:", len(train_ds), "Test size:", len(test_ds))