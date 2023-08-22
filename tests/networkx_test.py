import pytest
import networkx as nx
from hyperanfpy import HyperANF

@pytest.mark.parametrize("p", [1, 2, 3, 4])
def test_networkx_consistency(p):
  g = nx.gnp_random_graph(10, 0.5, seed=42)
  hanf = HyperANF(g)
  
  assert set(hanf.power(p).edges) == set(nx.power(g, p).edges)