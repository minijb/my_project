from py2neo import Graph,Node,Relationship,NodeMatcher
from read_data import read_node,read_relationships
from rich import print
from create_ele import create_Node,create_relationship
graph = Graph('http://localhost:7474',auth=('neo4j','3210'))


# node_list = read_node("node1.csv")
# for i,node_con in enumerate(node_list):
#     node = create_Node(node_con[0],node_con[1],node_con[2])
#     graph.create(node)

realtion_txt = read_relationships("./relationship.csv")
for i,relation in enumerate(realtion_txt):
    try:
        relation = create_relationship(graph,relation[0],relation[1],relation[2])
    except Exception:
        print(relation)
        print(i,'is error')
    graph.create(relation)