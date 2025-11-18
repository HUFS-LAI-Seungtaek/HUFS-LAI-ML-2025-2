from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np

best_model = make_model([100, 50, 25]).to(device)
optimizer = optim.Adam(best_model.parameters(), lr=1e-3)

best_model.train()
for epoch in range(5):
    for batch in train_loader:
        imgs = batch["image"].to(device)
        labels = batch["label"].to(device)
        optimizer.zero_grad()
        loss = criterion(best_model(imgs), labels)
        loss.backward()
        optimizer.step()

best_model.eval()
y_true, y_pred = [], []
with torch.no_grad():
    for batch in test_loader:
        imgs = batch["image"].to(device)
        labels = batch["label"].to(device)
        preds = best_model(imgs).argmax(1)
        y_true.extend(labels.cpu().numpy())
        y_pred.extend(preds.cpu().numpy())

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap="Reds", xticks_rotation=45)
plt.title("Confusion Matrix of Best Model (lr=1e-3, [100,50,25])")
plt.show()
