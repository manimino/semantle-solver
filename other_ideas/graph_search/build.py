import dataclasses

from graph_search.structs import Node, Edge

from typing import *


class Graph:

    def __init__(self):
        self.nodes: List[Node] = []
        self.idx = 0

    def add_node(self, node: Node):
        self.nodes.append(node)
        self.idx += 1

    def add_edges(self, from_node_idx: int, edges: List[Edge]):
        node = self.nodes[from_node_idx]
        node.edges.extend(edges)


def read_glove_file():
    pass


def main():



main()