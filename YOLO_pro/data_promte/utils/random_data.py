import cv2
import numpy as np
from PIL import Image
import matplotlib.pylab as plt
from rich import print


def rand(a=0, b=1):
    return np.random.rand()*(b-a) + a

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
    bbox_list = []
    for bbox_dic in xml:
        bbox=bbox_dic['bndbox']
        bbox = np.array(bbox)
        bbox[[0,2]] = bbox[[0,2]]*nw/iw+dx
        bbox[[1,3]] = bbox[[1,3]]*nh/ih + dy
        bbox_list.append(bbox)
    return new_img,bbox_list

def random_img(image, input_size, xml,nums_ch):
    # ===========================#
    # 得到图像以及目标图像的wh
    # ===========================#
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    ih, iw = image.shape[:2]
    w, h = input_size
    scale = min(w/iw, h/ih)  
    # ===========================#
    # 得到数值参数
    # ===========================#
    jitter = nums_ch[1]
    hue = nums_ch[2]
    sat = nums_ch[3]
    val = nums_ch[4]
    # ===========================#
    # 对长宽进行扭曲
    # ===========================#

    
    new_ar = iw/ih * rand(1-jitter,1+jitter) / rand(1-jitter,1+jitter)
    scale = rand(.25,2)
    
    if new_ar < 1:
        nh = int(scale*h)
        nw = int(nh*new_ar)
    else:
        nw = int(scale*w)
        nh = int(nw/new_ar)
    if nw>w: nw = int(rand(0,w))
    if nh>h: nh = int(rand(0,h))
    
    # ===========================#
    # 翻转
    # ===========================#
    flip = rand()<.5
    if flip:
        image = cv2.flip(image,1)
        for bbox_dic in xml:
            bbox=bbox_dic['bndbox']
            origin_xmin = bbox[0]
            origin_xmax = bbox[2]
            bbox[0]=image.shape[1]-origin_xmax
            bbox[2]=image.shape[1]-origin_xmin
    
    image = cv2.resize(image,(nw,nh),interpolation=cv2.INTER_LINEAR)
    dx = int(rand(0, (w-nw)//2))
    dy = int(rand(0, (h-nh)//2))
    # show(image)
    new_img = np.zeros((w,h,3),dtype=np.uint8)+128
    print(new_img[dy:dy+nh,dx:dx+nw].shape,image.shape)
    new_img[dy:dy+nh,dx:dx+nw] = image
    image = new_img
    # image = new_img

    #---------------------------------#
    #   对图像进行色域变换
    #   计算色域变换的参数
    #---------------------------------#
    r = np.random.uniform(-1,1,3)*[hue,sat,val]+1
    #---------------------------------#
    #   将图像转到HSV上
    #---------------------------------#
    hue, sat, val   = cv2.split(cv2.cvtColor(image, cv2.COLOR_RGB2HSV))
    dtype           = image.dtype
     #---------------------------------#
    #   应用变换
    #---------------------------------#
    x       = np.arange(0, 256, dtype=r.dtype)
    lut_hue = ((x * r[0]) % 180).astype(dtype)
    lut_sat = np.clip(x * r[1], 0, 255).astype(dtype)
    lut_val = np.clip(x * r[2], 0, 255).astype(dtype)
    image = cv2.merge((cv2.LUT(hue, lut_hue), cv2.LUT(sat, lut_sat), cv2.LUT(val, lut_val)))
    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    
    bbox_list = []
    for bbox_dic in xml:
        bbox=bbox_dic['bndbox']
        bbox = np.array(bbox)
        bbox[[0,2]] = bbox[[0,2]]*nw/iw+dx
        bbox[[1,3]] = bbox[[1,3]]*nh/ih+dy
        bbox_list.append(bbox)
    
    return image,bbox_list