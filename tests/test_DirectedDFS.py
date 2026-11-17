"""
Tests for DirectedDFS.

Run with:
    pytest -v test_directed_dfs.py
"""

import random

import pytest

from DirectedDFS import DirectedDFS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def digraph():
    #   4 -> 0 -> 1 -> 3
    #        |    ^    |
    #        v    +----+
    #        2
    return {0: [1, 2], 1: [3], 2: [], 3: [1], 4: [0]}


@pytest.fixture
def dfs_from_0(digraph):
    return DirectedDFS(digraph, 0)


# ---------------------------------------------------------------------------
# Reachability: marked / has_path_to
# ---------------------------------------------------------------------------

def test_reachable_set(digraph, dfs_from_0):
    reachable = {v for v in digraph if dfs_from_0.marked(v)}
    assert reachable == {0, 1, 2, 3}


def test_source_is_marked(dfs_from_0):
    assert dfs_from_0.marked(0) is True


def test_unreachable_vertex_not_marked(dfs_from_0):
    # 4 -> 0 exists, but 0 -> 4 does not
    assert dfs_from_0.marked(4) is False


@pytest.mark.parametrize("v", [0, 1, 2, 3, 4])
def test_has_path_to_equals_marked(dfs_from_0, v):
    assert dfs_from_0.has_path_to(v) == dfs_from_0.marked(v)


def test_source_reaching_everything(digraph):
    dfs = DirectedDFS(digraph, 4)
    assert all(dfs.marked(v) for v in digraph)


# ---------------------------------------------------------------------------
# Paths: path_to
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "v, expected",
    [
        (0, [0]),
        (1, [0, 1]),
        (2, [0, 2]),
        (3, [0, 1, 3]),
        (4, None),
    ],
)
def test_path_to_from_0(dfs_from_0, v, expected):
    assert dfs_from_0.path_to(v) == expected


def test_path_to_from_4(digraph):
    dfs = DirectedDFS(digraph, 4)
    assert dfs.path_to(3) == [4, 0, 1, 3]


def test_path_to_does_not_change_state(dfs_from_0):
    # Calling path_to twice must return the same result
    assert dfs_from_0.path_to(3) == dfs_from_0.path_to(3)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_single_vertex():
    dfs = DirectedDFS({0: []}, 0)
    assert dfs.marked(0) is True
    assert dfs.path_to(0) == [0]


def test_two_cycle_terminates():
    dfs = DirectedDFS({0: [1], 1: [0]}, 0)
    assert dfs.marked(0) and dfs.marked(1)
    assert dfs.path_to(1) == [0, 1]


def test_self_loop():
    dfs = DirectedDFS({0: [0]}, 0)
    assert dfs.path_to(0) == [0]


def test_parallel_edges():
    # Multigraph: same edge repeated (several transactions A -> B)
    dfs = DirectedDFS({0: [1, 1, 1], 1: []}, 0)
    assert dfs.path_to(1) == [0, 1]


def test_disconnected_component():
    g = {0: [1], 1: [], 2: [3], 3: []}
    dfs = DirectedDFS(g, 0)
    assert {v for v in g if dfs.marked(v)} == {0, 1}
    assert dfs.path_to(3) is None


def test_non_contiguous_keys():
    # Vertices do not need to be 0..V-1 when using a dict
    g = {10: [20], 20: [30], 30: [], 40: [10]}
    dfs = DirectedDFS(g, 10)
    assert dfs.path_to(30) == [10, 20, 30]
    assert dfs.marked(40) is False


def test_independent_instances(digraph):
    # A second search must not inherit state from the first one
    a = DirectedDFS(digraph, 2)
    b = DirectedDFS(digraph, 4)
    assert {v for v in digraph if a.marked(v)} == {2}
    assert all(b.marked(v) for v in digraph)


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def test_empty_digraph_raises():
    with pytest.raises(ValueError):
        DirectedDFS({}, 0)


def test_invalid_start_raises(digraph):
    with pytest.raises(ValueError):
        DirectedDFS(digraph, 99)


@pytest.mark.parametrize("method", ["marked", "has_path_to", "path_to"])
def test_query_invalid_vertex_raises(dfs_from_0, method):
    with pytest.raises(ValueError):
        getattr(dfs_from_0, method)(99)


def test_missing_sink_key_raises_value_error():
    # Vertex 1 appears only as a destination (an account that only receives).
    # Contract: a clear ValueError, never a raw KeyError.
    with pytest.raises(ValueError):
        DirectedDFS({0: [1]}, 0)


# ---------------------------------------------------------------------------
# Oracle: random graphs vs networkx
# ---------------------------------------------------------------------------

def _random_digraph(rng, n_vertices, p):
    return {
        v: [w for w in range(n_vertices) if rng.random() < p]
        for v in range(n_vertices)
    }


def _is_valid_path(g, path, source, target):
    if not path or path[0] != source or path[-1] != target:
        return False
    return all(b in g[a] for a, b in zip(path, path[1:]))


@pytest.mark.parametrize("seed", range(50))
def test_matches_networkx(seed):
    nx = pytest.importorskip("networkx")

    rng = random.Random(seed)
    n = rng.randint(1, 30)
    g = _random_digraph(rng, n, rng.uniform(0.02, 0.3))
    s = rng.randrange(n)

    G = nx.DiGraph()
    G.add_nodes_from(g)
    G.add_edges_from((v, w) for v, adj in g.items() for w in adj)
    expected = nx.descendants(G, s) | {s}

    dfs = DirectedDFS(g, s)

    assert {v for v in g if dfs.marked(v)} == expected
    for v in expected:
        assert _is_valid_path(g, dfs.path_to(v), s, v)
    for v in set(g) - expected:
        assert dfs.path_to(v) is None


# ---------------------------------------------------------------------------
# Known limitation of the recursive version
# ---------------------------------------------------------------------------

@pytest.mark.xfail(raises=RecursionError, reason="recursive DFS; iterative version must pass")
def test_long_chain():
    n = 5000
    chain = {v: [v + 1] for v in range(n - 1)}
    chain[n - 1] = []
    dfs = DirectedDFS(chain, 0)
    assert dfs.marked(n - 1)
    assert len(dfs.path_to(n - 1)) == n