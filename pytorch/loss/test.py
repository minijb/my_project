import torch
from torch.nn import L1Loss
from torch import nn

input = torch.tensor([1,2,3],dtype=torch.float32)
target = torch.tensor([1,2,5],dtype=torch.float32)

inputs = torch.reshape(input,(1,1,1,3))
targets = torch.reshape(target,(1,1,1,3))

loss = L1Loss(reduction='sum')
result = loss(inputs,targets)

# print(result)

x = torch.tensor([0.1,0.2,0.3])
y = torch.tensor([1])
x = torch.reshape(x,[1,3])
loss_cross = nn.CrossEntropyLoss()
result = loss_cross(x,y)
print(result)