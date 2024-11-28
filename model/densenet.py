from torchvision.models import densenet121
import torch.nn as nn


def CreateDenseNet121(classes):
    model = densenet121(pretrained=True)
    num_ftrs = model.classifier.in_features
    model.classifier = nn.Linear(num_ftrs, classes, bias=True)
    return model

# model = CreateDenseNet121(26)
# print(model)