from visdom import Visdom
import numpy as np
import time
# 新建名为'demo'的环境
viz = Visdom(env='demo')
x, y = 0, 0
for i in range(50):
    time.sleep(0.1)
    x = i
    y = i*i
    viz.line(
        X = np.array([x]),
        Y = np.array([y]),
        win = 'window',
        update = 'append')