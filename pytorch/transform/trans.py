from torchvision import transforms
from PIL import Image
from torch.utils.tensorboard import SummaryWriter
from rich import print
import os
import cv2
img_path = r'pytorch/data/train/ants/0013035.jpg'
img = Image.open(img_path)
# img.show()
cv_img = cv2.imread(img_path)
tensor_trans =  transforms.ToTensor()
# print(type(tensor_trans(cv_img)))
#torch.Size([3, 512, 768])
img = tensor_trans(cv_img)
data = [1,2,3,4]
with SummaryWriter("pytorch/transform/logs") as writer:
    writer.add_image('test',img)