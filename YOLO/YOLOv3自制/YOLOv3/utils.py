import torch
from torch import nn
import numpy as np
import matplotlib.pyplot as plt

class DecodeBox(nn.Module):
    def __init__(self,anchors, num_classes, input_shape, anchors_mask = [[6,7,8], [3,4,5], [0,1,2]]):
        super(DecodeBox,self).__init__()
        self.anchors        = anchors
        self.num_classes    = num_classes
        self.bbox_attrs     = 5 + num_classes
        self.input_shape    = input_shape
        self.anchors_mask   = anchors_mask
        #-----------------------------------------------------------#
        #   13x13的特征层对应的anchor是[116,90],[156,198],[373,326]
        #   26x26的特征层对应的anchor是[30,61],[62,45],[59,119]
        #   52x52的特征层对应的anchor是[10,13],[16,30],[33,23]
        #-----------------------------------------------------------#

   
    def forward(self,input):
        pass
    
    def decode_box(self,inputs):
        """解码

        Args:
            inputs (list): 3*(1+4+class_nums),13,13 
            batch , 255 , 13/xx , 13
        """        
        outputs= []
        for i,input in inputs:
            batch_size = input.size(0)
            input_height = input.size(2)
            input_width = input.size(3)
        
            #----------------------------------
            # 也就是说第一种情况将图片分为13*13那么图片每一个grid cell的周长为32也就是stride
            # 输入416*416
            # stride_h = stride_w = 
            # (1) 416/13 = 32  (2)416/26 = 16  (3)416/54=8
            #----------------------------------
            
            stride_h = self.input_shape[0]/input_height
            stride_w = self.input_shape[1]/input_width
            # ===========================#
            # 修改anchor使之对应特征层的大小，以13*13为例也就是anchor_h/stride_h
            # ===========================#
            scaled_anchors = [(anchor_w/stride_w,anchor_h/stride_h) for anchor_w,anchor_h in self.anchors]
            
            # 分割数据  batch,3(anchor),13,13,85
            prediction = input.view(batch_size,len(self.anchors_mask[i]),
                                    self.bbox_attrs,input_height,input_width).permute(0,1,3,4,2).contiguous()
            #permute更换不同的维度
            # contiguous：view和permute只是在内存上没有改变只是更换了读取方式，这个函数让内存和读取的方式都为连续！！
            
            
            # 在85中分割数据
            # ===========================#
            # 调整先验框的中心位置
            # ===========================#
            x = torch.sigmoid(prediction[...,0])
            y = torch.sigmoid(prediction[...,1])
            # ===========================#
            # anchor宽高的调整参数
            # ===========================#
            w = prediction[...,2]
            h = prediction[...,3]
            # ===========================#
            # 置信度
            # ===========================#
            conf = prediction[...,4]
            # ===========================#
            # 种类
            # ===========================#
            pred_classed = prediction[...,5:]
            
            FloatTensor = torch.cuda.FloatTensor if x.is_cuda else torch.FloatTensor
            LongTensor = torch.cuda.LongTensor if x.is_cuda else torch.LongTensor
            
            # ===========================#
            # 生成网络和先验框中心（也就是cell左上角）,batch,3,13,13
            # ===========================#
            grid_x = torch.linspace(0,input_width-1,input_width).repeat(input_width,1).repeat(
                batch_size*len(self.anchors_mask[i]),1,1).view(x.shape).type(FloatTensor)
            grid_y = torch.linspace(0,input_height-1,input_height).repeat(input_height,1).repeat(
                batch_size*len(self.anchors_mask[i]),1,1).view(y.shape).type(FloatTensor)
            
            #anchor的宽高
            anchor_w = FloatTensor(scaled_anchors).index_select(1,LongTensor[0])
            anchor_h = FloatTensor(scaled_anchors).index_select(1, LongTensor([1]))
            anchor_w = anchor_w.repeat(batch_size, 1).repeat(1, 1, input_height * input_width).view(w.shape)
            anchor_h = anchor_h.repeat(batch_size, 1).repeat(1, 1, input_height * input_width).view(h.shape)
            #调整中心点和宽高
            pred_boxes          = FloatTensor(prediction[..., :4].shape)
            pred_boxes[..., 0]  = x.data + grid_x
            pred_boxes[..., 1]  = y.data + grid_y
            pred_boxes[..., 2]  = torch.exp(w.data) * anchor_w
            pred_boxes[..., 3]  = torch.exp(h.data) * anchor_h
            
            #用于将输出调整为相对于416，416大小
            _scale = torch.Tensor([stride_w,stride_h]*2).type(FloatTensor)
            output = torch.cat((pred_boxes.view(batch_size, -1, 4) / _scale,
                                conf.view(batch_size, -1, 1), pred_classed.view(batch_size, -1, self.num_classes)), -1)
            outputs.append(output.data)
        return outputs

