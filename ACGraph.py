class ACGraph:

    ac = {0:  {}}

    def __init__(self, patterns):  # czy ten obiekt jest gotowy do użycia?
        self.patterns = tuple(set(patterns))

    def build(self):
        nodes = [item for item in range(1, 10000000)]  # po co nam prawie 10 mln liczb?

        for pattern in self.patterns:
            n = 0
            for letter in pattern:
                if letter in self.edges_from(n):
                    for node in self.neighbours(n):
                        if self.edge_between(n, node) == letter:
                            n = node
                else:
                    new_index = nodes.pop(0)
                    self.add_node(new_index)
                    self.add_edge(n, new_index, letter)
                    n = new_index

        return self.ac

    def add_edge(self, parent, child, edge):
        try:
            self.ac[parent].update({edge: child})
        except KeyError:
            print("Error. Node does not exist yet.")  # wymiana wyjątku na komunikat w konsoli jest bardzo nieopłacalna

    def add_node(self, child):
        self.ac[child] = {}

    def neighbours(self, node):
        return list(self.ac[node].values())

    def edges_from(self, node):
        if node in self.ac.keys():
            return tuple(self.ac[node].keys())
        return []

    def edge_between(self, node1, node2):
        if node1 not in self.ac.keys() and node2 not in self.ac.keys():
            print("Nodes do not exist or are not connected directly.")
        else:
            if node1 in self.neighbours(node2):
                for edge in self.edges_from(node2):
                    if self.ac[node2][edge] == node1:
                        return edge
            else:
                for edge in self.edges_from(node1):
                    if self.ac[node1][edge] == node2:
                        return edge

    def acceptance_nodes(self):
        acc = []
        for i in self.ac.keys():
            if self.ac[i] == {}:
                acc.append(i)
        return acc

    def parent(self, node):
        for i in self.ac.keys():
            if node in self.ac[i].values():
                return i

    def fail_link(self):
        fail_link_dict = {0: 0}
        nodes_to_fail_link = self.bfs(0)
        nodes_to_fail_link.remove(0)

        for node in nodes_to_fail_link:
            parent = self.parent(node)
            edge = self.edge_between(parent, node)
            parent_fail_link = fail_link_dict[parent]
            if edge in self.edges_from(parent_fail_link) and self.ac[parent_fail_link][edge] != node:
                fail_link_dict[node] = self.ac[parent_fail_link][edge]
            else:
                fail_link_dict[node] = parent_fail_link

        return fail_link_dict

    def text_until_node(self, node):
        text = ""
        i = node
        try:
            while i != 0:
                parent = self.parent(i)
                text += self.edge_between(parent, i)
                i = parent
            return text[::-1]
        except KeyError:
            print("Non existent or isolated node")

    def bfs(self, node):
        nodes = list()
        visited = list()
        visited.append(node)

        for v in self.neighbours(node):
            nodes.append(v)

        while len(nodes) > 0:
            u = nodes.pop(0)
            visited.append(u)
            for v in self.neighbours(u):
                if not v in visited and not v in nodes:
                    nodes.append(v)

        return visited

    def search(self, text):

        trie = self.build().copy()  # czy do każdego wyszukiwania trzeba na nowo budować automat?

        childless_nodes = []
        for key in self.ac.keys():
            if len(self.edges_from(key)) == 0:
                childless_nodes.append(key)

        for key in childless_nodes:
            del trie[key]

        fail_links = self.fail_link()
        acceptance_nodes = self.acceptance_nodes()

        i = 0
        n = 0
        sailed = []
        result = []

        while n < len(text):
            t = text[n]
            if i in acceptance_nodes:
                sailed.append(i)
                i = fail_links[i]
            elif t in trie[i].keys():
                i = trie[i][t]
                n += 1
            else:
                if i == 0:
                    n += 1
                else:
                    i = fail_links[i]
        if i in acceptance_nodes:
            sailed.append(i)

        for s in sailed:
            found_pattern = self.text_until_node(s)
            result.append(text.index(found_pattern))

        return result


one = ACGraph(("abc", "aac", "bca"))
print(one.build())
print(one.search("aaabc"))

