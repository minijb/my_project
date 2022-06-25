import torch
from torch import nn
import numpy as np

class DecodeBox(nn.Module):
    def __init__(self):
        super(DecodeBox,self).__init__()
        
    def forward(self,input):
        """解码

        Args:
            input (list): 3*(1+4+class_nums),13,13 
        """        
        pass