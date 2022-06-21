from collections import OrderedDict
from os import SEEK_CUR
import torch 
from torch import nn

from YOLOv3.darknet import darkNet53

def conv2d(filter_in, filter_out, kernel_size):
    pad = (kernel_size - 1) // 2 if kernel_size else 0
    return nn.Sequential(OrderedDict([
        ("conv", nn.Conv2d(filter_in, filter_out, kernel_size=kernel_size, stride=1, padding=pad, bias=False)),
        ("bn", nn.BatchNorm2d(filter_out)),
        ("relu", nn.LeakyReLU(0.1)),
    ]))

def make_last_layers(filter_list,in_filter,out_filters):
        m = nn.ModuleList([
            conv2d(in_filter,filter_list[0],1),
            conv2d(filter_list[0],filter_list[1],3),
            conv2d(filter_list[1],filter_list[0],1),
            conv2d(filter_list[0],filter_list[1],3),
            conv2d(filter_list[1],filter_list[0],1),
            conv2d(filter_list[0],filter_list[1],3),
            #调整通道数
            nn.Conv2d(filter_list[1],out_filters,kernel_size=1,stride=1,padding=0,bias=True)
        ])
        
        return m

class YoloBody(nn.Module):
    def __init__(self,config):
        super(YoloBody,self).__init__()
        self.config = config 
        self.backbone = darkNet53()
        out_filters = self.backbone.layers_out_filters
        #就是每个grad cell的输出 : 3*25 原文为3*(5+80)
        final_out_filter0 = len(config['yolo']['anchor'][0]) * (5+config["yolo"]["classes"])
        self.last_layer0 = make_last_layers([512,1024],out_filters[-1],final_out_filter0)
        
        final_out_filter1 = len(config['yolo']['anchor'][1]) * (5+config["yolo"]["classes"])
        self.last_layer1_conv = conv2d(512,256,1)
        self.last_layer1_upSample = nn.Upsample(scale_factor=2,mode='nearest')
        self.last_layer1 = make_last_layers([256,512],out_filters[-2]+256,final_out_filter1)
        
        
        final_out_filter2 = len(config['yolo']['anchor'][2]) * (5+config["yolo"]["classes"])
        self.last_layer2_conv = conv2d(256,128,1)
        self.last_layer2_upSample = nn.Upsample(scale_factor=2,mode='nearest')
        self.last_layer2 = make_last_layers([128,256],out_filters[-3]+128,final_out_filter2)
    