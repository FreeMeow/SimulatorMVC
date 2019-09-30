import model.utils.global_utils as global_utils
from model.entities.vertex import Vertex
import numpy as np
import random


class Td_aco:

    def __init__(self, world, distance_matrix, alg_args):
        self.world = world
        self.distance_matrix = distance_matrix
        self.limit = int(alg_args['t']['default'])

    def copy_vertex(self, vertex):
        new_vertex = Vertex(vertex.p, vertex.st, vertex.point)
        new_vertex.lv = vertex.lv
        new_vertex.ts = vertex.ts
        return new_vertex

    def initialize(self, tau):
        pass

    def start(self):
        pass
    LOCAL_RUNS = 1000
    GLOBAL_RUNS = 100
    Q0 = 0.8

    def next_step(self, current_vertex_ind, vertexes, current_time):
        # 1.initialize
        iteration = 0
        sim_vertexes = [self.copy_vertex(vertex) for vertex in vertexes]
        tau = [[[] for vertex in vertexes] for vertex in vertexes]
        # 2.for every global run, do:
        for _ in range(0, self.GLOBAL_RUNS):
            for _ in range(0, self.LOCAL_RUNS):
                # 2.1 for every local run, do:
                # 2.1.1 init vertexes
                for vertex in sim_vertexes:
                    vertex.lv = 0
                    vertex.ts = 0

                # 2.1.2 place ant at current index
                current_ind = current_vertex_ind
                current_time = 0
                path = []
                # 2.1.3 while rout time < limit, do:
                while(current_time < self.limit):
                    # 2.1.3.1 decide next step according to ACO
                    # start of ACO algorithm
                    neighbors = []
                    for vertex in sim_vertexes:
                        if
                    if random.random() < self.Q0:
                        # exploitation
                    else:
                        # exploration
                        pass
                # 2.1.4 keep min cost tour
                # 2.1.5 change global tau according to tour
                # 3. decide next step greedily according to max tau

        return None

    def output(self):
        return {}
