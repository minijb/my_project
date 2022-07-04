import json
from rich import print
from PIL import Image
import os
from lxml import etree

class config:
    def __init__(self,url=None) -> None:
        if url!=None:
            path = url
        else :
            path = "config.json"  
        print(path)  
        with open(path,"r") as f:
            str_json = f.read()
        config = json.loads(str_json)
        base_config = config['base']
        self.mixup_config = config['mixup']
        base_url = base_config['base_url']
        img_dir = base_config['img_dir']
        xml_dir = base_config['xml_dir']
        img_name = base_config['img_name']+".jpg"
        xml_name = base_config['img_name']+".xml"
        self.img_path= os.path.join(base_url,img_dir,img_name)
        self.xml_path = os.path.join(base_url,xml_dir,xml_name)
        

    def get_img(self):
        img = Image.open(self.img_path)
        img = img.convert("RGB")
        return img
    def get_xml(self):
        with open(self.xml_path,'r') as f:
            xml_text = f.read()
        tree  = etree.XML(xml_text)
        img_ann = []
        obj_ann = []
        size_ele = tree.xpath("/annotation/size")[0]
        img_ann.append(size_ele.xpath("./width/text()")[0])
        img_ann.append(size_ele.xpath("./height/text()")[0])
        for obj in tree.xpath("/annotation/object"):
            object ={}
            object["name"] = obj.xpath("./name/text()")[0]
            bndbox = obj.xpath("./bndbox")[0]
            object["bndbox"] = [
                bndbox.xpath("./xmin/text()")[0],
                bndbox.xpath("./ymin/text()")[0],
                bndbox.xpath("./xmax/text()")[0],
                bndbox.xpath("./ymax/text()")[0]
            ]
            obj_ann.append(object)
        return img_ann,obj_ann
    
    def get_mixupConfig(self):
        return self.mixup_config
# config = config()
# print(config.get_xml())


        