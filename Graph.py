import string


class Graph:
    alphabet = list(string.ascii_lowercase)  # jeszcze nie wiem, co to jest, ale nie powinno tego być
    visited = list()    # podobnie

    def __init__(self, grp):
        self.grp = dict(grp)  # czmu grp?

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            try:
                x = next(self.visited)  # a kto inicjalizuje visited?
                print(x)
            except StopIteration:
                break
        # a gdzie jakiś return, jakieś StopIteration?

    def add_edge(self, node1, node2):
        edge = Graph.alphabet.pop(0)  # a jak się skończą literki?
        self.grp[node1][edge] = node2
        self.grp[node2].update({edge: node1})

    def add_node(self, parents, child):
        self.grp[child] = {}
        for parent in parents:
            self.add_edge(parent, child)

    def neighbours(self, node):
        return list(self.grp[node].values())

    def print_graph(self):
        print(self.grp)

    def delete_edge(self, edge):
        Graph.alphabet.insert(0, edge)
        nodes_edge = []
        for key in self.grp.keys():
            for value in self.grp[key].keys():
                if value == edge:
                    nodes_edge.append(key)

        for n in nodes_edge:
            del self.grp[n][edge]

    def delete_node(self, node):
        edges = list(self.grp[node].keys())

        for edge in edges:
            self.delete_edge(edge)

        del self.grp[node]

    def bfs(self, node):
        nodes = list()
        self.visited = list()
        self.visited.append(node)

        for v in self.neighbours(node):
            nodes.append(v)

        while len(nodes) > 0:
            u = nodes.pop(0)
            self.visited.append(u)
            for v in self.neighbours(u):
                if not v in self.visited and not v in nodes:
                    nodes.append(v)

        return self.visited  # Uwaga: metody nie mają zwracać listy ani krotki, tylko iterator (metody __iter__ i __next__).

    def dfs(self, node):
        nodes = list()
        self.visited = list()
        self.visited.append(node)

        for v in self.neighbours(node):
            nodes.insert(0, v)

        while len(nodes) > 0:
            u = nodes.pop(0)
            self.visited.append(u)
            for v in self.neighbours(u):
                if not v in self.visited and not v in nodes:
                    nodes.insert(0, v)

        return self.visited


# dict1 = {'0': {}, '1': {}}
# one = Graph(dict1)
# one.print_graph()
# one.add_edge('0', '1')
# one.print_graph()
# one.add_node(['0', '1'], '2')
# one.print_graph()
# one.add_node([], '3')
# one.print_graph()
# one.add_node(['2', '3'], '4')
# one.add_node('4', '5')
# one.print_graph()
#
# for i in one.dfs('5'):
#     print(i)

