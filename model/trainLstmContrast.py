import torch

from Lstm import LSTMNetwork
from npyDataset import createTripleDataset, creatDataset
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim


# 示例参数
input_size = 128  # 输入特征维度
hidden_size = 128  # LSTM隐藏层大小
num_layers = 6  # LSTM层数
output_size = 256  # 输出维度

# 初始化网络
model = LSTMNetwork(input_size, hidden_size, num_layers, output_size)

# dataset = createTripleDataset(r"D:\hnu\Auth\dataset\melNpy_cyw\train")
dataset = creatDataset(r"D:\hnu\Auth\dataset\melNpy_cyw\train")
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

# valDataset = createTripleDataset(r"D:\hnu\Auth\dataset\melNpy_cyw\val")
valDataset = creatDataset(r"D:\hnu\Auth\dataset\melNpy_cyw\val")
valDataloader = DataLoader(valDataset, batch_size=4, shuffle=True)

# criterion = nn.TripletMarginLoss(margin=1)
# optimizer = optim.SGD(model.parameters(), lr=0.005)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.005)

epochs = 100
best_weights = model.state_dict()
model.train()
bestLoss = 9999
for epoch in range(epochs):
    trainingLoss = 0.
    trainNum = 0
    trainCorrect = 0
    for (i, batch) in enumerate(dataloader):
        # anchor, postive, negative, anchorLabel, anchorPos = batch
        anchor, anchorLabel, anchorPos = batch
        anchorOutput = model(anchor)
        loss = criterion(anchorOutput, anchorLabel)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        _, predicted = torch.max(anchorOutput.data, 1)
        trainCorrect += (predicted == anchorLabel).sum().item()
        trainingLoss += loss.item()
        trainNum += anchorLabel.size(0)
        trainingAcc = trainCorrect/trainNum
        print('\r', f'[{i}/{len(dataloader)}, loss:{loss:.6f}, trainAcc:{trainingAcc:.6f} ]')
    print(f'\nEpoch [{epoch + 1}/{epochs}], Loss: {trainingLoss / trainNum:.6f},train_Acc:{trainingAcc:.6f}')
    if loss < bestLoss:
        best_weights = model.state_dict()
        best_loss = loss
        torch.save(best_weights, './weights/best_test.pth')

    # 测试集
    val_acc = 0.
    val_correct = 0
    val_num = 0
    model.eval()
    for (val_inputs, val_labels, _) in valDataloader:
        # val_inputs, val_labels = val_inputs.to(device), val_labels.to(device)

        val_outputs = model(val_inputs)

        _, val_pred = torch.max(val_outputs.data, 1)
        val_correct += (val_pred == val_labels).sum().item()
        val_num += val_labels.size(0)

    val_acc = val_correct / val_num
    print(f'val_Acc:{val_acc:.4f}')

print('Training finished.')