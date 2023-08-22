from hyperhanfpy import HyperANF
import networkx

#g = networkx.gnp_random_graph(5, 0.5, seed=42)

g = networkx.Graph()
g.add_node(0)
g.add_node(1)
g.add_node(2)
g.add_node(3)

g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 3)

hanf = HyperANF(g)
print(hanf.power(4).edges)
