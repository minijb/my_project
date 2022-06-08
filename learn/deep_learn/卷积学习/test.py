from functools import reduce
import re
import tensorflow as tf 
from keras import layers,optimizers,datasets,Sequential
from Resnet import resNet18

tf.random.set_seed(2345)

conv_layers = [
    #unity 1
    layers.Conv2D(64,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.Conv2D(64,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.MaxPool2D(pool_size=[2,2],strides=2,padding='same'),
    
    #unity 2
    layers.Conv2D(128,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.Conv2D(128,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.MaxPool2D(pool_size=[2,2],strides=2,padding='same')  ,
    
    #unity 3
    layers.Conv2D(256,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.Conv2D(256,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.MaxPool2D(pool_size=[2,2],strides=2,padding='same') ,
    
    #unity 4
    layers.Conv2D(512,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.Conv2D(512,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.MaxPool2D(pool_size=[2,2],strides=2,padding='same') ,
    
    #unity 5
    layers.Conv2D(512,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.Conv2D(512,kernel_size=[3,3],padding='same',activation=tf.nn.relu),
    layers.MaxPool2D(pool_size=[2,2],strides=2,padding='same') 
]

def preprocess(x,y):
    x = tf.cast(x,tf.float32)/255
    y = tf.cast(y,tf.int32)
    return x,y

def print_sample_shape(db):
    sample = next(iter(db))
    print(sample[0].shape,sample[1].shape)




def main():
    
    (x, y), (x_test, y_test) = datasets.cifar100.load_data()
    y =tf.squeeze(y , axis=1)
    y_test =tf.squeeze(y_test , axis=1)
    #(50000,32,32,3)  (10000,32,32,3)

    train_db = tf.data.Dataset.from_tensor_slices((x,y))
    train_db = train_db.shuffle(10000).map(preprocess).batch(64)

    test_db = tf.data.Dataset.from_tensor_slices((x_test,y_test))
    test_db = test_db.map(preprocess).batch(64)

    print_sample_shape(train_db)#(64, 32, 32, 3) (64,)
    
    conv_net = Sequential(conv_layers)
    conv_net.build(input_shape=[None,32,32,3])
    # x = tf.random.normal([4,32,32,3])# ==> (4, 1, 1, 512)
    # out = conv_net(x)
    # print(out.shape)
    
    fc_net = Sequential([
        layers.Dense(256,activation=tf.nn.relu),
        layers.Dense(128,activation=tf.nn.relu),
        layers.Dense(100,activation=None),
    ])
    
    conv_net.build(input_shape=[None,32,32,3])
    #(b, 1, 1, 512) == > (b , 512)
    fc_net.build(input_shape=[None,512])
    
    
    #优化器
    optimizer = optimizers.Adam(learning_rate=1e-4)
    #需要梯度的部分为conv+fc两部分
    variables = conv_net.trainable_variables  + fc_net.trainable_variables
    
    for epoch in range(50):
        for step , (x,y) in enumerate(train_db):
            
            with tf.GradientTape() as tape:
                out = conv_net(x)
                out = tf.reshape(out ,[-1,512])
                logits = fc_net(out)
                #[b] => b,100
                y_onehot = tf.one_hot(y,depth=100)
                loss = tf.losses.categorical_crossentropy(y_onehot,logits,from_logits=True)
                loss = tf.reduce_mean(loss)
                
            
            grads = tape.gradient(loss,variables)
            optimizer.apply_gradients(zip(grads,variables))
            
            if step %100 ==0:
                print(epoch, step , float(loss))
            
        total_num = 0
        total_correct = 0
        for x,y in test_db:
            out = conv_net(x)
            out = tf.reshape(out ,[-1,512])
            logits = fc_net(out)
            prob = tf.nn.softmax(logits,axis=1)
            pred = tf.argmax(prob,axis=1)
            pred = tf.cast(pred,tf.int32)
            correct = tf.cast(tf.equal(pred,y),tf.int32)
            correct = tf.reduce_sum(correct)
            total_num += x.shape[0]
            total_correct += int(correct)
        acc = total_correct/total_num
        print('*'*10)
        print(epoch,'accuracy:',acc)
        print('*'*10)
if __name__ == '__main__':
    main()