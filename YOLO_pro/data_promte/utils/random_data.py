import cv2
import numpy as np
from PIL import Image
import matplotlib.pylab as plt
from rich import print

def show(img):
    cv2.imshow("img",img)
    cv2.waitKey(0)

# def get_random_data_mixup(image, input_size, config, random=True):
#     # ===========================#
#     # 得到图像以及目标图像的wh
#     # ===========================#
#     iw, ih = image.shape[:2]
#     w, h = input_size
#     # ===========================#
#     # 获得预测框
#     # ===========================#
#     bboxes = config.get_xml()[1]
#     '''
#     bboxes:{
#         name:"xxx",
#         bndbox:[1,2,3,4]
#     }
#     '''
    
#     if not random:
#         # 转变因子
#         pass
        
def move_image(image, input_size, xml):
    # ===========================#
    # 得到图像以及目标图像的wh
    # ===========================#
    iw, ih = image.size
    w, h = input_size
    # ===========================#
    # 获得预测框
    # ===========================#
    box = xml
    '''
    bboxes:{
        name:"xxx",
        bndbox:[1,2,3,4]
    }
    '''
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)
    dx = (w-nw)//2
    dy = (h-nh)//2
    #---------------------------------#
    #   将图像多余的部分加上灰条
    #---------------------------------#
    # image       = image.resize((nw,nh), Image.BICUBIC)
    image       = image.resize((nw,nh))
    new_image   = Image.new('RGB', (w,h), (128,128,128))
    new_image.paste(image, (dx, dy))
    # new_image.show()
    

    #---------------------------------#
    #   对真实框进行调整
    #---------------------------------#
    print(box)
    if len(box)>0:
        np.random.shuffle(box)
        box = box[0]["bndbox"]
        box = np.array(box)
        box[[0,2]] = box[[0,2]]*nw/iw + dx
        box[[1,3]] = box[[1,3]]*nh/ih + dy
        box[0:2][box[0:2]<0] = 0
        if box[2]>w:
            box[2]=w
        if box[3]>h:
            box[3]=h
        box_w = box[2] - box[0]
        box_h = box[3] - box[1]
        box = box[np.logical_and(box_w>1, box_h>1)] # discard invalid box
    return new_image, box
    
def  base_img(image, input_size, xml):
    # ===========================#
    # 得到图像以及目标图像的wh
    # ===========================#
    ih, iw = image.shape[:2]
    w, h = input_size
    '''
    bboxes:{
        name:"xxx",
        bndbox:[1,2,3,4]
    }
    '''
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)   
    dx = (w-nw)//2
    dy = (h-nh)//2
    
    # ===========================#
    # 加入灰度条
    # ===========================#
    new_img = np.zeros((w,h,3),dtype=np.uint8)+128
    image = cv2.resize(image,(nw,nh),interpolation=cv2.INTER_LINEAR)
    new_img[dy:dy+nh,dx:dx+nw] = image
    
    # ===========================#
    # 修改预测框
    # ===========================#
    print(xml)
    for bbox_dic in xml:
        bbox=bbox_dic['bndbox']
        bbox = np.array(bbox)
        bbox[[0,2]] = bbox[[0,2]]*nw/iw+dx
        bbox[[1,3]] = bbox[[1,3]]*nh/ih + dy
    return new_img,bbox
    