import os
import shutil
import random


# 数据集划分，20%测试集，80%训练集

# 定义数据集路径
dataset_dir = "/Users/lance/Desktop/Auth/dataset/melPng"
# divide_dir = "/Users/lance/Desktop/Auth/dataset/melDataset"
train_dir = os.path.join(dataset_dir, 'train')
val_dir = os.path.join(dataset_dir, 'val')

# 创建训练集和测试集文件夹
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# 获取每个类别的文件夹路径
classes = os.listdir(dataset_dir)
classes = [cls for cls in classes if not cls.startswith(".")]
classes = [cls for cls in classes if os.path.isdir(os.path.join(dataset_dir, cls)) and cls not in ['train', 'val']]

# 遍历每个类别并进行数据划分
for cls in classes:
    class_dir = os.path.join(dataset_dir, cls)
    images = os.listdir(class_dir)
    random.shuffle(images)  # 随机打乱

    # 计算训练集和验证集的分界点
    split_index = int(len(images) * 0.8)

    # 创建对应类别的训练集和验证集文件夹
    train_class_dir = os.path.join(train_dir, cls)
    val_class_dir = os.path.join(val_dir, cls)
    os.makedirs(train_class_dir, exist_ok=True)
    os.makedirs(val_class_dir, exist_ok=True)

    # 拷贝文件到训练集和验证集
    for img in images[:split_index]:
        shutil.copy(os.path.join(class_dir, img), os.path.join(train_class_dir, img))
    for img in images[split_index:]:
        shutil.copy(os.path.join(class_dir, img), os.path.join(val_class_dir, img))

print("数据集划分完成！")
