import torch
import torch.nn as nn

class MLP(nn.Module):

    # 다양한 구조 변경 실험을 지원하는 유연한 MLP 모델.
    # 은닉층 개수, 활성화 함수, 드롭아웃 비율을 조절할 수 있습니다.
    
    def __init__(self, input_size=784, num_classes=10, hidden_size=100, 
                 num_hidden_layers=1, activation_fn='relu', dropout_p=0.0):
        super(MLP, self).__init__()
        
        layers = []
        
        # 입력층 -> 첫 번째 은닉층
        layers.append(nn.Linear(input_size, hidden_size))

        # 활성화 함수 및 드롭아웃 추가
        if activation_fn == 'relu':
            layers.append(nn.ReLU())
        elif activation_fn == 'sigmoid':
            layers.append(nn.Sigmoid())
        elif activation_fn == 'tanh':
            layers.append(nn.Tanh())
        
        if dropout_p > 0:
            layers.append(nn.Dropout(p=dropout_p))

        # 추가 은닉층 (num_hidden_layers가 2 이상일 경우)
        for _ in range(num_hidden_layers - 1):
            layers.append(nn.Linear(hidden_size, hidden_size))
            if activation_fn == 'relu':
                layers.append(nn.ReLU())
            elif activation_fn == 'sigmoid':
                layers.append(nn.Sigmoid())
            elif activation_fn == 'tanh':
                layers.append(nn.Tanh())
            
            if dropout_p > 0:
                layers.append(nn.Dropout(p=dropout_p))

        # 출력층
        layers.append(nn.Linear(hidden_size, num_classes))
        
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)


class MLP_Advanced(nn.Module): # 2-4 실험을 위한 모델을 별도로 정의하였습니다.
    def __init__(self, input_size=784, hidden_size=100, num_classes=10, num_layers=1, dropout_rate=0.0):
        super(MLP_Advanced, self).__init__()

        layers = []
        # 입력층 -> 첫 번째 은닉층
        layers.append(nn.Linear(input_size, hidden_size))
        layers.append(nn.ReLU())
        if dropout_rate > 0:
            layers.append(nn.Dropout(dropout_rate))

        # 추가 은닉층
        for _ in range(num_layers - 1): # num_layers가 1이면 이 루프는 실행되지 않음 (기본 MLP 구조)
            layers.append(nn.Linear(hidden_size, hidden_size))
            layers.append(nn.ReLU())
            if dropout_rate > 0:
                layers.append(nn.Dropout(dropout_rate))

        # 마지막 은닉층 -> 출력층
        layers.append(nn.Linear(hidden_size, num_classes))

        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)
