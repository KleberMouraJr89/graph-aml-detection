"""Tests for the Digraph API."""

import random
from collections import Counter

import pytest

from Digraph import Digraph

# Accounts: A=0, B=1, C=2, D=3, E=4
EDGES = [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 4)]


def build(V, edges):
    g = Digraph(V)
    for v, w in edges:
        g.add_edge(v, w)
    return g


def edge_multiset(g):
    """All edges as a multiset {(v, w): count}. Order-independent."""
    return Counter((v, w) for v in range(g.vertices) for w in g.adj(v))


@pytest.fixture
def g():
    return build(5, EDGES)


# --- size ---------------------------------------------------------------

def test_vertices_and_edges_count(g):
    assert g.vertices == 5
    assert g.e() == 6


def test_new_graph_has_no_edges():
    g = Digraph(3)
    assert g.e() == 0
    assert all(list(g.adj(v)) == [] for v in range(3))


# --- adjacency and degrees ----------------------------------------------

@pytest.mark.parametrize("v, expected", [
    (0, {1, 2}), (1, {2}), (2, {0, 3}), (3, {4}), (4, set()),
])
def test_adjacency(g, v, expected):
    assert set(g.adj(v)) == expected


@pytest.mark.parametrize("v, expected", [(0, 2), (1, 1), (2, 2), (3, 1), (4, 0)])
def test_outdegree(g, v, expected):
    assert g.outdegree(v) == expected


@pytest.mark.parametrize("v, expected", [(0, 1), (1, 1), (2, 2), (3, 1), (4, 1)])
def test_indegree(g, v, expected):
    assert g.indegree(v) == expected


def test_indegree_is_a_pure_query(g):
    assert g.indegree(2) == g.indegree(2) == 2


def test_degree_sums_equal_edge_count(g):
    V = g.vertices
    assert sum(g.outdegree(v) for v in range(V)) == g.e()
    assert sum(g.indegree(v) for v in range(V)) == g.e()


# --- reverse ------------------------------------------------------------

def test_reverse_returns_new_digraph(g):
    r = g.reverse()
    assert isinstance(r, Digraph)
    assert r is not g


def test_reverse_flips_every_edge(g):
    r = g.reverse()
    assert r.vertices == g.vertices
    assert r.e() == g.e()
    assert edge_multiset(r) == Counter((w, v) for v, w in EDGES)


def test_reverse_swaps_degrees(g):
    r = g.reverse()
    for v in range(g.vertices):
        assert r.outdegree(v) == g.indegree(v)
        assert r.indegree(v) == g.outdegree(v)


def test_double_reverse_is_identity(g):
    assert edge_multiset(g.reverse().reverse()) == edge_multiset(g)


def test_reverse_does_not_mutate_original(g):
    before = edge_multiset(g)
    g.reverse()
    assert edge_multiset(g) == before


# --- multigraph semantics -----------------------------------------------

def test_parallel_edges_and_self_loops_are_allowed():
    m = build(2, [(0, 1), (0, 1), (1, 1)])
    assert m.e() == 3
    assert edge_multiset(m) == Counter({(0, 1): 2, (1, 1): 1})
    assert m.outdegree(1) == 1
    assert m.indegree(1) == 3   # two parallel edges + self-loop


# --- validation ---------------------------------------------------------

@pytest.mark.parametrize("bad", [-1, 5])
def test_add_edge_rejects_invalid_vertices(g, bad):
    with pytest.raises(ValueError):
        g.add_edge(0, bad)
    with pytest.raises(ValueError):
        g.add_edge(bad, 0)


@pytest.mark.parametrize("method", ["adj", "outdegree", "indegree"])
@pytest.mark.parametrize("bad", [-1, 5])
def test_queries_reject_invalid_vertices(g, method, bad):
    with pytest.raises(ValueError):
        getattr(g, method)(bad)


def test_negative_vertex_count_raises():
    with pytest.raises(ValueError):
        Digraph(-1)


@pytest.mark.parametrize("V", [0, 1])
def test_empty_and_single_vertex_graphs_are_valid(V):
    g = Digraph(V)
    assert g.vertices == V
    assert g.e() == 0


# --- string representation ----------------------------------------------

def test_tostring(g):
    lines = g.tostring().splitlines()
    assert lines[0] == "5 vertices"
    assert lines[3].split("->")[1].split() == ["0", "3"]   # vertex 2


# --- oracle: networkx ---------------------------------------------------

@pytest.mark.parametrize("seed", range(5))
def test_matches_networkx_on_random_multigraph(seed):
    nx = pytest.importorskip("networkx")
    rng = random.Random(seed)
    V = rng.randint(2, 30)
    edges = [(rng.randrange(V), rng.randrange(V)) for _ in range(rng.randint(0, 100))]

    g = build(V, edges)
    ref = nx.MultiDiGraph()
    ref.add_nodes_from(range(V))
    ref.add_edges_from(edges)

    assert g.e() == ref.number_of_edges()
    for v in range(V):
        assert g.outdegree(v) == ref.out_degree(v)
        assert g.indegree(v) == ref.in_degree(v)
    assert edge_multiset(g.reverse()) == Counter((u, v) for u, v, _ in ref.reverse().edges(keys=True))