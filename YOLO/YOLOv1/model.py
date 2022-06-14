import torch
import torch.nn as nn

model_config = [
    # kernel_size output_size stride padding
    (7, 64, 2, 3),
    "M",
    (3, 192, 1, 1),
    "M",
    (1, 128, 1, 0),
    (3, 256, 1, 1),
    (1, 256, 1, 0),
    (3, 512, 1, 1),
    "M",
    [(1, 256, 1, 0), (3, 512, 1, 1), 4],
    (1, 512, 1, 0),
    (3, 1024, 1, 1),
    "M",
    [(1, 512, 1, 0), (3, 1024, 1, 1), 2],
    (3, 1024, 1, 1),
    (3, 1024, 2, 1),
    (3, 1024, 1, 1),
    (3, 1024, 1, 1),
]


class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, **kwargs):
        super(CNNBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)
        self.batchnorm = nn.BatchNorm2d(out_channels)
        self.leakyrelu = nn.LeakyReLU(0.1)

    def forward(self, x):
        x = self.conv(x)
        x = self.batchnorm(x)
        x = self.leakyrelu(x)
        return x


class Yolov1(nn.Module):
    def __init__(self, in_channels=3, **kwargs):
        super(Yolov1, self).__init__()
        self.model_config = model_config
        self.in_channels = in_channels
        self.darknet = self._create_conv_layers(self.model_config)
        self.fcs = self._create_fcs(**kwargs)

    def forward(self, x):
        x = self.darknet(x)
        x = torch.flatten(x, start_dim=1)
        x = self.fcs(x)
        return x
        # Flattens input by reshaping it into a one-dimensional tensor.
        # start=也就是说按照那招第一维度进行reshape

    def _create_conv_layers(self, architecture):
        layers = []
        in_channels = self.in_channels

        for item in architecture:
            if type(item) == tuple:
                layers += [CNNBlock(
                    in_channels, item[1], kernel_size=item[0],
                    stride=item[2], padding=item[3])]
                in_channels = item[1]
            elif type(item) == str:
                layers += [nn.MaxPool2d(kernel_size=2,stride=2)]
            elif type(item) == list:
                conv1 = item[0]
                conv2 = item[1]
                num_repeat = item[2] 
                
                for _ in range(num_repeat):
                    layers+=[
                        CNNBlock(
                        in_channels, conv1[1], kernel_size=conv1[0],
                        stride=conv1[2], padding=conv1[3]),
                        CNNBlock(
                        conv1[1], conv2[1], kernel_size=conv2[0],
                        stride=conv2[2], padding=conv2[3]),
                        ]
                    in_channels = conv2[1]
        
        return nn.Sequential(*layers)
    
    def _create_fcs(self,split_size,num_boxes,num_classes):
        S,B,C = split_size,num_boxes,num_classes
        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024*S*S,496),#缩短时间---origin paper:4096
            nn.Dropout(0.0),
            nn.LeakyReLU(0.1),
            nn.Linear(496,S*S*(C+B*5)),#origin 7*7*(5*2+20)因为用不到那么多的类别所以缩小了参数!!!
            #感觉主要是思想符合就可以，细节可以微调
        )
        
def test(S = 7 , B = 2 , C=20):
    model = Yolov1(split_size = S,num_boxes=B,num_classes=C)
    x = torch.randn((2,3,448,448))
    print(model)
    out = model(x)
    print(out.shape)
    
    
