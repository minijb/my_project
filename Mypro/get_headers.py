

class_a={}
class_b={}
class_c={}## 网页对应去符号字段
class_c_1={}
filePath = r'D:\list\归类.xlsx'
data_list = []
public_headers=[]
with open('headers.txt','r',encoding='utf-8') as f:
    for line in f.readlines():
        data = line.split(' __!__ ')
        data = [i.strip() for i in data]
        class_a[data[0]]= data[1]
        class_b[data[1]] = data[0]
    f.close()
with open('f2.txt','r',encoding='utf-8') as f:
    for line in f.readlines():
        data = line.split(' __!__ ')
        data = [i.strip() for i in data]
        class_c[data[0]]= data[1]
        class_c_1[data[1]] =data[0]

    f.close()
with open('f.txt','r') as f:
    for line in f.readlines():
        data = line.split(' __!__ ')
        data = [i.strip() for i in data]
        data_list.append(data)
    f.close()
for data in data_list:
    if data[0]=='Public':
        public_headers+=[data[1]]

all_data={}
typeOptions = []
biaotou = []
for data in data_list:
    biaotou.append(data[-1])
# biaotou = list(set(biaotou))

headers = []
headers = biaotou
types =[]
for data in data_list:
    for i in range(0,len(data)):
        types.append(data[i].strip())
types =list(set(types))

for type in types:
    if type in headers:
        typeOptions.append({'id':type,'name':type})
    else:
        typeOptions.append({'id': -1, 'name': type})

from collections import defaultdict
trees= defaultdict(lambda :'no')
treeOptions=[]
new_datas =[]
tem =[]
for data in data_list:
    text =''
    for i in data[:-1]:
        text=text+'__!__'+i
    if trees[text] =='no':
        trees[text]=[data[-1]]
    else:
        trees[text].append(data[-1])
print(len(trees))

new1 =[]
ok =[]
for key,value in trees.items():
    hs = [ i for i in key.split('__!__') if i !='' ]

    length =len(hs)
    txt =''
    for i in hs[:-1]:
        txt=txt+"__!__"+i

    tem={}
    tem['id']=hs[-1]
    tem['name'] =hs[-1]
    tem['children']=[]
    for data in value:
        tem['children'].append({'id':data,'name':data})
    if length ==1:
        ok.append(tem)
    else:
        new1.append([txt,tem])
print('1====')

tem_k ={}
new2=[]
for key,value in new1:

    tem_k[key] =[]
for key,value in new1:
    tem_k[key].append(value)
for key,value in tem_k.items():

    hs = [i for i in key.split('__!__') if i != '']

    length = len(hs)
    txt = ''
    for i in hs[:-1]:
        txt = txt + "__!__" + i
    if length ==1:
        tem={}
        tem['id'] = hs[-1]
        tem['name'] = hs[-1]
        tem['children'] = value
        ok.append(tem)
    else:
        new2.append([txt,{'id':hs[-1],'name':hs[-1],'children':value}])
print('2=====')
print(len(ok))
print(new2)

new3 =[]
tem_k ={}
for key,value in new2:
    tem_k[key] =[]
for key,value in new2:
    tem_k[key].append(value)

for key,value in tem_k.items():

    hs = [i for i in key.split('__!__') if i != '']

    length = len(hs)
    txt = ''
    for i in hs[:-1]:
        txt = txt + "__!__" + i
    if length ==1:
        tem={}
        tem['id'] = hs[-1]
        tem['name'] = hs[-1]
        tem['children'] = value
        ok.append(tem)
    else:
        new3.append([txt,{'id':hs[-1],'name':hs[-1],'children':value}])
print('3===')
print(len(ok))
print(new3)
new4=[]
tem_k ={}
for key,value in new3:
    tem_k[key] =[]
for key,value in new3:
    tem_k[key].append(value)

for key,value in tem_k.items():
    print(key)
    hs = [i for i in key.split('__!__') if i != '']

    length = len(hs)
    txt = ''
    for i in hs[:-1]:
        txt = txt + "__!__" + i
    if length ==1:
        tem={}
        tem['id'] = hs[-1]
        tem['name'] = hs[-1]
        tem['children'] = key
        ok.append(tem)
    else:
        new4.append([txt,{'id':hs[-1],'name':hs[-1],'children':value}])
print('4======')
print(ok)
for i in range(0,len(ok)):

    for j in range(0,i):
        try:
            if ok[i]['id'] == ok[j]['id']:
                ok[j]['children'] +=ok[i]['children']
                ok.pop(i)
        except:
            continue
print(len(ok))

treeOptions =ok
# for key,value in new1:
#     hs =key.split('__!__')


# for data in data_list:
#     length = len(data)
#     if length ==2:
#         index =trees[data[0]]
#         if index =='no':
#             trees[data[0]] =[]
#             trees[data[0]].append(data[1])
#         else:
#             trees[data[0]].append(data[1])
#     if length == 3:
#         index1 = trees[data[0]]
#         if trees[data[0]] =='no':
#             trees[data[0]] = defaultdict(lambda :'no')
#             trees[data[0]][data[1]]=[data[2]]
#         else:
#             if trees[data[0]][data[1]] =='no':
#                 trees[data[0]][data[1]] =[data[2]]
#             else:
#                 trees[data[0]][data[1]].append(data[2])





# for key,value in all_data.items():
#     tem ={}
#     tem['id'] = str(key)
#     tem['name'] = str(key)
#     tem['children'] = []
#     for data in value:
#         tem['children'].append({'id':str(data),'name':str(data)})
#     treeOptions.append(tem)

def get_headers():
    return treeOptions,typeOptions,headers

def get_all_headers():

    return headers
#   去符号到数据库字段
def get_classfy(header):
    if class_a.get(header,'no') == 'no':
        print(header)
    return class_a.get(header,'no')
#   数据库到去符号
def get_classfy_1(header):
    return class_b.get(header,'no')
# 原始归一到去符号归一
def get_classfy_c(header):
    if class_c.get(header,'no')=='no':
        print(header)
    return class_c.get(header,'no')
# 去符号归一到原始归一
def get_classfy_c_1(header):
    return class_c_1.get(header,'no')


for data in data_list:
    if data[0] == 'Public':
        public_headers += [get_classfy(data[1])]
public_headers=['id']+public_headers
def get_public_headers():
    return public_headers
# 返回文件夹里字段
its_headers={}
with open('f.txt', 'r') as f:
    for line in f.readlines():
        data = line.split(' __!__ ')
        data = [i.strip() for i in data]

        if data[-2] in its_headers.keys():
            its_headers[data[-2]].append(data[-1])
        else:
            its_headers[data[-2]]=[]
            its_headers[data[-2]].append(data[-1])

    f.close()
def get_its_headers(file):
    return its_headers[file]


if __name__ == '__main__':
    # print('main')
    # h=['Exp/Leg', 'Site', 'Hole', 'Latitude', 'Longitude', 'Water depth (m)', 'Core', 'Type', 'Core-Sect', 'Section', 'A/W', 'Interval (cm)', 'Top Offset [cm]', 'Top Depth (m)', 'Top Depth (mcd)', 'Top depth CSF-A (m)', 'Top depth CSF-B (m)', 'Top Depth MSF (m)', 'Bottom offset [cm]', 'Bottom depth (m)', 'Bottom depth CSF-A (m)', 'Bottom Depth CSF-B (m)', 'Bottom Depth MSF (m)', 'Midpoint depth (mbsf)', 'Reference', 'DOI', 'Method', 'Cuttings sample', 'Instrument', 'Instrument group', 'COMMENTSCHNS', 'Nitrogen (wt%)', 'Sulfur (wt%)', 'Comment_CHNS', 'Method_CHNS', 'Carbon_CaCO3 (wt%)', 'Carbon_Carbonate (wt%)', 'Carbon_Inorganic (wt%)', 'Carbon_Organic (wt%)', 'Carbon_Total (wt%)', 'Hydrogen (mg HC/g)', 'Hydrogen (wt%)']
    # for i in h:
    #     a =get_classfy_c(i)
    #
    #     b= get_classfy(a)
    #
    # print('fs-----')
    # all=get_its_headers('Salinity')
    # print(all)
    treeOptions,typeOptions,headers=get_headers()
    print(treeOptions[0]['children'])
    # print(get_public_headers())


