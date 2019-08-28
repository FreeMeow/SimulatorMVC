import json
import model.utils.parser as parser
import model.utils.dispatcher as dispatcher
import pprint
from model.utils.constants import CONSTANTS
import random


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.current_world = None
        self.current_world_path = None
        self.current_scenerio = None

    def load_world_from_file(self, path):
        try:
            world_json = open(path).read()
            world_data = json.loads(world_json)
            self.current_world = parser.json_to_world(world_data)
            self.current_world_path = path
        except FileNotFoundError:
            return False, "File not found"
        except Exception as e:
            return False, e
        return True, ""

    def generate_world(self, args):
        try:
            world_file = open(args['path']['default'] +
                              '/'+args['name']['default'])
            # prepare world parameters
            name = args['name']['default']
            width = 600
            height = 600
            tile_width = 20
            vertex_count = args['vertex_count']['default']
            obstacle_count = args['obstacle_count']['default']
            clustering_factor = args['clustering_factor']['default']
            max_pg = args['max_pg']['default']
            min_st = args['min_st']['default']
            max_st = args['max_st']['default']

            row_length = int(width/tile_width)
            column_length = int(height/tile_width)
            world_matrix = {{0}*row_length}*column_length
            vertexes = []
            obstacles = []
            # calculate item placement
            # TODO: implement clustering factor, probabillity variance
            for i in range(0, vertex_count):
                while(True):
                    x = random.randrange(1, row_length)
                    y = random.randrange(1, column_length)
                    if world_matrix[y][x] == 0:
                        break
                world_matrix[y][x] = 1
                vertexes.append({
                    "position": [x*tile_width, y*tile_width],
                    "starvation": random.randrange(min_st, max_st, 10),
                    "probability": 0.2
                })

            for j in range(0, obstacle_count):
                while(True):
                    connection_options = ['left', 'right', 'up', 'down']
                    vertical = random.randrange(0, 2)
                    wall = random.randrange(0, 2)
                    x = random.randrange(1, row_length)
                    y = random.randrange(1, column_length)
                    for vertex in vertexes:
                        if vertex["position"][0] == x:
                            if y > vertex["position"][1] and connection_options.__contains__('down'):
                                connection_options.remove('down')
                            elif connection_options.__contains__('up'):
                                connection_options.remove('up')
                        if vertex["position"][1] == y:
                            if x > vertex["position"][0] and connection_options.__contains__('left'):
                                connection_options.remove('left')
                            elif connection_options.__contains__('right'):
                                connection_options.remove('right')

        except FileNotFoundError:
            return False, "File not found"
        except Exception as e:
            return False, e
        return True, ""

    def run_algorithm_on_world(self, algo, algo_args, tpd):
        try:
            if self.current_world is None:
                return False, "No world loaded"
            self.current_scenerio = dispatcher.run_algorithm_on_world(
                self.current_world, algo, algo_args, tpd)
        except FileNotFoundError as e:
            return False, e
        except NameError as e:
            return False, e
        return True, ""

    def get_scenerio_for_gui(self):
        if self.current_scenerio is None:
            return False, "No scenerio have been created"
        return True, self.current_scenerio

    def get_scenerio_info(self):
        return self.current_scenerio['statistic']

    def set_const(self, const_name, new_value):
        if const_name in CONSTANTS:
            try:
                converted_value = float(new_value)
            except ValueError:
                try:
                    converted_value = int(new_value)
                except ValueError:
                    converted_value = new_value

            CONSTANTS[const_name] = converted_value
            return True, ""
        else:
            return False, "Constant '{}' not found".format(const_name)
