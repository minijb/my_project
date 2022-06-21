import cv2
import os
from lxml import etree
from rich import print
# 文件目录
baseUrl = r'D:\datasets\VOCdevkit\VOC2007'
baseDirList = os.listdir(baseUrl)
# ===========================
# 得到标注框和名称
# ===========================

#使用yield节约内存 , 输出图片本体和所有标注框+名称
color = [0, 0, 221]

def get_element(url):
    annotations = os.listdir(url)
    for i, xml_path in enumerate(annotations):
        path = os.path.join(baseUrl, 'Annotations', xml_path)
        with open(path, 'r') as f:
            path_content = f.read()  # 得到内容
        # 进行解析
        xml_tree = etree.XML(path_content)
        img_name = xml_tree.xpath(
            "/annotation/filename/text()")[0]
        names = xml_tree.xpath(
            "//object/name/text()"
        )
        xmins = xml_tree.xpath(
            "//xmin/text()"
        )
        ymins = xml_tree.xpath(
            "//ymin/text()"
        )
        xmaxs = xml_tree.xpath(
            "//xmax/text()"
        )
        ymaxs = xml_tree.xpath(
            "//ymax/text()"
        )
        yield img_name, list(zip(names, xmins, ymins, xmaxs, ymaxs))

#画出box
def draw_boxes(img_name, bundbox_list):
    # cv2.namedWindow('img',cv2.WINDOW_KEEPRATIO)
    img = cv2.imread(
        os.path.join(baseUrl, 'HPEGImages', 
                    os.path.join(baseUrl,'JPEGImages',img_name)))
    for name, xmin, ymin, xmax, ymax in bundbox_list:
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax) 
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax),color,2)
        cv2.putText(img,name , (xmin,ymin-10),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),1,cv2.LINE_AA)
    cv2.imshow('img',img)
    cv2.waitKey(0)


img_name, bundbox_list = next(
    iter(get_element(os.path.join(baseUrl, 'Annotations'))))

draw_boxes(img_name,bundbox_list)
# print(img_name.bundbox_list)



    
