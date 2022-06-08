import tensorflow as tf
from keras import layers, Sequential, Model


class BasicBlock(layers.Layer):
    def __init__(self, filter_num, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = layers.Conv2D(
            filter_num, (3, 3), strides=stride, padding='same')
        self.bn1 = layers.BatchNormalization()
        self.relu = layers.Activation('relu')
        self.conv2 = layers.Conv2D(
            filter_num, (3, 3), strides=1, padding='same')
        self.bn2 = layers.BatchNormalization()

        # 此步就是短接层，目的就是让两者的特征图可以相加！！！！
        if stride != 1:
            self.downsample = Sequential()
            self.downsample.add(layers.Conv2D(
                filter_num, (1, 1), strides=stride))
            self.downsample.add(layers.BatchNormalization())
        else:
            self.downsample = lambda x: x
        self.stride = stride

    def call(self, inputs, training=None):

        residual = self.downsample(inputs)

        out = self.conv1(inputs)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        output = layers.add([out, residual])
        output = self.relu(output)
        return output


class ResNet(Model):
    # [2,2,2,2]
    def __init__(self, layer_dims, num_classes=100):
        super(ResNet, self).__init__()
        # 预处理层
        self.stem = Sequential([
            layers.Conv2D(64, (3, 3), strides=(1, 1)),
            layers.BatchNormalization(),
            layers.Activation('relu'),
            layers.MaxPool2D(pool_size=(2, 2), strides=(1, 1), padding='same')
        ])

        # block层
        self.layer1 = self.build_resblock(64, layer_dims[0])
        self.layer2 = self.build_resblock(128, layer_dims[1], stride=2)
        self.layer3 = self.build_resblock(256, layer_dims[2], stride=2)
        self.layer4 = self.build_resblock(512, layer_dims[3], stride=2)

        # output : [b,512,h,w]自适应的确认输入全连接层的大小
        self.avgpool = layers.GlobalAveragePooling2D()

        # 全连接层
        self.fc = layers.Dense(num_classes)

    def call(self, inputs, training=None):
        x = self.stem(inputs)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        # [b,c]
        x = self.avgpool(x)
        # [b,100]
        x = self.fc(x)

        return x

    def build_resblock(self, filter_num, blocks, stride=1):
        res_blocks = Sequential()
        res_blocks.add(BasicBlock(filter_num, stride))
        for _ in range(1, blocks):
            res_blocks.add(BasicBlock(filter_num, stride=1))
        return res_blocks


def resNet18():
    return ResNet([2, 2, 2, 2])


def resNet34():
    return ResNet([3, 4, 6, 3])



