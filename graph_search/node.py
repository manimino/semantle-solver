import dataclasses
from typing import *


@dataclasses.dataclass
class Edge:
    to_idx: int
    dist: float


@dataclasses.dataclass
class Node:
    idx: int
    word: str
    vec: List[float]
    edges: List[Edge]

    def __str__(self):
        s = [
            '{}: {} ({} edges)'.format(self.id, self.word, len(self.edges))
        ]
        return '\n'.join(s)
