from numpy import dtype
import tensorflow as tf
from matplotlib import axis, pyplot as plt

def func(x):
    z = tf.math.sin(x[...,0])+tf.math.cos(x[...,1])
    return z

x = tf.linspace(0,2*4,500)
y = tf.linspace(0,2*4,500)

points_x,points_y = tf.meshgrid(x,y)
points = tf.stack([points_x,points_y],axis=2)

z = func(points)

plt.figure(figsize=(15,7))
plt.subplot(121)
plt.imshow(z,origin='lower',interpolation='none')
plt.colorbar()

plt.subplot(122)
plt.contour(points_x,points_y,z)
plt.colorbar()
plt.show()