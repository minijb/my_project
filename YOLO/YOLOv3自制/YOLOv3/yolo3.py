from torch import nn
import torch
from YOLOv3.yolo3_md import conv2d 

from darknet import darkNet53

class YOLOv3(nn.Module): 
    def __init__(self,anchor_masks,classes_num):
        """ YOLOv3
        Args:
            anchor_masks (list): the anchors shape from kmeans
            classes_num (int): the number of classes 
        """        
        super(YOLOv3,self).__init__()
        self.backbone = darkNet53()
        # ===========================#
        # convolutional set
        # 五部分: (kernel_size) 1,3,1,3,1
        # ===========================#
        
        #conv1--------------------------------------------------------
        self.convolutionalSet0  = self._createConvoltionalSet(1024,512)
        #get 13,13,weneed
        self.branch_out0 = self._createBranchOut(512,1024,len(anchor_masks[0]*(classes_num+5)))
        self.branch_down0 =self._createBranchDown(512,216)
        
        #conv2-------------------------------------------------------
        
        
    def forward(self,x):
        """_summary_

        Returns:
            out0: [13,13,need]
            
        """        
        # out2 : [52,52,256]  out1: [ 26,26,512]  out0:[13,13,1024]
        out2,out1,out0 = self.backbone(x)
        
        out0 = self.convolutionalSet0(out0)
        out0_out = self.branch_out0(out0)#[13,13,need]
        out0_down = self.branch_down0(out0)#[26,26,216]
        out0_down = torch.cat([out0_down,out1],1)#[26,26,728]
        
        
        
        return out0
        
        
    def conv2d(channel_in,channel_out,kernel_size):
        pad = (kernel_size - 1) // 2 if kernel_size else 0
        return nn.Sequential([
            nn.Conv2d(channel_in,channel_out,kernel_size=kernel_size,stride=1,padding=pad,bias=False),
            nn.BatchNorm2d(channel_out),
            nn.LeakyReLU(0.1)
        ])
    
    def _createConvoltionalSet(self,channel_0,channel_1):
        return nn.Sequential([
            self.conv2d(channel_0,channel_1,1),
            self.conv2d(channel_1,channel_0,3),
            self.conv2d(channel_0,channel_1,1),
            self.conv2d(channel_1,channel_0,3),
            self.conv2d(channel_0,channel_1,1),
        ])
        
    def _createBranchOut(self,channel_in,channel_out,channel_need):
        return nn.Sequential([
            self.conv2d(channel_in,channel_out,3),
            nn.Conv2d(channel_out,channel_need,kernel_size=1,padding=0,stride=1,bias=True)
        ])

    def _createBranchDown(self,channel_in,channel_out):
        return nn.Sequential([
            conv2d(channel_in,channel_out,1),
            nn.Upsample(scale_factor=2,mode='nearest')
        ])
        
    
        