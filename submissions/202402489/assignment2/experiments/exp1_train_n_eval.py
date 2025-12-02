def set_seed(seed: int = 42):
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def make_loaders(batch_size: int = 128, test_batch_size: int = 1000, num_workers: int = 2):
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,  num_workers=num_workers)
    test_loader  = DataLoader(test_ds,  batch_size=test_batch_size, shuffle=False, num_workers=num_workers)
    return train_loader, test_loader

def train_one_epoch(model: nn.Module, loader: DataLoader, optimizer: optim.Optimizer, criterion, device) -> float:
    model.train()
    total_loss = 0.0
    n = 0
    for batch in loader:
        imgs = batch["image"].to(device)
        labels = batch["label"].to(device)
        optimizer.zero_grad()
        outs = model(imgs)
        loss = criterion(outs, labels)
        loss.backward()
        optimizer.step()
        bs = imgs.size(0)
        total_loss += float(loss.item()) * bs
        n += bs
    return total_loss / n if n>0 else 0.0

def evaluate(model: nn.Module, loader: DataLoader, criterion, device) -> Tuple[float, float]:
    model.eval()
    total_loss = 0.0
    correct = 0
    n = 0
    with torch.no_grad():
        for batch in loader:
            imgs = batch["image"].to(device)
            labels = batch["label"].to(device)
            outs = model(imgs)
            loss = criterion(outs, labels)
            total_loss += float(loss.item()) * imgs.size(0)
            preds = outs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            n += imgs.size(0)
    avg_loss = total_loss / n if n>0 else 0.0
    acc = 100.0 * correct / n if n>0 else 0.0
    return avg_loss, acc