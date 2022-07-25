import random

import pandas as pd
import csv
#
# filePath = r'D:\list\分类.xlsx'
# data_list = []
# df = pd.read_excel(filePath,sheet_name='Smear slide')
# index_num = df.index
# num_class = -1
#
# for i in index_num:
#     row_data = list(df.values[i])  # type(df.iloc[i]) => series
#     data_list.append(row_data)
#
# datas = []
# train_data = []
#
# test_data = []
# with open('f2.txt','a',encoding='utf-8') as f:
#     for data in data_list:
#         f.write(str(data[3])+" __!__ "+str(data[3])+'\n')
#     f.close()
#


# with open('f.txt','a') as f:
#     a = ''
#     b = ''
#     c =''
#     a_= ''
#     b_=''
#     c_=''
#     for data in data_list:
#         a_ = str(data[0]).strip()
#         b_ = str(data[1]).strip()
#         # c_ =data[2]
#         if str(data[0]).strip() =='nan':
#             a_ =a
#         else:
#             a = str(data[0]).strip()
#
#         if str(data[1]).strip() =='nan':
#             b_ =b
#         else:
#             b = str(data[1]).strip()
#         if str(data[2]).strip() == 'nan':
#             c_ = c
#         else:
#             c = str(data[2]).strip()
#
#
#         print(str(a_)+" "+str(b_)+'||'+str(a)+" "+str(b))
#
#         f.write(str(a_) + ' __!__ ' + str(b_) + ' __!__ ' + str(c_) + ' __!__ ' +str(data[3]) + '\n')
#
#
# f.close()
# with open('f.txt','a') as f:
#     for data in data_list:
#         f.write(str('Reflectance Spectroscopy and Colorimetry') + ' __!__ ' +str(data[1]) + '\n')
#     f.close()
from collections import defaultdict
print('Al2O3\xa0 percent')
print('Al2O3 percent')