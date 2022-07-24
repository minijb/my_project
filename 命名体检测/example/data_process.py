from glob import glob
import os
import random
import pandas as pd
from config import *
from rich import print

# 解析标签
def get_annotation(ann_path):
    with open(ann_path,encoding='utf-8') as file:
        anns = {}
        for line in file.readlines():
            arr = line.split("\t")[1].split()
            name = arr[0]
            start = int(arr[1])
            end = int(arr[-1])
            if end-start >50 :#标注过长可能出问题
                continue
            anns[start] = 'B-'+name
            for i in range(start+1,end):
                anns[i] = 'I-'+name
        return anns
    
def get_text(txt_path):
    with open(txt_path,encoding="utf-8") as file:
            return file.read()
        
def generate_annotation():
    for txt_path in glob(ORIGIN_DIR+'*.txt'):
        ann_path = txt_path[:-3]+'ann'
        # print(ann_path)
        anns = get_annotation(ann_path)
        text = get_text(txt_path)
        
            
            
if __name__ == "__main__":
    generate_annotation()
