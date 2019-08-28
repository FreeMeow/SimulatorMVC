import model.utils.global_utils as global_utils
import model.utils.dijakstra as dijakstra
import math
from model.utils.constants import CONSTANTS


class Node:

    def __init__(self, point, index=-1):
        self.children = []
        self.point = point
        self.index = index

    def addChild(self, child):
        self.children.append(child)

    def find_child(self, point):
        for child in self.children:
            if child.point == point:
                return child
        return None


class Gravitational_search:

    def __init__(self, world, distance_matrix, alg_args):
        self.world = world
        self.distance_matrix = distance_matrix

    def start(self):
        pass

    def next_step(self, current_vertex_ind, vertexes, current_time):
        self.current_vertex_ind = current_vertex_ind
        self.current_time = current_time
        self.vertexes = vertexes
        # 1.build the path tree
        # current point is current vertex
        root = Node(vertexes[current_vertex_ind].point, current_vertex_ind)
        for i, v in enumerate(self.vertexes):
            if i == current_vertex_ind:
                continue
            path = dijakstra.get_points_path_with_dijakstra(
                self.world, root.point, vertexes[i].point)
            current_node = root
            path.pop(0)
            for point in path:
                temp = current_node.find_child(point)
                if temp:
                    current_node = temp
                else:
                    temp = Node(point)
                    current_node.addChild(temp)
                    current_node = temp
            current_node.index = i
        return self.calc_cost(root)

        # list next step for every vertex
        # do for every vertex in list
        # calc cost
        # for every vertex in vertexes
        # add to cost according to angle
        # if greater than max, update
        # if point of maximum cost is vertex's point, return point
        # current point = calculated point and repeat

    def output(self):
        return {}

    def angle_factor(self, root, point1, point2):
        angle = math.atan2(point2.y-root.y, point2.x-root.x) - \
            math.atan2(point1.y-root.y, point1.x-root.x)
        factor = math.cos(angle)
        if(math.isclose(factor, 0, abs_tol=1e-07) or factor <= 0):
            return 0
        return factor

    def calc_cost(self, node):
        if not node.children:
            node.chosen = None
            node.distance = self.distance_matrix[self.current_vertex_ind][node.index]
            node.price = self.price_function(1, node, node.distance)
            return node.index
        for child in node.children:
            self.calc_cost(child)

        max_price = 0
        max_child = None
        for child1 in node.children:
            if child1.price == 0:
                continue
            current_price = 0
            for child2 in node.children:
                if child2.price == 0:
                    continue
                current_price += self.price_function(self.angle_factor(
                    node.point, child1.point, child2.point), child2, child2.distance)

            if current_price > max_price:
                max_price = current_price
                max_child = child1
        if max_price == 0:
            node.index = self.current_vertex_ind
            node.price = 0
            node.chosen = None
            node.distance = 0
            return node.index
        node.price = max_price
        node.chosen = max_child
        node.index = node.chosen.index
        node.distance = node.chosen.distance
        return node.index

    def price_function(self, factor, node, distance):
        if distance == 0:
            return 0
        vertex = self.vertexes[node.index]
        # cost = global_utils.price(vertex.cst(
        #     self.current_time+distance), vertex.p)
        cost = global_utils.price(vertex.cst(
            self.current_time), vertex.p)
        # TODO: replace with constant
        return factor*cost*((1/distance)**CONSTANTS['G'])
        # path_list = []
        # for i, v in enumerate(vertexes):
        #     tup = (v, dijakstra.get_points_path_with_dijakstra(
        #         self.world, vertexes[current_vertex_ind].point, v.point))
        #     path_list.append(tup)
        # current_point = vertexes[current_vertex_ind].point
        # for i in range(1,):
        #     max_ind = current_vertex_ind
        #     max_price = 0
        #     for j, v in enumerate(path_list):
        #         if current_vertex_ind == j:
        #             print("continue cur=j", j)
        #             continue
        #         current_price = global_utils.price(
        #             v[0].cst(current_time+self.distance_matrix[current_vertex_ind][j]), v[0].p)
        #         if len(v[1]) <= i:
        #             print("len<=i+1", len(v[1]), (i+1))
        #             continue
        #         for k, w in enumerate(path_list):
        #             print("inner starts with j,k ", j, k)
        #             if k == j or k == current_vertex_ind:
        #                 continue
        #             if len(w[1]) <= i:
        #                 continue
        #             point1 = current_point
        #             point2 = v[1][i]
        #             point3 = w[1][i]
        #             angle = math.atan2(point3.y-point1.y, point3.x-point1.x) - \
        #                 math.atan2(point2.y-point1.y, point2.x-point1.x)
        #             angle = abs(angle)
        #             if angle >= 180:
        #                 angle = 360-angle
        #             if(angle >= 90):
        #                 continue
        #             print("angle ", angle)
        #             current_price += global_utils.price(w[0].cst(
        #                 current_time+self.distance_matrix[current_vertex_ind][j]), w[0].p) * ((90-angle)/90)
        #             print("current price ", j, " updated to ",
        #                   current_price, " because of ", k)
        #         if current_price > max_price:
        #             max_price = current_price
        #             max_ind = j
        #     if len(path_list[max_ind][1]) <= i+1:
        #         print("exit with ", max_ind, " with price ",
        #               max_price, " because path ends")
        #         return max_ind
        #     current_point = path_list[max_ind][1][i+1]
        #     for p in path_list:
        #         if len(p[1]) <= i+1 or current_point != p[1][i+1]:
        #             path_list.remove(p)
        #             print("path removed")
        #     if len(path_list) <= 1:
        #         print("exit with ", max_ind, " with price ",
        #               max_price, " because no more paths")
        #         return max_ind
