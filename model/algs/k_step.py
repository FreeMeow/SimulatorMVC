import model.utils.global_utils as global_utils
from model.entities.vertex import Vertex
from model.utils.algo_utils import BaseConverter


class State:
    def __init__(self, time_stamp, state_vertex_ind, vertexes, distance_matrix):
        self.vertexes = vertexes
        self.distance_matrix = distance_matrix
        self.time_stamp = time_stamp
        self.state_vertex_ind = state_vertex_ind
        self.children = []

    def copy_vertex(self, vertex):
        new_vertex = Vertex(vertex.p, vertex.st, vertex.point)
        new_vertex.lv = vertex.lv
        new_vertex.ts = vertex.ts
        return new_vertex

    def branch(self):
        for i, v in enumerate(self.vertexes):
            self.price = 0
            c_time_stamp = self.time_stamp + \
                self.distance_matrix[self.state_vertex_ind][i]
            c_vertexes = []
            for j, w in enumerate(self.vertexes):
                c_vertexes.append(self.copy_vertex(w))
            c_state_vertex_ind = i
            c_vertexes[c_state_vertex_ind].visit(c_time_stamp)
            # calculate price of state by end result
            child = State(c_time_stamp, c_state_vertex_ind,
                          c_vertexes, self.distance_matrix)
            # total world price divided by time passed
            # child.price = sum([global_utils.price(c.cst(c_time_stamp), c.p) for c in child.vertexes])*(c_time_stamp-self.time_stamp) + self.price
            child.price = (sum([global_utils.price(v.cst(c_time_stamp), v.p) for v in child.vertexes]) - sum(
                [global_utils.price(v.cst(self.time_stamp), v.p) for v in self.vertexes]))/(c_time_stamp-self.time_stamp) + self.price

            # print('parent point: ',
            #   self.vertexes[self.state_vertex_ind].point, 'child point', self.vertexes[child.state_vertex_ind].point, ' price: ', child.price, ' time: ', self.time_stamp)
            self.children.append(child)
        return self.children


class K_step:

    def __init__(self, world, distance_matrix, alg_args):
        self.world = world
        self.distance_matrix = distance_matrix
        self.k = int(alg_args['k'])

    def start(self):
        # debug
        self.is_first = True
        # 1.generate first k-1 steps
        self.current_states = []
        self.string_base = ""

    def next_step(self, current_vertex_ind, vertexes, current_time):
        # 1. generate k layer of tree from k-1 layer
        print("time: ", current_time)
        if self.is_first:
            self.is_first = False
            root = State(0, current_vertex_ind,
                         vertexes, self.distance_matrix)
            root.price = 0
            self.current_layer = []
            self.current_layer.append(root)
            for i in range(0, self.k-1):
                new_layer = []
                for c in self.current_layer:
                    new_layer += c.branch()
                self.current_layer = new_layer
            # make base converter
            for i in range(0, len(vertexes)):
                if i < 10:
                    self.string_base += str(i)
                else:
                    self.string_base += chr(ord('a')+i-10)
            self.base_n = BaseConverter(self.string_base)

        # 2. find state with minimum cost
        next_layer = []
        for i, x in enumerate(self.current_layer):
            next_layer += x.branch()
        # print('size of next layer:', len(next_layer))
        min_price = 1000000
        min_index = -1
        self.current_layer = next_layer
        group_size = len(vertexes)**(self.k-1)

        for i, state in enumerate(next_layer):
            if state.price < min_price and int(i/group_size) == current_vertex_ind:
                min_price = state.price
                min_index = i
        for i, state in enumerate(next_layer):
            if state.price < min_price and int(i/group_size) != current_vertex_ind:
                min_price = state.price
                min_index = i
        # print('index chosen: ', min_index, ' price: ', min_price)
        # 4. find and return first layer vertex

        if min_index == -1:
            selected = current_vertex_ind
            print("staying")
        # *(index of state indicates first child in route)
        else:
            selected = int(min_index/group_size)
            print(self.base_n.from_decimal(min_index))
        # reduce layer to paths with selected state as parent
        self.current_layer = self.current_layer[selected *
                                                group_size:(selected+1)*group_size]
        # print('sublist chosen:[', selected * group_size,
        #   ':', (selected+1)*group_size, ']')

        # print("going to selected ", selected)

        return selected

    def output(self):
        return {}
