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
    text = ""
    with open(txt_path,encoding="utf-8") as file:
        for line in file.readlines():
            line.strip()
            text += line
    return text
        
def generate_annotation():
    for txt_path in glob(ORIGIN_DIR+'*.txt'):
        ann_path = txt_path[:-3]+'ann'
        # print(ann_path)
        anns = get_annotation(ann_path)
        text = get_text(txt_path)
        # print(text)
        # exit()
        # 建立文本和标签的对应关系
        df = pd.DataFrame({'word':list(text),'label':['0']*len(text)})
        df.loc[anns.keys(),'label']=list(anns.values())
        # 导出到文件
        file_name = os.path.split(txt_path)[1]
        df.to_csv(ANNOTATION_DIR+file_name,header=None,index=None)

def split_sample(test_size = 0.3):
    files = glob(ANNOTATION_DIR+'*.txt')
    random.seed(0)
    random.shuffle(files)
    n = int(len(files)*test_size)
    test_files = files[:n]
    train_files = files[n:]
    # 合并文件
    merge_file(train_files,TRAIN_SAMPLE_PATH)
    merge_file(test_files,TEST_SAMPLE_PATH)
    
def merge_file(files,target_path):
    with open(target_path,'a',encoding='utf-8') as file:
        for f in files:
            with open(f,encoding='utf-8') as ff:
                text = ff.read()
            file.write(text)    
            
     
if __name__ == "__main__":
    split_sample()
