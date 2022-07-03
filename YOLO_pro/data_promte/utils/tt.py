import json
from rich import print
from PIL import Image
import os

with open("config.json","r") as f:
    str_json = f.read()

config = json.loads(str_json)
print(config)
base = config["base"]
base_url = base["base_url"]
img_dir = base["img_dir"]
xml_dir = base["xml_dir"]
img_name = base["img_name"]
print(os.listdir(base_url))

img_path = os.path.join(base_url,img_dir,img_name)
img = Image.open(img_path)
img.convert("RGB")
img.show()
