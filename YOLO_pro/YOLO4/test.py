import torch
from torch import mode, nn
import torch.nn.functional as F


class Mish(nn.Module):
    def __init__(self):
        super(Mish, self).__init__()
    def foward(self, x):
        return x*torch.tanh(F.softplus(x))
    
# ===========================#
# 主干部分的卷积快
# ===========================#
class BasicConv(nn.Module):
    def __init__(self,in_channels,out_channels,kernel_size,strides=1):
        super(BasicConv,self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, strides, kernel_size//2, bias=False)
        self.bn = nn.BatchNorm2d(out_channels)
        self.activation = Mish()
    def forward(self,x):
        x = self.conv(x)
        x = self.bn(x)
        x = F.mish(x)
        return x
        
# ===========================#
# 主干部分残差块
# ===========================#

class ResBlock(nn.Module):
    #nn.Identity()就是输入什么就输出什么的占位模块
    def __init__(self,channels,hidden_channels=None,residual_activation=nn.Identity()):
        super(ResBlock,self).__init__()
        if hidden_channels is None:
            hidden_channels = channels
        self.block = nn.Sequential(
            BasicConv(channels,hidden_channels,1),
            BasicConv(hidden_channels,channels,3)
        )
        
    def forward(self,x):
        return x + self.block(x)


# ===========================#
# 主干的模块
# ===========================#

'''
注意点：第一次之后一层卷积且图的储存不修改
输入：输入的通道数，输出的通道数，part2需要卷积的次数，是否是第一层（第一层的特征曾shape不变化）
'''
class ResBlock_body(nn.Module):
    def __init__(self,in_channels,out_channels,num_blocks,first=False) -> None:
        super(ResBlock_body,self).__init__()
        
        #卷积下采样
        self.downSample_conv = BasicConv(in_channels,out_channels,3,2)
        
        if first:
            #第一层只需要改变通道数不需要改变shape
            self.branch_conv0 = BasicConv(out_channels,out_channels,1)
            self.branch_conv1 = BasicConv(out_channels,out_channels,1)
            self.blcoks_conv = nn.Sequential(
                ResBlock(channels=out_channels,hidden_channels=out_channels//2),
                BasicConv(out_channels, out_channels, 1)
            )
            #注：这里进行了因为进行了堆叠所以需要*2
            self.concat_conv = BasicConv(out_channels*2, out_channels, 1)
        else:
            self.branch_conv0 = BasicConv(out_channels,out_channels//2,1)
            self.branch_conv1 = BasicConv(out_channels,out_channels//2,1)
            self.blcoks_conv = nn.Sequential(
                 *[ResBlock(out_channels//2) for _ in range(num_blocks)],
                BasicConv(out_channels//2, out_channels//2, 1)
            )
            self.concat_conv = BasicConv(out_channels, out_channels, 1)
            
    def forward(self,x):
        x = self.downSample_conv(x)
        
        x0 = self.branch_conv0(x)
        x1 = self.branch_conv1(x)
        x1= self.blcoks_conv(x1)
        x = torch.cat([x1,x0],dim=1)
        x = self.concat_conv(x)
        return x
    


# ===========================#
# 主体模块
# ===========================#
class CSPDarkNet(nn.Module):
    def __init__(self, layers):
        super(CSPDarkNet, self).__init__()
        self.inplanes = 32
        self.conv1 = BasicConv(3, self.inplanes, kernel_size=3, strides=1)
        self.feature_channels = [64, 128, 256, 512, 1024]

        self.stages = nn.ModuleList([
            ResBlock_body(self.inplanes, self.feature_channels[0], layers[0], first=True),
            ResBlock_body(self.feature_channels[0], self.feature_channels[1], layers[1], first=False),
            ResBlock_body(self.feature_channels[1], self.feature_channels[2], layers[2], first=False),
            ResBlock_body(self.feature_channels[2], self.feature_channels[3], layers[3], first=False),
            ResBlock_body(self.feature_channels[3], self.feature_channels[4], layers[4], first=False)
        ])

        self.num_features = 1


    def forward(self, x):
        x = self.conv1(x)

        x = self.stages[0](x)
        x = self.stages[1](x)
        out3 = self.stages[2](x)
        out4 = self.stages[3](out3)
        out5 = self.stages[4](out4)

        return out3, out4, out5

def darknet53(**kwargs):
    model = CSPDarkNet([1, 2, 8, 8, 4])
    return model


text = torch.ones(1,3,416,416)
model = darknet53()
out1,out2,out3= model(text)
print(out1.shape)