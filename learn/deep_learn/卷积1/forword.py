from functools import total_ordering
from numpy import gradient
import tensorflow as tf
from tensorflow.keras import datasets
from tensorflow import keras


(x, y), (x_test,y_test) = datasets.mnist.load_data()

x = tf.convert_to_tensor(x, dtype=tf.float32)/255  # 将范围转化为0-1
y = tf.convert_to_tensor(y, dtype=tf.int32)

x_test = tf.convert_to_tensor(x_test, dtype=tf.float32)/255  # 将范围转化为0-1
y_test = tf.convert_to_tensor(y_test, dtype=tf.int32)

print(x.shape, y.shape)
#(60000, 28, 28) (60000,)
print(tf.reduce_min(x), tf.reduce_max(x))
print(tf.reduce_min(y), tf.reduce_max(y))
'''
tf.Tensor(0.0, shape=(), dtype=float32) tf.Tensor(255.0, shape=(), dtype=float32)
tf.Tensor(0, shape=(), dtype=int32) tf.Tensor(9, shape=(), dtype=int32)
'''
# 按照数据集环缝  每个数据集128个样本
train_db = tf.data.Dataset.from_tensor_slices((x, y)).batch(128)
train_iter = iter(train_db)
test_db = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(128)
test_iter = iter(test_db)
# sample = next(train_iter)
# print('batch:',sample[0].shape,sample[1].shape)#batch: (128, 28, 28) (128,)

# 降维过程[b,784]=>[b,512]=>[b,10]
# w:[dim_in,dim_out] b[dim_out]
w1 = tf.Variable(tf.random.truncated_normal([784, 256],stddev=0.1))
b1 = tf.Variable(tf.zeros([256]))
w2 = tf.Variable(tf.random.truncated_normal([256, 128],stddev=0.1))
b2 = tf.Variable(tf.zeros([128]))
w3 = tf.Variable(tf.random.truncated_normal([128, 10],stddev=0.1))
b3 = tf.Variable(tf.zeros([10]))

learn_rate = 0.005

for epoch in range(100):#总体次数
    for step, (x, y) in enumerate(train_db):#数据集迭代
        # h1 = w1@x1+b1
        #(128, 28, 28) (128,)
        # 维度变换
        # x[b,28*28]
        x = tf.reshape(x, [-1, 28*28])

        # 把需要计算梯度的公式放在with内部
        with tf.GradientTape() as tape:
            # [b,784]@[784,256]+[256]=>[b,256]+[256] ,,, +自动broadcast_to
            h1 = x@w1+b1
            h1 = tf.nn.relu(h1)
            h2 = h1@w2 + b2
            h2 = tf.nn.relu(h2)
            out = h2@w3+b3

            # compute loss
            # out:[b,10] y:[b]
            y_onehot = tf.one_hot(y, depth=10)

            loss = tf.square(y_onehot-out)  # [10]
            loss = tf.reduce_mean(loss)

        # compute gradients
        grads = tape.gradient(loss, [w1, b1, w2, b2, w3, b3])
        # print(grads)
        #w1 = w1 - lr*w1_grad
        # w1 = w1 - learn_rate*grads[0]
        # b1 = b1 - learn_rate*grads[1]
        # w2 = w2 - learn_rate*grads[2]
        # b2 = b2 - learn_rate*grads[3]
        # w3 = w3 - learn_rate*grads[4]
        # b3 = b3 - learn_rate*grads[5]
        #原地更新
        w1.assign_sub(learn_rate*grads[0])
        b1.assign_sub(learn_rate*grads[1])
        w2.assign_sub(learn_rate*grads[2])
        b2.assign_sub(learn_rate*grads[3])
        w3.assign_sub(learn_rate*grads[4])
        b3.assign_sub(learn_rate*grads[5])
        
        #初始化的时候需要指定均值为0.1否则梯度爆炸
        # if step % 100 == 0:
        #     print(epoch,':',step, 'loss', float(loss))
    total_correct ,total_num = 0,0
    for step,(x,y) in enumerate(test_db):
        #前向传播
        x = tf.reshape(x,[-1,28*28])
        
        h1 = tf.nn.relu(x@w1+b1)
        h2 = tf.nn.relu(h1@w2+b2)
        out = h2@w3+b3
        #out:[b,10]
        #prob:0-1
        prob = tf.nn.softmax(out,axis=1)
        #pred:[b,10]->[b]
        pred = tf.cast(tf.argmax(prob,axis=1),tf.int32)
        correct = tf.cast(tf.equal(pred,y),tf.int32)
        correct = tf.reduce_sum(correct)
        total_num += x.shape[0]
        total_correct += int(correct)
    acc =  total_correct/total_num
    print('total accuracy:',acc)
        
        