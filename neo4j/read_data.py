from rich import  print
def read_node(url):
    with open(url,'r',encoding="utf-8") as f:
        node  = []
        for line in f.readlines():
            line = line.strip()
            if line[0]=='#': continue
            param = line.split('|')
            if len(param) != 3:
                print("there is error in")
                break
            node.append(param)
    return node

def read_relationships(url):
    with open(url,'r',encoding="utf-8") as f:
        node = []
        for line in f.readlines():
            line = line.strip()
            if line[0]=="#": continue
            param = line.split('|')
            if(len(param)!=3):
                print('error')
                break
            node.append(param)
    return node

