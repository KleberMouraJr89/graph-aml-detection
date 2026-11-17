
class DirectedDFS: #Depth-First Search
    """
        Single-source depth-first search on a directed graph.

        Computes every vertex reachable from a source vertex `start` and
        records the DFS tree (parent links), so that a path from `start`
        to any reachable vertex can be reconstructed. All the work is done
        in the constructor; queries are answered afterwards in constant time
        (or proportional to the path length, for `path_to`).

        Args:
            digraph: Adjacency lists as {vertex: [adjacent vertices]}.
                Every vertex, including those with no outgoing edges,
                must appear as a key.
            start: Source vertex. Must be a key of `digraph`.

        Raises:
            ValueError: If `digraph` is empty or `start` is not a vertex.

        Complexity:
            Construction: O(V + E) time; O(V) extra memory
            (visited and edge_to maps plus the recursion stack).
            marked / has_path_to: O(1).
            path_to: O(length of the path).

        Notes:
            Recursive implementation, bounded by Python's recursion limit
            (~1000 frames); long chains raise RecursionError. Use the
            iterative version for large graphs.
            The path returned is *a* path, not necessarily the shortest;
            use BFS for shortest paths.

        Example:
            >>> g = {0: [1, 2], 1: [3], 2: [], 3: [1], 4: [0]}
            >>> dfs = DirectedDFS(g, 0)
            >>> dfs.marked(3)
            True
            >>> dfs.marked(4)
            False
        """
    def __init__(self, digraph:dict, start:int, recursive:bool=False):

        self.digraph = digraph
        self.start = start

        #validation 
        self._validation = Validate()
        self._validation._illegal_input(digraph, start)
        self._validation._illegal_neighboors(digraph)

        self.dict_visited, self.dict_edgeto = self.empty_dfs(self.digraph)

        #run
        if recursive:
            self._dfs(None, self.start)
        else:
            self._dfs_nonrecursive(None, self.start)


    def __str__(self):
        return f"Directed Depth-First Search Algorithm's - Recursive Algorithm"

    def __repr__(self):
        return f"Directed Depth-First Search Algorithm's - input: diraph(dict); start vertice (int)"

    @staticmethod
    def empty_dfs(graph):
        """
            Build the initial search state for every vertex of the digraph.

            Args:
                digraph: Adjacency lists as {vertex: [adjacent vertices]}.

            Returns:
                A tuple (visited, edge_to):
                    visited: {vertex: False} for every vertex.
                    edge_to: {vertex: None} for every vertex.

            Complexity:
                O(V) time; O(V) memory. Only the keys are traversed,
                never the adjacency lists.
        """

        visit = {i: False for i in graph.keys()}
        edgeto = {i: None for i in graph.keys()}
        return visit, edgeto
    

    def _dfs(self, father, vertice:int):

        """
            Recursively visit every vertex reachable from `vertice`.

            Marks `vertice`, records `father` as its parent in the DFS tree,
            then recurses into each adjacent vertex not yet visited.

            Args:
                father: Vertex from which `vertice` was reached,
                    or None if `vertice` is the source.
                vertice: Vertex being visited.

            Complexity:
                Over the whole search: O(V + E) time, since each vertex is
                marked once and each edge is examined once. O(V) memory for
                the recursion stack in the worst case (a long chain).
        """

        self._validation._illegal_range_input(self.digraph, vertice)

        self._mark(father, vertice)

        for i in self.digraph[vertice]:
            if not self.dict_visited[i]:
                self._dfs(vertice, i)

    def _dfs_nonrecursive(self, father, vertice:int):


        self._validation._illegal_range_input(self.digraph, vertice)

        adj = {v: iter(self.digraph[v]) for v in self.digraph}
        stack = []

        self._mark(father, vertice)
        stack.append(vertice)

        while stack:

            v = stack[-1]

            try:
                w = next(adj[v])

                if not self.dict_visited[w]:

                    self._mark(v, w)

                    stack.append(w)

            except StopIteration:

                stack.pop()



    def _mark(self, father, index:int):
        """
            Mark `vertice` as visited and store its parent in the DFS tree.

            Args:
                father: Parent of `vertice`, or None for the source.
                vertice: Vertex being marked.

            Complexity:
                O(1) time and memory.
        """

        self.dict_visited[index] = True
        self.dict_edgeto[index] = father

    def marked(self, v:int):
        """
            Check whether `v` is reachable from the source.

            Args:
                v: Vertex to query.

            Returns:
                True if there is a directed path from the source to `v`,
                False otherwise.

            Raises:
                ValueError: If `v` is not a vertex of the digraph.

            Complexity:
                O(1) time and memory.
        """
        self._validation._illegal_range_input(self.digraph, v)

        return self.dict_visited[v]

    def path_to(self, v:int):
        """
            Return a directed path from the source to `v`.

            Args:
                v: Destination vertex.

            Returns:
                A list [source, ..., v], or None if `v` is not reachable.

            Complexity:
                O(L) time and memory, where L is the length of the path.
        """
        self._validation._illegal_range_input(self.digraph, v)

        if not self.has_path_to(v):
            return None

        path = []
        current = v
        while current is not None:
            path.append(current)
            current = self.dict_edgeto[current]

        path.reverse()
        return path

    def has_path_to(self, v:int):
        """
            Check whether there is a directed path from the source to `v`.

            Equivalent to `marked(v)`; kept for API compatibility with
            Princeton's DepthFirstDirectedPaths.

            Args:
                v: Vertex to query.

            Returns:
                True if `v` is reachable from the source, False otherwise.

            Raises:
                ValueError: If `v` is not a vertex of the digraph.

            Complexity:
                O(1) time and memory.
        """
        self._validation._illegal_range_input(self.digraph, v)

        return self.dict_visited[v]


class Validate:
    """Input validation helpers for Directed DFS"""
    
    def __init__(self):
        pass

    def __str__(self):
        return f"Depth-First Search algorithm Validation"

    def __repr__(self):
        return f"Validation DFS algorithm - input: digraph [dict], start vertice [int]"

    @staticmethod
    def _illegal_input(digraph, start):
        if (len(digraph.keys()) <= 0):
            raise ValueError("The digraph must have a keys at least")
        elif not (start in digraph.keys()):
            raise ValueError(f"The input must be between 0 and {len(digraph.keys())-1}")
            
    @staticmethod
    def _illegal_range_input(digraph, start):
        if not (start in digraph.keys()):
            raise ValueError(f"The input must be between 0 and {len(digraph.keys())-1}")

    @staticmethod
    def _illegal_neighboors(digraph):
        
        mainkeys = list(digraph.keys())

        for i in digraph.values():
            if not set(i).issubset(set(mainkeys)):
                raise ValueError(f"The values in the dictionary must be between 0 and {len(digraph.keys())-1}")



if __name__ == "__main__":

    digraph = {0: [1, 2], 1: [3], 2: [], 3: [1], 4: [0]}

    #test 1
    dfs = DirectedDFS(digraph, 0)
    print(dfs)

    for v in digraph.keys():
        print(v, dfs.marked(v), dfs.path_to(v))

    #test 2
    dfs = DirectedDFS(digraph, 4)
    print(dfs.path_to(3))

    #test 3 - cycle
    dfs = DirectedDFS({0: [1], 1: [0]}, 0)
    print(dfs.marked(0), dfs.marked(1))