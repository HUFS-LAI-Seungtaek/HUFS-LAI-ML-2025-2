# nn.Tanh()가 변인이 된 모델입니다.
class MLP(nn.Module):
    def __init__(self, input_size=784, hidden_size=100, num_classes=10):
        super(MLP, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, num_classes)
        )
    def forward(self, x):
        return self.layers(x)

# 모델 확인 (간단 샘플)
_model = MLP()
total_params = sum(p.numel() for p in _model.parameters())
trainable_params = sum(p.numel() for p in _model.parameters() if p.requires_grad)
print("MLP summary:")
print(_model)
print(f"Total params: {total_params:,}, Trainable: {trainable_params:,}")