import model.utils.global_utils as global_utils
import numpy

WALL_FACTOR = 100


class Naive_potential_field:

    def __init__(self, world, distance_matrix, alg_args):
        self.world = world
        self.distance_matrix = distance_matrix

    def start(self):
        pass

    def next_step(self, current_vertex_ind, vertexes, current_time):
        # 1. calculate potential field force on robot
        current_point = vertexes[current_vertex_ind].point
        fv = (0, 0)
        for i, v in enumerate(vertexes):
            if i == current_vertex_ind:
                continue
            # 1.0 calc distance
            d = numpy.linalg.norm(current_point - v.point)
            # 1.1 calc length of vector
            length = global_utils.price(v.cst(current_time), v.p) / d**2
            # 1.2 calc direction vector
            fv += length * ((v.point-current_point)/d)
        # 1.3 obstacles
        fv += self.obstacle_forces(current_point)
        # 2. make sure that path is valid
        # 3. if vertex is in radius and screaming and not current vertex, return vertex index
        # 4. move virtual step toward force vector
        # 5. repeat until 3 is satisfied
        return None

    def obstacle_forces(self, current_point):
        fv = (0, 0)
        for i, o in enumerate(self.world["obstacles"]):
            wall_direction = o[0].point - o[1].point
            # if horizontal
            if wall_direction[0]:
                if o[0].point[0] < current_point[0] < o[1].point[0]:
                    # C
                    d = abs(o[0].point[1]-current_point[1])
                    length = (d/WALL_FACTOR)**-3
                    fv += length*(0, 1) if current_point[1] > o[0].point[1] else length*(0, -1)
                elif o[1].point[0] < current_point[0]:
                    if abs(o[1].point[0]-current_point[0]) < abs(o[1].point[1]-current_point[1]):
                        # B
                        d = abs(o[1].point[1]-current_point[1])
                        length = (d/WALL_FACTOR)**-3
                        fv += length*(0, 1) if current_point[1] > o[1].point[1] else length*(0, -1)
                    else:
                        # A
                        d = abs(o[1].point[0]-current_point[0])
                        length = (d/WALL_FACTOR)**-3
                        fv += length*(1, 0) if current_point[0] > o[1].point[0] else length*(-1, 0)
                else:
                    if o[0].point[0] < current_point[0]:
                        # D
                        d = abs(o[0].point[1]-current_point[1])
                        length = (d/WALL_FACTOR)**-3
                        fv += length*(0, 1) if current_point[1] > o[0].point[1] else length*(0, -1)
                    else:
                        # E
                        d = abs(o[0].point[0]-current_point[0])
                        length = (d/WALL_FACTOR)**-3
                        fv += length*(1, 0) if current_point[0] > o[1].point[0] else length*(-1, 0)
            # not horizonal
            else:
                if o[0].point[1] < current_point[1] < o[1].point[1]:
                    # C
                    d = abs(o[0].point[0]-current_point[0])
                    length = (d/WALL_FACTOR)**-3
                    fv += length*(1, 0) if current_point[0] > o[0].point[0] else length*(-1, 0)
                elif o[1].point[1] < current_point[1]:
                    if abs(o[1].point[1]-current_point[1]) < abs(o[1].point[0]-current_point[0]):
                        # B
                        d = abs(o[1].point[0]-current_point[0])
                        length = (d/WALL_FACTOR)**-3
                        fv += length*(1, 0) if current_point[0] > o[1].point[0] else length*(-1, 0)
                    else:
                        # A
                        d = abs(o[1].point[1]-current_point[1])
                        length = (d/WALL_FACTOR)**-3
                        fv += length*(0, 1) if current_point[1] > o[1].point[1] else length*(0, -1)
                else:
                    if o[0].point[1] < current_point[1]:
                        # D
                        d = abs(o[0].point[0]-current_point[0])
                        length = (d/WALL_FACTOR)**-3
                        fv += length*(1, 0) if current_point[0] > o[0].point[0] else length*(-1, 0)
                    else:
                        # E
                        d = abs(o[0].point[1]-current_point[1])
                        length = (d/WALL_FACTOR)**-3
                        fv += length*(0, 1) if current_point[1] > o[1].point[1] else length*(0, -1)
        return fv

    def output(self):
        return {}
