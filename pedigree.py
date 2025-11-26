import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from app01 import models

pedigrees = models.pedigree.object.all()
for pedigree in pedigrees:
    print(pedigree.pedigree_name,
          pedigree.parent_f,
          pedigree.parent_m)
family_matrix = [[pedigree['pedigree_name'],
                  pedigree['parent_f'],
                  pedigree['parent_m']] for pedigree in pedigrees]
family_members = {}
for row in family_matrix:
    child = row[0]
    parents = row[1:]
    family_members[child] = parents

G = nx.DiGraph()

# 添加顶点(家族成员)
for member in family_members.keys():
    G.add_node(member)

# 添加边(父母关系)
for child, parents in family_members.items():
    if parents:
        father, mother = parents
        G.add_edge(father, child)
        G.add_edge(mother, child)

pos = nx.planar_layout(G)

same_parents = []
baby = []

for row in family_matrix:
    if row[1] == row[2]:
        same_parents.append(row[1])
        baby.append(row[0])

big = same_parents + baby
bigg = np.array(big).reshape(2, len(baby))
node_colors = dict.fromkeys(same_parents, 'red');

# 计算每个节点的辈分
for node in G.nodes():
    ancestors = nx.ancestors(G, node)
    generation = len(list(ancestors)) + 1
    print(f"{node} : {generation} ")

# 绘制系谱图
fig = plt.figure(figsize=(10, 8))
nx.draw_networkx(G, pos, node_color=[node_colors.get(node, 'gray') for node in G.nodes()], alpha=0.5, node_size=500,
                 font_size=9, font_weight="bold", node_shape='h', with_labels=True)
blue_edges = list(zip(bigg[0], bigg[1]))
black_edges = [edge for edge in G.edges() if edge not in blue_edges]
nx.draw_networkx_edges(G, pos, edgelist=black_edges, edge_color='gray', alpha=0.5, width=2, arrowsize=10, arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=blue_edges, edge_color='red', alpha=1, width=2, arrowsize=10, arrows=True)
plt.axis('off')
plt.show()
