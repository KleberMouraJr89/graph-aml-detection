"""
    Diagraph algorithm
"""
from DirectedDFS import DirectedDFS

class Digraph:
    """ 
        Directed graph with integer vertices, backed by adjacency lists.

        Vertices are integers in [0, V). Mapping external identifiers (e.g.
        account ids) to integers is the responsibility of a separate symbol
        table. Parallel edges and self-loops are allowed; deduplication, if
        needed, must be done by the caller before inserting edges.

        Memory: Theta(V + E).
    """

    def __init__(self, vertices:int):
        """
            Create an empty digraph with the given number of vertices and no edges.

            Args:
                vertices: Number of vertices. Must be non-negative.

            Raises:
                ValueError: If vertices is negative.

            Complexity:
                O(vertices) time and memory.
        """

        self.vertices = vertices

        # Validation
        self._validation = Validate()
        self._validation._illegal_input(vertices)

        self.digraph = self.empty_digraph(self.vertices)
        self._indegree = self.empty_indegree(self.vertices)
    
    def __str__(self):
        return f"Digraph algorithm's with {self.vertices} vertices"

    def __repr__(self):
        return f"Diagraph's algorithm - input: numbers of Vertices [int]"

    @staticmethod
    def empty_digraph(vert):
        return {i: [] for i in range(vert)}

    @staticmethod
    def empty_indegree(vert):
            return {i: 0 for i in range(vert)}

    def e(self):
        """ 
            Return the number of edges

            complexity: O(V + E) time O(E) memory
        """
        aux = [item for line in self.digraph.values() for item in line]
        return len(aux)

    def add_edge(self, v, e):
        """ Add the directed edge v -> e.

            Updates the adjacency list of v, the indegree of e and the edge count.

            Args:
                v: Tail (source) vertex, in [0, V).
                e: Head (destination) vertex, in [0, V).

            Raises:
                ValueError: If v or e is outside [0, V).

            Complexity:
                O(1) amortized time.
        """

        #validation function input
        self._validation._illegal_double_range_input(self.vertices, v, e)

        #append in digraph structure
        self.digraph[v].append(e)
        #increment +1 in the specific vertice
        self._indegree[e]+=1

    def adj(self, v):
        """ Return the vertices adjacent from v (heads of edges leaving v).

            Iteration order is an implementation detail and must not be relied on.
            The returned list is the internal structure: do not modify it.

            Args:
                v: Vertex index in [0, V).

            Raises:
                ValueError: If v is outside [0, V).

            Complexity:
                O(1) to return; O(outdegree(v)) to iterate.
        """

        #validation function input
        self._validation._illegal_range_input(self.vertices, v)

        return self.digraph[v]

    def outdegree(self, v):
        """ Return the number of edges leaving vertex v.

            Parallel edges are counted separately.

            Args:
                v: Vertex index in [0, V).

            Raises:
                ValueError: If v is outside [0, V).

            Complexity:
                O(1) time.
        """

        #validation function input
        self._validation._illegal_range_input(self.vertices, v)

        return len(self.digraph[v])

    def indegree(self, v):
        """ Return the number of edges entering vertex v.

            Parallel edges are counted separately.

            Args:
                v: Vertex index in [0, V).

            Raises:
                ValueError: If v is outside [0, V).

            Complexity:
                O(1) time (maintained incrementally by add_edge).
        """

        #validation function input
        self._validation._illegal_range_input(self.vertices, v)

        return self._indegree[v]

    def reverse(self):
        """ Return a new digraph with every edge reversed (v -> w becomes w -> v).

            The original digraph is not modified. Both graphs have the same vertices,
            the same number of edges and the same strongly connected components;
            outdegree and indegree are swapped.

            Complexity:
                O(V + E) time and O(V + E) additional memory.
        """
        reversed_graph = Digraph(self.vertices)
        for v in range(self.vertices):
            for w in self.digraph[v]:
                reversed_graph.add_edge(w, v)
        return reversed_graph 

    def tostring(self):
        lines = [f"{self.vertices} vertices"]
        for v in range(self.vertices):
            neighbors = " ".join(str(w) for w in self.digraph[v])
            lines.append(f"{v} -> {neighbors}")
        return "\n".join(lines)

    def V(self):
        """ Numbers of vertices"""
        return self.vertices


class Validate:
    """Input validation helpers for Digraph."""
    
    def __init__(self):
        pass

    def __str__(self):
        return f"Diagraph's algorithm Validation"

    def __repr__(self):
        return f"Validation Diagraph's algorithm - input: numbers of Vertices [int]"

    @staticmethod
    def _illegal_input(vertice):
        if vertice < 0:
            raise ValueError("The input must be more than 0")

    @staticmethod
    def _illegal_range_input(vertice, v):
        
        if not (0 <= v <= (vertice-1)):
            raise ValueError(f"The input must be between 0 and {vertice-1}")

    @staticmethod
    def _illegal_double_range_input(vertice , v, e):
            
            if not (0 <= v <= (vertice-1)) or not (0 <= e <= (vertice-1)):
                raise ValueError(f"The input must be between 0 and {vertice-1}")


if __name__ == "__main__":
    # A=0, B=1, C=2, D=3, E=4
    d = Digraph(5)
    for v, w in [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 4)]:
        d.add_edge(v, w)

    print(d.tostring())

    assert sorted(d.adj(2)) == [0, 3]
    assert d.outdegree(0) == 2
    assert d.indegree(2) == 2      # recebe de A e de B
    assert d.indegree(2) == 2      # chamar de novo não pode mudar o resultado

    r = d.reverse()
    assert sorted(r.adj(2)) == [0, 1]   # em Gᴿ: C "recebeu" de A e B
    assert r.outdegree(4) == 1               # E recebeu de D

    print(r.tostring())

    print("OK")
    