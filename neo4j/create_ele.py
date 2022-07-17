from py2neo import Graph,Node,Relationship,NodeMatcher
from read_data import read_node
from rich import print

def create_Node(label,name,describe):
    if describe=="None" : describe = eval(describe)
    if describe is not None:
        node = Node(label,name=name,describe=describe)
    else:
        node = Node(label,name=name)
    return node

def create_relationship(graph,start_Node,relation,end_Node):
    nodematcher = NodeMatcher(graph)
    nodes = nodematcher.match(start_Node)
    start_node = list(nodes)[0]
    nodes = nodematcher.match(end_Node)
    end_node = list(nodes)[0]
    relation = Relationship(start_node,relation,end_node)
    return relation

    