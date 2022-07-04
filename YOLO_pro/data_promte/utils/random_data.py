from PIL import Image
import numpy as np

def get_random_data_mixup(image,input_size,config,random=True):
    # ===========================#
    # iw，ih为原图的宽和长，w，h为需要输出的宽和长
    # ===========================#
    
    iw,ih = image.size
    w,h = input_size
    # ===========================#
    # 得到所有预测框
    # ===========================#
    
    bndboxes = config.get_xml()[1]
    
    if not random:
        scale = min(w/iw, h/ih)
        nw = int(iw*scale)
        nh = int(ih*scale)
        dx = (w-nw)//2
        dy = (h-nh)//2
        
        # ===========================#
        # 加上灰条：先创建一个灰色的图像，然后把图片放上去
        # ===========================#
        image = image.resize((nw,nh),Image.BICUBIC)
        new_image = Image.new('RGB',(w,h),(128,128,128))
        new_image.paste(image,(dx,dy))
        image_data = np.array(new_image,np.float32)
        new_image.show()
        
        # ===========================#
        # 调整预测框
        # ===========================#
        
        if len(bndboxes)>0:
            for box in bndboxes:
                bbox = box["bndbox"]
                bbox = np.array(bbox)
                bbox[:,[0,2]] = box[:,[0,2]]*nw/iw+dx
                bbox[:,[1,3]] = box[:,[1,3]]*nh/ih+dy
                bbox[:,0:2][bbox[:.0:2]<0]=0
                bbox[:, 2][bbox[:, 2]>w] = w
                bbox[:, 3][bbox[:, 3]>h] = h
                box_w = bbox[:, 2] - bbox[:, 0]
                box_h = bbox[:, 3] - bbox[:, 1]
                bbox = bbox[np.logical_and(box_w>1, box_h>1)]
        return image_data, box