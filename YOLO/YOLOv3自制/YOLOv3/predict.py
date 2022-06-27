import cv2
import numpy as np
from PIL import Image
from yolo3 import YOLOv3

config ={
    'anchor_masks':[
        [1,2,3],
        [2,3,4],
        [3,4,5],
    ],
    'class_num':80,
    'anchors':[[[116,90],[156,198],[373,326]],
                [[30,61],[62,45],[59,119]],
                [[10,13],[16,30],[33,23]]
               ],
    'input_size':416
}


if __name__ == '__main__':
    yolo = YOLOv3(config['anchor_masks'],config['class_num'])