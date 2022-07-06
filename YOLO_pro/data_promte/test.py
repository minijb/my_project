from utils.config import config
from utils.random_data import base_img,move_image,random_img
import cv2
import numpy as np

con = config()
# a,b=move_image(con.get_img_PIL(),(416,416),con.get_xml())

con = config()
# a,b = base_img(con.get_img_CV(),(416,416),con.get_xml())
# print(b)
# for obj in b:
#     cv2.rectangle(a,obj[0:2],obj[2:4],(0,255,0),1)
# a = cv2.cvtColor(a,cv2.COLOR_RGB2BGR)
# cv2.imshow("a",a)
# cv2.waitKey(0)
a,b = random_img(con.get_img_CV(),(416,416),con.get_xml(),con.get_mixupConfig())
for obj in b:
    cv2.rectangle(a,obj[0:2],obj[2:4],(0,255,0),1)
a = cv2.cvtColor(a,cv2.COLOR_RGB2BGR)
cv2.imshow("a",a)
cv2.waitKey(0)

# print(create_config())