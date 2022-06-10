import torch 
import torchvision

vgg16 = torchvision.models.vgg16(pretrained=False)
#方式1
# torch.save(vgg16,"vgg16.pth")

#把网络模型保存为一个字典,也就是说保存的是参数
torch.save(vgg16.state_dict(),"vgg16_m2.pth")