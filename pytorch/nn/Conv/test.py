from turtle import forward
from black import out
import torch
from torchvision import datasets,transforms
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import nn

from rich import print

datasets = datasets.CIFAR10("./pytorch/transform/dataset",train=True , transform=transforms.ToTensor())

dataloader = DataLoader(datasets , batch_size=64)

class conv_model(nn.Module):
    def __init__(self):
        super(conv_model,self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=6 , kernel_size=3,stride=1)
    
    def forward(self, x ):
        x = self.conv1(x)
        return x
    
    
model = conv_model()

writer  = SummaryWriter("pytorch/nn/Conv/logs")


step = 0 
for step,data in enumerate(dataloader):
    imgs ,targets = data
    output = model(imgs)
    output = torch.reshape(output,(-1,3,30,30))
    if step % 10 == 0:
        print(imgs.shape,output.shape,end=' ')
        writer.add_images("imgs",imgs,step)
        writer.add_images("output",output,step)
        step +=1 
        
writer.close()