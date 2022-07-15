from rich import  print
def read_node(url):
    list = []
    with open(url,'r') as f:
        node  = []
        for line in f.readlines():
            line = line.strip()
            param = line.split('|')
            node.append(param)
    print(node[0])
            
read_node('node.csv')