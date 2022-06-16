import torch
import os
import pandas as pd
from PIL import Image

from torch.utils.data import Dataset

class VOCDataset(Dataset):
    def __init__(self,csv_file,img_dir,label_dir,S=7,B=2,C=20,transform = None):
        self.annotations = pd.read_csv(csv_file)
        self.img_dir = img_dir
        self.label_dir = label_dir
        self.transform = transform
        self.S = S
        self.B = B
        self.C = C
        
    def __len__(self):
        return len(self.annotations)
    
    def __getitem__(self, index) :
        label_path = os.path.join(self.label_dir,self.annotations.iloc[index,1])
        boxes = []
        with open(label_path) as f:
            for label in f.readlines():
                temp =  [
                    float(x) if float(x) != int(float(x)) else int(x)
                    for x in label.replace("\n","").split()
                ]
                class_label , x, y ,width , height = temp
                boxes.append(temp)
                
        img_path = os.path.join(self.img_dir,self.annotations.iloc[index,0])
        image = Image.open(img_path)
        boxes = torch.tensor(boxes)
        #如果需要处理图像和数据那么就自己传入即可
        if self.transform:
            image , boxes = self.transform(image,boxes)
        #标签矩阵
        label_matrix = torch.zeros((self.S,self.S, self.C + 5 * self.B))
        #这里的标签是全局意义上的  ，我们需要转换为特定格子里的
        for box in boxes:
            class_label,x,y,width,height = box.tolist()
            class_label = int(class_label)#保证class_label是整数
            # i,j represents the cell row and cell column
            i,j = int(self.S*y),int(self.S*x)
            #两者是cell内部的x,y
            x_cell , y_cell = self.S*x - j,self.S*y-i
            width_cell ,height_cell = (
                width*self.S,
                height*self.S
            )
            if label_matrix[i,j,20] == 0 :
                label_matrix[i,j,20] == 1
                box_coordinates = torch.tensor(
                    [x_cell,y_cell,width_cell,height_cell]
                )
                label_matrix[i,j,21:25] = box_coordinates
                label_matrix[i,j,class_label] = 1
        return image,label_matrix