import torch
from torch import mode, nn
from torch.autograd import forward_ad
import torch.nn.functional as F

class SpatialPyramidPooling(nn.Module):
    def __init__(self, pool_sizes=[5, 9, 13]):
        super(SpatialPyramidPooling, self).__init__()
        self.maxpools = nn.ModuleList([
            # padding为pool_size//2保证了输出的size不变
            nn.MaxPool2d(pool_size,1,pool_size//2)  for pool_size in pool_sizes
        ])
    def forward(self,x):

        features = [maxpool(x) for maxpool in self.maxpools[::-1]]
        features = torch.cat(features+[x],dim=1)
        #有一个短接
        return features
        
# maxpools = nn.ModuleList([
#             nn.MaxPool2d(pool_size,1,pool_size//2)  for pool_size in [5, 9, 13]
#         ])


# x = torch.ones(1,3,416,416)
# a = [maxpool(x) for maxpool in maxpools]
# print(a[1].shape)