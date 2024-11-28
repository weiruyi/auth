import torch
import torch.nn as nn
import numpy as np


class LSTMNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMNetwork, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # 6层LSTM
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

        # 全连接层
        self.fc = nn.Linear(hidden_size, output_size)
        self.fc2 = nn.Linear(output_size, 1024)
        self.fc3 = nn.Linear(1024, 2)

        # ReLU激活层
        self.relu = nn.ReLU()

    def forward(self, x):
        # 初始化隐藏状态和细胞状态
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # LSTM前向传播
        out, _ = self.lstm(x, (h0, c0))

        # 取最后一个时间步的输出
        out = out[:, -1, :]

        # 全连接层
        out = self.fc(out)
        out = self.fc2(out)
        out = self.fc3(out)

        # ReLU激活
        out = self.relu(out)
        return out


# # 示例参数
# input_size = 128  # 输入特征维度
# hidden_size = 128  # LSTM隐藏层大小
# num_layers = 6  # LSTM层数
# output_size = 256  # 输出维度
#
# # 初始化网络
# model = LSTMNetwork(input_size, hidden_size, num_layers, output_size)

# data = np.load("/Users/lance/Downloads/Auth/dataset/melNpy/train/ys/U1.94.0_9_1_mel.npy").T
# input_tensor = torch.from_numpy(data).float().unsqueeze(0)
# out = model(input_tensor)
# print(out)
