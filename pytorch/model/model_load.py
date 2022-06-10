import torch
from torchvision import models
#方式1
# model = torch.load("vgg16.pth")

#方式2
vgg16 = models.vgg16(pretrained=False)

vgg16.load_state_dict(torch.load("vgg16_m2.pth"))
print(vgg16.classifier[0].bias)