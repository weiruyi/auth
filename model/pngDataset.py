"""
创建数据集，适用于一般分类，文件结构 data/label_name/img,每个种类单独存放一个文件夹
"""
import random

from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import transforms
import os
from PIL import Image

# 标签，---修改---
labels = {"yz":0, "zs":1, "ys":2, "zz":3}


# ---修改---
train_transform = transforms.Compose([
    # transforms.ToPILImage(),
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
])


class myDataset(Dataset):
    def __init__(self, data_dir, label_dir, transform=None):
        self.data_dir = data_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.data_dir, self.label_dir)
        self.img_path = os.listdir(self.path)
        self.transform = transform


    def __len__(self):
        return len(self.img_path)

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        img_item_path = os.path.join(self.data_dir, self.label_dir, img_name)
        img = Image.open(img_item_path)
        img = img.convert("RGB")
        if self.transform is not None:
            img = self.transform(img)
        label = labels[self.label_dir]
        return img, label


class TripletDataset(Dataset):
    def __init__(self, dataset):
        self.dataset = dataset
        self.total_dataset = self.dataset[0]
        for i in range(1, len(self.dataset)):
            self.total_dataset += self.dataset[i]

    def __getitem__(self, index):
        anchor, anchor_label = self.total_dataset[index]
        # 寻找正样本
        positive_index = random.randint(0, len(self.dataset[anchor_label])-1)
        positive, _ = self.dataset[anchor_label][positive_index]

        # 寻找负样本
        key_index = random.choice([i for i in range(len(self.dataset)) if i != anchor_label])
        negative_index = random.randint(0, len(self.dataset[key_index])-1)
        negative, _ = self.dataset[key_index][negative_index]
        return anchor, positive, negative, anchor_label

    def __len__(self):
        length = 0
        for i in range(len(self.dataset)):
            length+= len(self.dataset[i])
        return length


def creat_triple_Dataset(data_dir):
    label_dirs = os.listdir(data_dir)
    MyDataset = [i for i in range(len(label_dirs))]
    for i in range(len(label_dirs)):
        MyDataset[labels[label_dirs[i]]] = myDataset(data_dir, label_dirs[i], train_transform)
    triple_dataset = TripletDataset(MyDataset)
    return triple_dataset

def creatDataset(data_dir):
    label_dirs = os.listdir(data_dir)

    for i in range(len(label_dirs)):
        if i == 0:
            MyDataset = myDataset(data_dir, label_dirs[i], train_transform)
        else:
            MyDataset += myDataset(data_dir, label_dirs[i], train_transform)
    return MyDataset


# ----------------------------------------
class batchDataset(Dataset):
    def __init__(self, data_dir, label, batch_id, transform=None):
        self.data_dir = data_dir
        self.label = labels[label]
        self.batch_id = batch_id
        # self.path = os.path.join(self.data_dir, self.label_dir)
        self.img_path = os.listdir(self.data_dir)
        self.transform = transform

    def __len__(self):
        return len(self.img_path)

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        img_item_path = os.path.join(self.data_dir, img_name)
        img = Image.open(img_item_path)
        if self.transform is not None:
            img = self.transform(img)
        return img, self.label, self.batch_id


class batch_TripletDataset(Dataset):
    def __init__(self, dataset):
        self.dataset = dataset
        self.total_dataset = self.dataset[0][0]
        for i in range(0, len(self.dataset)):
            label_dataset = self.dataset[i]
            for j in range(len(label_dataset)):
                if i==0 and j==0:
                    pass
                self.total_dataset += self.dataset[i][j]

    def __getitem__(self, index):
        anchor, anchor_label, batch= self.total_dataset[index]
        # 寻找正样本
        positive_index_batch = random.choice([i for i in range(len(self.dataset[anchor_label])) if i != batch])
        postive_index = random.randint(0, len(self.dataset[anchor_label][positive_index_batch]) - 1)
        positive, _ = self.dataset[anchor_label][positive_index_batch][postive_index]

        # 寻找负样本
        key_index = random.choice([i for i in range(len(self.dataset)) if i != anchor_label])
        negative_batch = random.randint(0, len(self.dataset[key_index])-1)
        negative_index = random.randint(0, len(self.dataset[key_index][negative_batch])-1)
        negative, _ = self.dataset[key_index][negative_batch][negative_index]
        return anchor, positive, negative, anchor_label

    def __len__(self):
        length = 0
        for i in range(len(self.dataset)):
            length += len(self.dataset[i])
        return length


def create_batch_triple_Dataset(data_dir):
    label_dirs = os.listdir(data_dir)
    label_num = len(label_dirs)
    dataset = [0 for _ in range(label_num)]

    for i in range(label_num):
        label_dir = os.path.join(data_dir, label_dirs[i])
        label = label_dirs[i]
        batchs = os.listdir(label_dir)
        batch_num = len(batchs)
        dataset[i] = [0 for _ in range(batch_num)]
        for j in range(batch_num):
            batch_id = batchs[j]
            batch_dir = os.path.join(label_dir, batch_id)
            dataset[i][j] = batchDataset(batch_dir, label, j, train_transform)
    triple_dataset = batch_TripletDataset(dataset)
    return triple_dataset

def create_batch_Dataset(data_dir):
    label_dirs = os.listdir(data_dir)
    label_num = len(label_dirs)

    for i in range(label_num):
        label_dir = os.path.join(data_dir, label_dirs[i])
        label = label_dirs[i]
        batchs = os.listdir(label_dir)
        batch_num = len(batchs)
        for j in range(batch_num):
            if i==0 and j == 0:
                batch_id = batchs[j]
                batch_dir = os.path.join(label_dir, batch_id)
                dataset = batchDataset(batch_dir, label, j, train_transform)
            else:
                batch_id = batchs[j]
                batch_dir = os.path.join(label_dir, batch_id)
                dataset += batchDataset(batch_dir, label, j, train_transform)
    return dataset