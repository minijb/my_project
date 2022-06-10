import torch
from torchvision import models,datasets
from torchvision.models import vgg

vgg16_False = models.vgg16(pretrained=False)#仅仅加载模型
vgg16_True = models.vgg16()#并下载参数
print('ok')

vgg16_True.add_module('add_liner',torch.nn.Linear(1000,10))
#如何在一个Sequential中添加model
vgg16_True.classifier.add_module('add_liner',torch.nn.Linear(1000,10))
print(vgg16_True)