import tensorflow as tf

w = tf.Variable(1.0)
b = tf.Variable(2.0)
x = tf.Variable(3.0)

with tf.GradientTape() as t1:
    with tf.GradientTape() as t2:
        y = x*w+b
    dy_dw,dy_db = t2.gradient(y,[w,b])
d2y_fw2 = t1.gradient(dy_dw,w)

print(dy_dw,dy_db,d2y_fw2)
#tf.Tensor(3.0, shape=(), dtype=float32) tf.Tensor(1.0, shape=(), dtype=float32) None
