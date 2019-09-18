import model.utils.global_utils as global_utils
from model.entities.vertex import Vertex
from model.utils.algo_utils import BaseConverter


class State:
    def __init__(self, time_stamp, state_vertex_ind, vertexes, distance_matrix, parent):
        self.vertexes = vertexes
        self.distance_matrix = distance_matrix
        self.time_stamp = time_stamp
        self.state_vertex_ind = state_vertex_ind
        self.children = []
        self.parent = parent

    def copy_vertex(self, vertex):
        new_vertex = Vertex(vertex.p, vertex.st, vertex.point)
        new_vertex.lv = vertex.lv
        new_vertex.ts = vertex.ts
        return new_vertex

    def branch(self):
        for i, v in enumerate(self.vertexes):
            if i == self.state_vertex_ind:
                continue
            self.price = 0
            c_time_stamp = self.time_stamp + \
                self.distance_matrix[self.state_vertex_ind][i]
            c_vertexes = []
            for _, w in enumerate(self.vertexes):
                c_vertexes.append(self.copy_vertex(w))

            c_state_vertex_ind = i
            c_vertexes[c_state_vertex_ind].visit(c_time_stamp)
            # calculate price of state by end result
            child = State(c_time_stamp, c_state_vertex_ind,
                          c_vertexes, self.distance_matrix, self)
            # total world price divided by time passed
            # child.price = sum([global_utils.price(c.cst(c_time_stamp), c.p) for c in child.vertexes])*(c_time_stamp-self.time_stamp) + self.price
            child.price = sum([global_utils.price(v.cst(c_time_stamp), v.p) for v in child.vertexes])

            # print('parent point: ',
            #   self.vertexes[self.state_vertex_ind].point, 'child point', self.vertexes[child.state_vertex_ind].point, ' price: ', child.price, ' time: ', self.time_stamp)
            self.children.append(child)
        return self.children


class K_step_v2:

    def __init__(self, world, distance_matrix, alg_args):
        self.world = world
        self.distance_matrix = distance_matrix
        self.k = int(alg_args['k'])

    def start(self):
        # debug
        self.steps_left = []
        # 1.generate first k-1 steps
        self.current_states = []

    def next_step(self, current_vertex_ind, vertexes, current_time):
        # 1. generate k layer of tree from k-1 layer
        if not self.steps_left:
            root = State(current_time, current_vertex_ind,
                         vertexes, self.distance_matrix, None)
            root.price = 0
            self.current_layer = []
            self.current_layer.append(root)
            for i in range(0, self.k):
                new_layer = []
                for c in self.current_layer:
                    new_layer += c.branch()
                self.current_layer = new_layer

            min_price = 10000000000000000000
            min_index = 0
            # TODO: check how dividing by length of path affects the algorithm
            # for i, state in enumerate(self.current_layer):
            #     price = state.price/(state.time_stamp - current_time)
            #     if price < min_price:
            #         min_price = price
            #         min_index = i
            for i, state in enumerate(self.current_layer):
                if state.price < min_price:
                    min_price = state.price
                    min_index = i
            state = self.current_layer[min_index]
            while state.parent:
                self.steps_left.insert(0, state.state_vertex_ind)
                state = state.parent

        return self.steps_left.pop(0)

    def output(self):
        return {}
