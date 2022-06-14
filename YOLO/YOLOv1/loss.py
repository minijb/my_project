import torch
from torch import nn, set_default_dtype
from utils import intersection_over_union

class YoloLoss(nn.Module):
    def __init__(self , S = 7 ,B = 2,C = 20):
        super(YoloLoss,self).__init__()
        self.mse = nn.MSELoss(reduction="sum")
        self.S = S 
        self.B = B
        self.C = C
        self.lambda_noobj = 0.5#就是置信度的那个
        self.lambda_coord = 5#就是用来测定长宽和位置的那个
        
    def forward(self, predicitons, targets):
        predicitons = predicitons.rshape(-1,self.S,self.S,self.C+self.B*5)
        #iou的计算
        iou_b1 = intersection_over_union(predicitons[...,21:25],targets[...,21:25])#位置信息
        iou_b2 = intersection_over_union(predicitons[...,26:30],targets[...,21:25])
        ious = torch.cat([iou_b1.unsqueeze(0),iou_b2.unsqueeze(0)],dim=0)
        #unsqueeze将tensor变为一行，之后按照行进行组合
        iou_maxes , best_box = torch.max(ious,dim=0)
        exists_box = targets[...,20].unsqueeze(3)#obji的置信度
        # ===========================
        # for box coordinates
        # ===========================
        box_predictions = exists_box * ( 
            (best_box*predicitons[...,26:30]+(1-best_box)*predicitons[...,21:25])
        )
        box_targets = exists_box * targets[...,21:25]
        #1e-6是为了增加稳定性, sign函数返回其+1 ， -1 也就是说返回原本的正负号！！！
        box_predictions[...,2:4] = torch.sign(box_predictions[...,2:4])  *torch.sqrt(
            torch.abs(box_predictions[...,2:4]+1e-6))
        # ===========================
        # for object loss
        # ===========================
        
        
        # ===========================
        # for no object loss
        # ===========================
            
        # ===========================
        # for class loss
        # ===========================
        
