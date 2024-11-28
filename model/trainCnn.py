import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from pngDataset import creatDataset
from densenet import CreateDenseNet121


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# device = torch.device("mps")
print(device)

dataset = creatDataset(r"D:\hnu\Auth\dataset\melPng_cyw\train")
# dataset = create_batch_Dataset('./dataset/new3/train')
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)


val_dataset = creatDataset(r"D:\hnu\Auth\dataset\melPng_cyw\val")
val_dataloader = DataLoader(val_dataset, batch_size=8, shuffle=True)




model = CreateDenseNet121(4)
# model.load_state_dict(torch.load('./weights/last_contrast_vivo40.pth', map_location=torch.device('cpu')))
# model.classifier = nn.Linear(1024, 26)
model= model.to(device)

criterion = nn.CrossEntropyLoss()

# 定义优化器
optimizer = optim.SGD(model.parameters(), lr=0.005)

# 训练模型
num_epochs = 100

best_loss = 99999
best_weights = model.state_dict()

for epoch in range(num_epochs):
    training_loss = 0.
    training_acc = 0.
    train_correct = 0
    train_num = 0
    model.train()
    for (i, batch) in enumerate(dataloader):
        inputs, labels = batch
        inputs, labels = inputs.to(device), labels.to(device)

        outputs = model(inputs)
        # 计算损失
        loss = criterion(outputs, labels)

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        _, predicted = torch.max(outputs.data, 1)
        train_correct += (predicted == labels).sum().item()
        training_loss += loss.item()
        train_num += labels.size(0)
        training_acc = train_correct / train_num
        print('\r',f' [{i}/{len(dataloader)}], Loss: {loss:.6f}, train_Acc:{training_acc:.6f}', end='')

    print(f'\nEpoch [{epoch + 1}/{num_epochs}], Loss: {training_loss/train_num:.6f},train_Acc:{training_acc:.6f}')
    if loss < best_loss:
        best_weights = model.state_dict()
        best_loss = loss
        torch.save(best_weights, './weights/best_test_png.pth')

    # 测试集
    val_acc = 0.
    val_correct = 0
    val_num = 0
    model.eval()
    for (val_inputs, val_labels) in val_dataloader:
        val_inputs, val_labels = val_inputs.to(device), val_labels.to(device)

        val_outputs = model(val_inputs)

        _, val_pred = torch.max(val_outputs.data, 1)
        val_correct += (val_pred == val_labels).sum().item()
        val_num += val_labels.size(0)

    val_acc = val_correct / val_num
    print(f'val_Acc:{val_acc:.4f}')

print('Training finished.')
# torch.save(model.state_dict(), './weights/last_classify_wry.pth')


