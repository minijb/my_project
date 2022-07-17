from py2neo import Graph,Node,Relationship,NodeMatcher
from read_data import read_node
from rich import print
from create_ele import create_Node
graph = Graph('http://localhost:7474',auth=('neo4j','3210'))


node_list = read_node("node1.csv")
for i,node_con in enumerate(node_list):
    node = create_Node(node_con[0],node_con[1],node_con[2])
    graph.create(node)
