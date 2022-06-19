import cv2 
import numpy as np
import matplotlib.pyplot as plt
import os
from rich import print

def look_img(img):
    # opencv 输出BGR格式，转化为RGB格式
    img_RGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img_RGB)
    plt.show

home_dir = r'./datasets/YOLOV3/'
path_join = os.path.join


net = cv2.dnn.readNet(path_join(home_dir,'yolov3.weights'),
                    path_join(home_dir,'YOLOV3.cfg'))

# ===========================
# 获得类别名称
# ===========================

with open(path_join(home_dir,'coco.names'),'r') as f:
    classes = f.read().splitlines()

# ===========================
# 导入图像
# ===========================

img = cv2.imread(path_join(home_dir,'img/test.jpg'))
# print(img.shape)
height , width , _ = img.shape

# ===========================
# 处理图像
# ===========================

blob = cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB=True,crop = False)
print(blob.shape)#(1, 3, 416, 416)

net.setInput(blob)

# ===========================
# 网络探索
# ===========================
# print(net.getLayerNames())
# print(net.getParam('conv_14').shape) 查看权重

#获取三个尺度输出层的名称
layersNames = net.getLayerNames()
output_layers_names = [layersNames[i-1] for i in net.getUnconnectedOutLayers()]
print(output_layers_names)

# ===========================
# 向前传播
# ===========================

prediction = net.forward(output_layers_names)
print([i.shape for i in prediction])
# [(507, 85), (2028, 85), (8112, 85)]
'''
13*13*3 = 507
26*26*3 = 2028
52*52*3 = 8112
'''

# ===========================
# 捕捉预测框
# ===========================

#预测框坐标
boxes=[]
#置信度
objectness=[]
#类别概率
class_probs = []
#类别索引号
class_ids = []
# 存放预测框名称
class_names = []

'''
85 = 5+80
0-3 --- 位置
4 --- 执行度
5-79 --- 类别
'''

for scale in prediction:
    for bbox in scale:#预测框
        obj = bbox[4]#执行度
        class_scores = bbox[5:]#各个类别分数
        #获得类别得分最高的索引号
        class_id = np.argmax(class_scores)
        #得到名称和预测值
        class_name = classes[class_id]
        class_prob = class_scores[class_id]
        
        #获得预测框中心点坐标,和预测框宽高
        center_x ,center_y = int(bbox[0]*width),int(bbox[1]*height)
        w , h = int(bbox[2]*width),int(bbox[3]*height)
        
        #预测框左上点的坐标
        x = int(center_x - w/2)
        y = int(center_y - h/2)
        
        boxes.append([x,y,w,h])
        objectness.append(float(obj))
        class_ids.append(class_id)
        class_names.append(class_name)
        class_probs.append(class_prob)
        
# 将objectness和类别概率相乘得到实际执行度
confidences = np.array(class_probs)* np.array(objectness)
print(len(confidences))
        
        
# ===========================
# 执行度过滤和非极大值抑制NMS
# ===========================

CONF_THRES = 0.1 #置信度阈值
NMS_THRES = 0.4 #NMS阈值，阈值越小，NMS越强

indexes =  cv2.dnn.NMSBoxes(boxes,confidences,CONF_THRES,NMS_THRES)
print(indexes.flatten())
color = [0, 221, 0]

for index in indexes.flatten():
    x,y,w,h = boxes[index]
    confidence = str(round(confidences[index],2))#round 四舍五入
    cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
    
    string = f'{class_names[index]} {confidence}'
    cv2.putText(img,string,(x,y+20),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
    
cv2.imwrite('result.jpg',img)