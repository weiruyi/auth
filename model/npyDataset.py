import os
import random
import numpy as np
import torch
from torch.utils.data import Dataset

userIndexs = {"yz":0, "zs":1}


class npyDataset(Dataset):
    def __init__(self, filename):
        self.filename = filename
        self.npys = os.listdir(filename)

    def __getitem__(self, index):
        npy = self.npys[index]
        npyPath = os.path.join(self.filename, npy)
        data = np.load(npyPath).T
        dataTensor = torch.from_numpy(data)
        labels = npy.split("-")
        user = labels[0]
        userIndex = userIndexs[user]
        pos = labels[1]
        return dataTensor, userIndex, pos

    def __len__(self):
        return len(self.npys)

class TripleDataset(Dataset):
    def __init__(self, datasetList):
        self.datasetList = datasetList
        self.dataset = datasetList[0]
        for i in range(1, len(datasetList)):
            self.dataset += datasetList[i]

    def __getitem__(self, index):
        anchor, anchorLabel, anchorPos = self.dataset[index]
        #正样本
        postiveIndex = random.randint(0, len(self.datasetList[anchorLabel])-1)
        postive, _,_ = self.datasetList[anchorLabel][postiveIndex]
        #负样本
        userIndex = random.choice([i for i in range(len(self.datasetList)) if i != anchorLabel])
        negativeIndex = random.randint(0, len(self.datasetList[userIndex])-1)
        negative, _,_ = self.datasetList[userIndex][negativeIndex]
        return anchor, postive, negative, anchorLabel, anchorPos

    def __len__(self):
        return len(self.dataset)


def createTripleDataset(filename):
    users = os.listdir(filename)
    userNums = len(users)
    datasetList = [i for i in range(userNums)]
    for i in range(userNums):
        user = users[i]
        userIndex = userIndexs[user]
        userFileName = os.path.join(filename, user)
        datasetList[userIndex] = npyDataset(userFileName)
    tripleDataset = TripleDataset(datasetList)
    return tripleDataset

def creatDataset(filename):
    users = os.listdir(filename)
    userNums = len(users)
    for i in range(userNums):
        user = users[i]
        userFileName = os.path.join(filename, user)
        if i == 0:
            MyDataset = npyDataset(userFileName)
        else:
            MyDataset += npyDataset(userFileName)
    return MyDataset