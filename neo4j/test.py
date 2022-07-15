
from py2neo import Graph,Node,Relationship

graph = Graph('http://localhost:7474',auth=('neo4j','3210'))

def create_node(label,name,describe=None):
    if describe is not None:
        node = Node(label,name=name,describe=describe)
    else:
        node = Node(label,name=name)
    graph.create(node)
    
# create_node('Carbonate_mudstone','Carbonate_mudstone','Carbonate mudstone is defined as a matrix-supported carbonate-dominated rock comprised of more than 90% carbonate mud (<63 μm) component. @Lokier S W, Al Junaibi M. The petrographic description of carbonate facies: are we all speaking the same language?. Sedimentology, 2016, 63(7): 1843-1885.')
