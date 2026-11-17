"""
Interfaces (contracts) shared by the graph algorithms.

The algorithms (DFS, BFS, DepthFirstOrder, Kosaraju...) do not depend on
the Digraph class itself, only on the methods described here. Any object
that has these methods can be used by any algorithm.
"""

from typing import Iterable, Protocol


class DigraphLike(Protocol):
    """
    Contract for a directed graph with integer vertices in [0, V).

    A class satisfies this protocol just by having these methods with
    compatible signatures. It does NOT need to inherit from DigraphLike
    (structural typing, also called "duck typing").
    """

    def V(self) -> int:
        """Return the number of vertices."""
        ...

    def iterable(self, v: int) -> Iterable[int]:
        """Return the vertices adjacent from v (heads of edges leaving v)."""
        ...


if __name__ == "__main__":

    # A minimal class that satisfies the protocol.
    # Note: it does not inherit from DigraphLike.
    class TinyGraph:
        def __init__(self):
            self._adj = {0: [1, 2], 1: [2], 2: []}

        def V(self) -> int:
            return len(self._adj)

        def adj(self, v: int) -> Iterable[int]:
            return self._adj[v]

    # A class that does NOT satisfy it (wrong method name).
    class BrokenGraph:
        def V(self) -> int:
            return 3

        def iterable(self, v: int) -> Iterable[int]:
            return []

    # A function that accepts any DigraphLike.
    def count_edges(G: DigraphLike) -> int:
        return sum(len(list(G.adj(v))) for v in range(G.V()))

    print(count_edges(TinyGraph()))     # 3
