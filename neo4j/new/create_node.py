import os

from_ele = "Carbonate_cement_texture"
relation = "Including"
on = False


with open('./static/content.txt','r') as file:
    node_list = []
    node_labels = []
    relations = []
    for line in file.readlines():
        line = line.replace('-','')
        line = line.strip()
        name = line
        line = line.replace(' ','_')
        ele_label = line
        node ='(%s:%s {name:"%s"}),\n' % (ele_label,from_ele,name)
        node_label = ele_label+'\n'
        ss = "(%s)-[:%s]->(%s),\n" % (from_ele,relation,ele_label)
        node_labels.append(node_label)
        node_list.append(node)
        relations.append(ss)

with open('./output/nodes.txt','w') as file:
    file.writelines(node_list)
    
with open('./output/node_label.txt','w') as file:
    file.writelines(node_labels)
    
with open('./output/relations.txt','w') as file:
    file.writelines(relations)

if on :
    with open('./output/list/new.txt','a') as file:
        file.writelines(node_list)
        file.writelines(relations)