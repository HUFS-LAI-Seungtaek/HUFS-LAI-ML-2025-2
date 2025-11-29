# 
# imports 완료 + 하드웨어 확인 출력
import os, time, csv, random
from collections import Counter
from typing import List, Tuple, Dict, Any

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from datasets import load_dataset
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")
if device.type == "cuda":
    try:
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    except Exception:
        pass
