class DiGraph(object):

    def __init__(self):
        self.graph = dict()
        self.__dist = dict()
        self.__pathToNode = dict()
        self.__infinity = 0
        self.__numEdges = 0
        self.__numEdgesBackup = 0 # Acrescentei esse atributo para restaurar o valor de numEdges quando removido pelo Dijkstra

    def addVertex(self, vertex):
        if (vertex is None) or (self.hasVertex(vertex)):
            return False

        else:
            self.graph[vertex] = set()
            return True

    def hasVertex(self, vertex):
        if vertex in self.graph:
            return True

        else:
            return False

    def vertices(self):
        if self.graph != dict():
            return set(self.graph)

        else:
            return set()

    def numVertices(self):
        return len(self.graph)

    def adjacentTo(self, vertex):
        if self.hasVertex(vertex):
            conj = set()
            for i in self.graph[vertex]:
                conj.add(i)
            return conj

        else:
            return set()

    def getEdge(self, src, dst):
        if self.hasEdge(src, dst):
            for edge in self.graph[src]:
                if edge.getVertex() == dst:
                    return edge

        else:
            return None

    def hasEdge(self, src, dst):
        if (self.hasVertex(src)) and (self.hasVertex(dst)) and (Edge(dst) in self.graph[src]):
            return True

        else:
            return False

    def addEdge(self, src, dst, c=1):
        if (src is None) or (dst is None) or (c <= 0) or (src == dst):
            return False

        else:
            if self.hasVertex(src):
                if self.hasVertex(dst):
                    a = Edge(dst)
                    if a in self.graph[src]:
                        self.graph[src].remove(a)
                        self.graph[src].add(Edge(dst, c))
                    else:
                        self.__numEdges = self.__numEdges + 1
                        self.graph[src].add(Edge(dst, c))
                else:
                    self.__numEdges = self.__numEdges + 1
                    self.addVertex(dst)
                    self.graph[src].add(Edge(dst, c))

            else:
                self.graph[src] = set()
                if self.hasVertex(dst):
                    self.__numEdges = self.__numEdges + 1
                    self.graph[src].add(Edge(dst, c))
                else:
                    self.__numEdges = self.__numEdges + 1
                    self.addVertex(dst)
                    self.graph[src].add(Edge(dst, c))

            return True

    def getInfinity(self):
        self.__infinity = 0
        for indice in self.graph:
            for item in self.graph[indice]:
                if self.__infinity <= item.getCost():
                    self.__infinity = item.getCost()
        return self.__infinity

    def numEdges(self):
        return self.__numEdges

    def removeVertex(self, vertex):
        if not self.hasVertex(vertex):
            return False
        else:
            conj = self.incomingEdges(vertex)
            self.__numEdgesBackup = int(self.__numEdges)
            self.__numEdges = self.__numEdges - len(self.graph[vertex])
            self.graph.pop(vertex)

            for i in conj: # mudei para conj
                if Edge(vertex) in self.graph[i]:
                    self.graph[i].discard(Edge(vertex))
                    self.__numEdges = self.__numEdges - 1

            return True

    def incomingEdges(self, vertex):
        conj = set()
        for i in self.graph:
            if i != vertex:
                for j in self.graph[i]:
                    if j.getVertex() == vertex:
                        conj.add(i)
        return conj

    def getDist(self, vertex):
        return self.__dist[vertex]

    def Dijkstra(self, source):
        if (source is None) or (not (self.hasVertex(source))) or (self.graph[source] == set()):
            return dict()

        else:
            backup = dict()
            for key in self.graph:  #tive de mudar a forma de backup devido ao set() que precisa ser copiado
                backup[key] = self.graph[key].copy()

            for v in self.graph:
                self.__dist[v] = float("inf")
                self.__pathToNode[v] = -1

            self.__dist[source] = 0
            d = dict(self.__dist)  # Cria-se uma cópia

            while self.graph != dict():
                u = 0
                menor = float("inf")

                for i in d:
                    if d[i] < menor:
                        menor = d[i]
                        u = i

                if u == 0:
                    break

                d.pop(u)
                adjacentToU = self.adjacentTo(u)

                for v in adjacentToU:  # v é um Edge então para pegar seu nome deve-se utilizar o getVertex()

                    if self.__dist[v.getVertex()] > self.__dist[u] + self.getEdge(u, v.getVertex()).getCost():
                        self.__dist[v.getVertex()] = self.__dist[u] + self.getEdge(u, v.getVertex()).getCost()
                        d[v.getVertex()] = self.__dist[v.getVertex()]
                        self.__pathToNode[v.getVertex()] = u

                self.removeVertex(u)  # Remove item do graph até chegar a zero
                self.__numEdges = int(self.__numEdgesBackup)

            self.graph = backup.copy()
            return self.__dist

    def Dijkstra2(self, source, dest):
        if (source is None) or (dest is None) or not (self.hasVertex(source)) or not (self.hasVertex(dest)) or (
                self.graph[source] == set()):
            return list()

        else:
            path = list()
            find = False
            self.Dijkstra(source)
            path = path + [dest]

            while not find:
                path = [self.__pathToNode[dest]]+path
                dest = self.__pathToNode[dest]
                if dest == source:
                    find = True

            return path


class Edge:

    def __init__(self, n, c=0):
        self.__node = n
        self.__cost = c

    def setCost(self, c):
        self.__cost = c

    def getVertex(self):
        return self.__node

    def getCost(self):
        return self.__cost

    def compCost(self, other):
        return cmp(self.getCost(), other.getCost())

    def __hash__(self):
        return hash((self.__node))

    def __contains__(self, obj):
        return (self.getVertex() == obj.getVertex())

    def __eq__(self, obj):
        return (self.getVertex() == obj.getVertex())

    def __repr__(self):
        return "(" + str(self.getVertex()) + ", " + str(self.getCost()) + ")"


def cmp(x, y):
    if x < y:
        return -1

    elif x == y:
        return 0

    else:
        return 1

def main(args = None):

    social = DiGraph()
    social.addEdge("James", "Larry", 1)
    social.addEdge("James", "Larry", 2)
    social.addEdge("James", "Jim", 2)
    social.addEdge("James", "Liam", 1)
    social.addEdge("Liam", "Kaith", 3)
    social.addEdge("Liam", "Keith", 1)
    social.addEdge("Liam", "Jim", 1)
    social.addEdge("Jim", "Keith", 1)
    social.addEdge("Keith", "Jim", 1)
    social.addEdge("Larry", "Kaith", 1)
    social.addEdge("Pie", "Kaith", 5)
    social.addEdge("Liam", "Paul", 2)
    social.addEdge("Paul", "Pie", 2)
    print(social.graph)
    social.removeVertex("Jim")
    print(social.graph)
    print(social.numVertices())
    print(social.numEdges())
    #print(social.Dijkstra("James"))


if __name__ == '__main__':
    main()
