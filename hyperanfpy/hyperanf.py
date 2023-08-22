#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016-2021
# Code is adapted from the PPANF framework by Álvaro García-Recuero, algarecu@gmail.com
# https://github.com/algarecu/ppanf/tree/main
# https://arxiv.org/abs/2102.12610
import networkx as nx

from collections import defaultdict
from copy import copy

from hyperanfpy.hyperloglog import HyperLogLog


class HyperANF(object):
	def __init__(self, g: nx.Graph, max_depth: float = None, precision: float = 4):
		"""
		Implements the HyperANF algorithm from [1]

		[1] https://arxiv.org/pdf/1011.5599

		Args:
				g (nx.Graph): Input graph.
				max_depth (float, optional): Maximum depth considered. If None (default) computes all the paths until the longest one.
				precision (float): Precision of the HyperLogLog algorithm. Defaults to 4.
		"""
		self.g = g
		self.precision = precision
		self.max_depth = max_depth

		self.balls = defaultdict(list) # hll counters, where index = t
		self.node_hll = dict() # node's hll array

		for v in g:
			self.node_hll[v] = HyperLogLog(self.precision)
			self.node_hll[v].add(v)
			self.balls[v].append(self.node_hll[v])

		# Run HyperANF until counters stabilize
		changed = True
		self.t = 0
		while not self.__has_converged(self.t, changed):
			changed = False
			updated_v_node_hll = dict()
			
			for v in g:
				v_hll = copy(self.node_hll[v])
				for w in g.neighbors(v):
					v_hll.union(self.node_hll[w])
				
				updated_v_node_hll[v] = v_hll
				
				# Store <v, a> pair
				self.balls[v].append(v_hll)
			
			# Check if counters are unchanged and update c
			for v in g:
				changed = changed or not updated_v_node_hll[v].equals(self.node_hll[v])
				self.node_hll[v] = updated_v_node_hll[v]
			
			self.t += 1

	def __has_converged(self, t: int, changed: bool) -> bool:
		"""
		Check for convergence of the algorithm, reached either by maximum
		depth or by graph stability.

		Args:
				t (int): Current depth.
				changed (bool): True if the graph has changed in the last iteration.

		Returns:
				bool: Convergence reached or not-
		"""
		cond = not changed
		if self.max_depth is not None:
			cond = cond and (t >= self.max_depth)
		return cond 
	
	def power(self, power: int, remove_previous: bool = False) -> nx.Graph:
		"""
		Computes the power graph by using the computed balls.

		Args:
				power (int): Power of the desired output.
				remove_previous (bool): If True outputs the nodes at exact distance K.
					If False outputs the nodes at distance <= K. Use False for same behaviour as NetworkX Graph.power.
		Returns:
				nx.Graph: Output power graph.
		"""
		out_g = nx.Graph()
		out_g.add_nodes_from(self.g.nodes)

		for node in self.g.nodes:
			ball = self.balls[node]
			
			# extract the nodes at `power` distance
			if len(ball) > power:
				nodes = ball[power].nodes

				# remove nodes from previous ball
				if remove_previous and power > 0:
					nodes = nodes.difference(ball[power - 1].nodes)

				for to in nodes:
					if to != node:
						out_g.add_edge(node, to, **self.g.get_edge_data(node, to, default={}))

		return out_g

