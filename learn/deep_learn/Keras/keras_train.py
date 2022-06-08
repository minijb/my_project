from cgi import test
from pickletools import optimize
import tensorflow as tf
from tensorflow import keras
import numpy as np


def preprocess(x, y):
    x = tf.cast(x, dtype=tf.float32)/255-1
    y = tf.cast(y, dtype=tf.int32)
    return x, y


batch_size = 128

# 数据处理
(x, y), (x_val, y_val) = keras.datasets.cifar10.load_data()
y = tf.squeeze(y)  # 删除值为1的元素
y_val = tf.squeeze(y_val)
# print(y.shape)#(50000, 1)
y = tf.one_hot(y, depth=10)
y_val = tf.one_hot(y_val, depth=10)

# 包装为数据库形式
train_db = tf.data.Dataset.from_tensor_slices((x, y))
train_db = train_db.map(preprocess).shuffle(10000).batch(batch_size)
test_db = tf.data.Dataset.from_tensor_slices((x_val, y_val))
test_db = test_db.map(preprocess).batch(batch_size)

# sample = next(iter(train_db))
# print(sample[0].shape)


class MyDense(keras.layers.Layer):

    def __init__(self, inp_dim, outp_dim):
        super(MyDense, self).__init__()
        self.kernel = self.add_weight('w', [inp_dim, outp_dim])
        self.bias = self.add_weight('b', [outp_dim])

    def call(self, inputs, training=None):
        out = inputs @ self.kernel+self.bias
        return out


class MyNetwork(keras.Model):
    def __init__(self):
        super(MyNetwork, self).__init__()
        self.fc1 = MyDense(32*32*3, 256)
        self.fc2 = MyDense(256, 256)
        self.fc3 = MyDense(256, 128)
        self.fc4 = MyDense(128, 64)
        self.fc5 = MyDense(64, 10)

    def call(self, input, training=None):
        """_summary_

        Args:
            input (_type_): [b,32,32,3]
        """
        x = tf.reshape(input, [-1, 32*32*3])

        x = self.fc1(x)
        x = tf.nn.relu(x)
        x = self.fc2(x)
        x = tf.nn.relu(x)
        x = self.fc3(x)
        x = tf.nn.relu(x)
        x = self.fc4(x)
        x = tf.nn.relu(x)
        x = self.fc5(x)
        return x


if __name__ == '__main__':
    network = MyNetwork()
    network.compile(optimizer = keras.optimizers.Adam(learning_rate = 0.001)
                    ,loss = tf.losses.CategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])
    network.fit(train_db,epochs=3,validation_data = test_db,validation_freq =1)
    network.evaluate(test_db)
    network.save_weights('ckpt/weights.ckpt')
    
    del network
    network = MyNetwork()
    network.compile(optimizer = keras.optimizers.Adam(learning_rate = 0.001)
                    ,loss = tf.losses.CategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])
    network.load_weights('ckpt/weights.ckpt').expect_partial()
    network.evaluate(test_db)