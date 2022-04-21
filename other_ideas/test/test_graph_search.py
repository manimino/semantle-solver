from graph_search.structs import Node, Edge

from scipy.spatial.distance import euclidean


def test_node_edge():
    n0 = Node(idx=0, word='ok', vec=[1, 1], edges=[])
    n1 = Node(idx=1, word='no', vec=[2.5, 1], edges=[])
    dist = euclidean(n0.vec, n1.vec)
    n0.edges.append(Edge(to_idx=n1.idx, dist=dist))
    n1.edges.append(Edge(to_idx=n0.idx, dist=dist))
    assert n0.idx == n1.edges[0].to_idx
    assert n1.idx == n0.edges[0].to_idx


