from utils.config import config
from utils.random_data import base_img,move_image
import cv2
import numpy as np

con = config()
a,b=move_image(con.get_img_PIL(),(416,416),con.get_xml())
print(b)
# # cv2.rectangle(a,b[0:1])
# print(b[0][0:2])
# a=np.array(a,dtype=np.uint8)
# cv2.rectangle(a,b[0][0:2],b[0][2:4],(0,255,0),3)
# cv2.imshow("a",a)
# cv2.waitKey(0)
con = config()
a,b = base_img(con.get_img_CV(),(416,416),con.get_xml())
print(b)
cv2.rectangle(a,b[0:2],b[2:4],(0,255,0),3)
cv2.imshow("a",a)
cv2.waitKey(0)



# print(create_config())