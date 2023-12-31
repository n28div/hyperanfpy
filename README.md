# HyperANF Python Implementation

This repository contains a Python implementation of [Paolo Boldi, Marco Rosa, Sebastiano Vigna - "HyperANF: Approximating the Neighbourhood Function of Very Large Graphs on a Budget"](https://arxiv.org/pdf/1011.5599). 

The library computes the power of a graph's adjacency matrix. Differently than [NetworkX implementation](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.operators.product.power.html), it computes the power graph for directed graph as well much more efficiently.

![Performance graph](assets/performance.png "Performance graph")

## Installation

```
pip install git+https://github.com/n28div/hyperhanfpy
```

## Example

```python
import networkx
g = networkx.gnp_random_graph(10, 0.5, seed=42)
from hyperanfpy import HyperANF
hanf = HyperANF(g)
hanf.power(1).edges
EdgeView([(0, 2), (0, 3), (0, 4), (0, 8), (0, 9), (1, 2), (1, 3), (1, 5), (1, 6), (1, 9), (2, 5), (2, 8), (2, 9), (3, 5), (3, 6), (3, 7), (4, 9), (6, 9), (7, 8), (7, 9), (8, 9)])
hanf.power(2).edges
EdgeView([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 6), (4, 7), (4, 8), (4, 9), (5, 6), (5, 7), (5, 8), (5, 9), (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9)])
hanf.power(3).edges
EdgeView([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (5, 6), (5, 7), (5, 8), (5, 9), (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9)])
```

## Acknowledgments

The initial codebase of this implementation derives from [ppanf](https://github.com/algarecu/ppanf).