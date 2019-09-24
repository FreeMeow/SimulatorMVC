import random
from os.path import exists
import numpy as np
import json

TRIES = 1000
CLUSTER_TRIES = 100


class World_generator():

    def generate_world(self, args):
        # prepare world parameters
        path = args['path']['default'] if 'path' in args else '.\_data\generated_worlds'
        if not 'name' in args:
            return [False, "world name required (add -name ______ to generateworld command"]
        name = args['name']['default']
        vertex_count = int(args['vn']['default']) if 'vn' in args else random.randint(5, 15)
        wall_num = int(args['wn']['default']) if 'wn' in args else random.randint(3, 10)
        cluster_count = int(args['cn']['default']) if 'cn' in args else random.randint(1, 5)
        clustering_factor = float(args['cf']['default']) if 'cf' in args else 0
        if not 0 <= clustering_factor <= 1:
            return [False, "clustering factor must be between 0 and 1"]
        min_st = int(args['st_min'][0]) if 'st_range' in args else 100
        max_st = int(args['st_max'][1]) if 'st_range' in args else 600
        if min_st > max_st:
            return [False, "minimum starvation cannot be higher than maximum"]
        width = 600
        height = 600
        self.tile_size = 10
        # TODO: implement random probability based on uniform distribution + probability factor
        # max_pg = float(args['max_pg']['default'])
        probability = 1/vertex_count
        row_length = int(width/self.tile_size)+1
        column_length = int(height/self.tile_size)+1
        self.visit_points = []
        self.walls = []
        world_matrix = [[0 for _ in range(row_length)] for _ in range(column_length)]

        # generate walls
        rooms = self.divide(world_matrix, 0, 0, row_length, column_length, self.choose_orientation(row_length-1, column_length-1), wall_num)
        # generate cluster positions
        if(cluster_count > vertex_count):
            return [False, "number of clusters cannot be higher than number of vertexes"]
        clusters = []
        if cluster_count < len(rooms):
            rooms_with_clusteres = random.sample(rooms, cluster_count)
        else:
            rooms_with_clusteres = rooms

        for i in range(0, cluster_count):
            # choose room for cluster
            room = rooms_with_clusteres.pop(0)
            rooms_with_clusteres.append(room)
            tries = 0
            while True:
                cx = random.randrange(room['x']+1, room['x']+room['width']-1)
                cy = random.randrange(room['y']+1, room['y']+room['height']-1)
                if self.check_area(world_matrix, cx, cy, 1):
                    clusters.append([cx, cy, room])
                    self.visit_points.append(self.create_visit_point(cx, cy, min_st, max_st, probability))
                    world_matrix[cy][cx] = 2
                    break
                tries += 1
                if tries > TRIES:
                    # try placing in different room
                    room = rooms_with_clusteres.pop(0)
                    rooms_with_clusteres.append(room)
                    tries = 0
        # generate vertexes
        for i in range(0, vertex_count - cluster_count):
            tries = 0
            placed = False
            # use clustering factor to determine if vertex will belong to a cluster
            if random.uniform(0, 1) <= clustering_factor:
                # position vertex in one of the clusteres randomly
                cluster_tries = 0
                chosen_cluster = random.choice(clusters)
                while True:
                    # using gaussian curve to determine position inside cluster
                    # clustering factor and number of failed placement attempts affects standard deviation of curve
                    vx = int(chosen_cluster[0] + np.random.normal(loc=0.0, scale=1 + 10*(1-clustering_factor) + 10*(tries/(TRIES))))
                    vy = int(chosen_cluster[1] + np.random.normal(loc=0.0, scale=1 + 10*(1-clustering_factor) + 10*(tries/(TRIES))))
                    if self.check_area(world_matrix, vx, vy, 1, chosen_cluster[2]):
                        placed = True
                        break
                    tries += 1
                    if tries > TRIES:
                        cluster_tries += 1
                        tries = 0
                        if cluster_tries > CLUSTER_TRIES:
                            break
                        chosen_cluster = random.choice(clusters)

            if not placed:
                 # position vertex randomly
                tries = 0
                room = random.choice(rooms)
                while True:
                    vx = random.randrange(room['x']+1, room['x']+room['width']-1)
                    vy = random.randrange(room['y']+1, room['y']+room['height']-1)
                    if self.check_area(world_matrix, vx, vy, 1):
                        break
                    tries += 1
                    if tries > TRIES:
                        tries = 0
                        room = random.choice(rooms)

            self.visit_points.append(self.create_visit_point(vx, vy, min_st, max_st, round(probability, 2)))
            world_matrix[vy][vx] = 2

        # check parameters at hte beginning
        if not exists(path):
            return [False, "path does not exist"]
        with open(path + '/' + name+'.world', "w+") as world_file:
            try:
                world_file.write(json.dumps({
                    "name": name,
                    "width": width,
                    "height": height,
                    "robot": {
                        "walk_speed": 10,
                        "start_point": 0
                    },
                    "obstacles": self.walls,
                    "visit_points": self.visit_points,
                }))
                return [True, ""]
            except:
                return [False, "there was a problem in creating ", name, '.py']

    # --------------------------------------------------------------------
    # 3. Helper routines
    # --------------------------------------------------------------------
    S, E = 1, 2
    HORIZONTAL, VERTICAL = 1, 2

    def choose_orientation(self, width, height):
        if width >= 7 and height < 7:
            return self.VERTICAL
        elif height >= 7 and width < 7:
            return self.HORIZONTAL
        elif width < height:
            return self.HORIZONTAL
        elif height < width:
            return self.VERTICAL
        else:
            return self.HORIZONTAL if random.randint(0, 1) == 0 else self.VERTICAL

    # --------------------------------------------------------------------
    # 4. The recursive-division algorithm itself
    # --------------------------------------------------------------------

    def divide(self, world_matrix, x, y, width, height, orientation, wall_num):
        if (width < 7 and height < 7) or wall_num == 0 or width < 4 or height < 4:
            return [{'x': x, 'y': y, 'width': width, 'height': height}]

        horizontal = orientation == self.HORIZONTAL

        # where will the wall be drawn from?
        wx = x + (0 if horizontal else random.randrange(3, width-3))
        wy = y + (random.randrange(3, height-3) if horizontal else 0)

        # opening = random.randint(2, int(width/2 + .5)) if horizontal else random.randint(2, int(height/2 + .5))
        opening = 2
        # where will the passage through the wall exist?
        start_of_wall = random.randint(0, 1)
        if horizontal:
            wx, wall_width = [wx + opening, width - opening] if start_of_wall else [wx, width - opening]
            if start_of_wall:
                if(wx+wall_width != len(world_matrix[0])):
                    wall_width += 1
            else:
                if wx != 0:
                    wx, wall_width = [wx-1, wall_width+1]
        else:
            wy, wall_height = [wy + opening, height - opening] if start_of_wall else [wy, height - opening]
            if start_of_wall:
                if(wy+wall_height != len(world_matrix)):
                    wall_height += 1
            else:
                if wy != 0:
                    wy, wall_height = [wy - 1, wall_height + 1]
        # what direction will the wall be drawn?
        dx = 1 if horizontal else 0
        dy = 0 if horizontal else 1

        # how long will the wall be?
        length = wall_width if horizontal else wall_height
        wall = [[wx*self.tile_size, wy*self.tile_size]]
        wall.append([(wx+wall_width-1)*self.tile_size, wy*self.tile_size] if horizontal else [wx*self.tile_size, (wy+wall_height-1)*self.tile_size])
        self.walls.append(wall)
        for _ in range(length):
            world_matrix[wy][wx] = 1
            wx += dx
            wy += dy

        nx, ny = x, y
        w, h = [width, wy-y] if horizontal else [wx-x, height]
        wall_num -= 1
        wall_distribution_factor = wy / (height-1) if horizontal else wx / (width-1)
        wall_count1 = int(wall_distribution_factor*wall_num)
        wall_count2 = wall_num - wall_count1
        rooms = []
        rooms += self.divide(world_matrix, nx, ny, w, h, self.choose_orientation(w, h), wall_count1)

        nx, ny = [x, wy+1] if horizontal else [wx+1, y]
        w, h = [width, y+height-wy-1] if horizontal else [x+width-wx-1, height]
        rooms += self.divide(world_matrix, nx, ny, w, h, self.choose_orientation(w, h), wall_count2)
        return rooms

    def check_area(self, world_matrix, x, y, distance, room=None):
        # check if within boundaries of the world
        if x - distance < 0 or x + distance > len(world_matrix[0])-1 or y - distance < 0 or y + distance > len(world_matrix)-1:
            return False
        # check if within boundaries of room, if room exists
        if room and (not room['x'] < x < room['x']+room['width'] or not room['y'] < y < room['y']+room['height']):
            return False
        empty = True
        for i in range(x-distance, x + distance+1):
            for j in range(y - distance, y + distance+1):
                empty = empty and world_matrix[j][i] == 0
        return empty

    def create_visit_point(self, x, y, min_st, max_st, probability):
        return {
            "position": [x*self.tile_size, y*self.tile_size],
            "starvation": random.randrange(min_st, max_st, 10),
            "probability": probability
        }
