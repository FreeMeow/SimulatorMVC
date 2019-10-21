import model.utils.global_utils as global_utils
from model.utils.algo_utils import AHC
from model.utils.algo_utils import clusterDistance
from model.utils.algo_utils import Graph
import itertools
from model.entities.vertex import Vertex


class Onion_search_heuristic:

    def __init__(self, world, distance_matrix, alg_args):
        self.world = world
        self.distance_matrix = distance_matrix
        self.cnum = int(alg_args["cnum"]) if "cnum" in alg_args else 4
        self.container = Onion_stack()

    def start(self):
        pass

    def next_step(self, current_vertex_ind, vertexes, current_time):
        while True:
            if not self.container.peek():
                next_cluster = [i for i, _ in enumerate(vertexes)]
            else:
                next_cluster = self.container.next()
            if len(next_cluster) < 2:
                return next_cluster[0]
            # divide to m clusteres
            clusters = AHC(self.distance_matrix, self.cnum, next_cluster)
            # pathfind using kstep
            permutations = itertools.permutations(clusters, len(clusters))
            min_price = float("inf")
            min_permutation = None
            for permutation in permutations:
                cost = self.calc_cost(permutation, current_time, vertexes)
                if cost < min_price:
                    min_price = cost
                    min_permutation = permutation
            # insert clusteres in order to container
            for item in reversed(min_permutation):
                self.container.insert(item)
            # get next cluster in container
            # if cluster is cluster, repeat else return vertex

        return None

    def output(self):
        return {}

    def calc_cost(self, permutation, current_time, vertexes):
        iteration_time = 0
        c_vertexes = [self.copy_vertex(vertex) for vertex in vertexes]
        for i, cluster in enumerate(permutation):
            for index in cluster:
                c_vertexes[index].visit(current_time+iteration_time)
            if i < len(permutation)-1:
                iteration_time += self.clusterDistance_heuristic(permutation[i], permutation[i+1])
        sum = 0
        for vertex in c_vertexes:
            vertex.visit(current_time+iteration_time)
            sum += vertex.ts
        return sum

    def copy_vertex(self, vertex):
        new_vertex = Vertex(vertex.p, vertex.st, vertex.point)
        new_vertex.lv = vertex.lv
        new_vertex.ts = vertex.ts
        return new_vertex

    def clusterDistance_heuristic(self, cluster1, cluster2):
        mst_time = self.mst_calc(cluster1)
        min = float("inf")
        for i in cluster1:
            for j in cluster2:
                if self.distance_matrix[i][j] < min:
                    min = self.distance_matrix[i][j]
        return min + mst_time

    def mst_calc(self, cluster1):

        graph = Graph(len(cluster1))
        index_dictionary = []
        for i, vertex1 in enumerate(cluster1):
            index_dictionary.append(vertex1)
            for j, vertex2 in enumerate(cluster1):
                if i <= j:
                    continue
                graph.addEdge(i, j, int(self.distance_matrix[vertex1][vertex2]))

        parent, n = graph.PrimMST()
        sum = 0
        for i in range(1, n):
            sum += self.distance_matrix[index_dictionary[parent[i]]][index_dictionary[i]]
        return sum


class Onion_stack:
    def __init__(self):
        self.stack = []

    def next(self):
        return self.stack.pop(0)

    def insert(self, cluster):
        self.stack.insert(0, cluster)

    def peek(self):
        if len(self.stack) == 0:
            return None
        return self.stack[0]


class Onion_queue:
    def __init__(self):
        self.queue = []

    def next(self):
        return self.queue.pop(-1)

    def insert(self, cluster):
        self.queue.insert(0, cluster)

    def peek(self):
        return self.queue[-1]
