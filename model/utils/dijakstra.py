import math
from pythonds.graphs import PriorityQueue



def dijkstra(a_graph, start):
  pq = PriorityQueue()
  start.distance = 0
  a_graph.append(start)
  pq.buildHeap([(v.distance, v) for v in a_graph])
  while not pq.isEmpty():
    current_vertex = pq.delMin()
    for next_vertex in current_vertex.connections:
      new_dist = current_vertex.distance \
      + current_vertex.distance_from(next_vertex)
      if new_dist < next_vertex.distance:
        next_vertex.distance = new_dist
        next_vertex.pred = current_vertex
        pq.decreaseKey(next_vertex, new_dist)


def get_dijkastra_vertex_by_point(dv_arr, p):
  for dv in dv_arr:
    if dv.point == p:
      return dv
  return None

def euclidean_distance(p1, p2):
  return math.sqrt(((p1.x - p2.x) ** 2) + ((p1.y - p2.y) ** 2))

def reverse_dijkstra_path_scan(d_src, d_dest):
  current_ver = d_dest
  path = [d_dest.point]
  while current_ver.point != d_src.point:
    current_ver = current_ver.pred
    path.append(current_ver.point)
  return path

def get_points_path_with_dijakstra(world,p_src, p_dest):
  d_src = DijkstraVertex(p_src)
  d_dest = DijkstraVertex(p_dest)
  dijkstra_vertexes = create_dijkstra_vertexes_base(world, d_src, d_dest)
  dijkstra(dijkstra_vertexes, d_src)
  dijkstra_vertexes.remove(d_src)
  d_dest = get_dijkastra_vertex_by_point(dijkstra_vertexes, p_dest)
  path = reverse_dijkstra_path_scan(d_src, d_dest)
  return path[::-1]


def create_dijkstra_vertexes_base(world, d_src, d_dest):
  dijkstra_vertexes = [d_dest]
  excluded_list = []
  for obstacle in world['obstacles']:
    for p in obstacle:
      fill_connections_and_add_to_base(world,p, dijkstra_vertexes, excluded_list, d_dest)
  if d_src not in dijkstra_vertexes:
    for d_v in dijkstra_vertexes:
      if is_valid_path(world, d_src.point, d_v.point):
        set_meutual_connection(d_v, d_src)
  return dijkstra_vertexes

def fill_connections_and_add_to_base(world,p, dijkstra_vertexes, excluded_list, d_dest):
  d_p = DijkstraVertex(p)
  for vertex in dijkstra_vertexes:
      if (d_p in dijkstra_vertexes) and (p != d_dest.point):
          excluded_list.append(p)
          excluded_list = list(set(excluded_list))
          dijkstra_vertexes.remove(d_p)
      if (p not in excluded_list) and (is_valid_path(world, p, vertex.point)):
          set_meutual_connection(vertex, d_p)
  if (d_p not in dijkstra_vertexes) and (p not in excluded_list):
      dijkstra_vertexes.append(d_p)


def is_valid_path(world,p_robot, p_dest):
  if is_on_border(world,[p_robot, p_dest]):
      return False
  for obstacle in world['obstacles']:
      if (p_dest not in obstacle) and (p_robot not in obstacle) and (is_lines_crossing(p_robot, p_dest, obstacle[0], obstacle[1])):
          return False
  return True

def is_lines_crossing(crossing_p1, crossing_p2, crossed_p1, crossed_p2):
  if (crossing_p1.x > crossed_p1.x) and (crossing_p1.x > crossed_p2.x) and (crossing_p2.x > crossed_p1.x) and (crossing_p2.x > crossed_p2.x):
    return False
  if (crossing_p1.x < crossed_p1.x) and (crossing_p1.x < crossed_p2.x) and (crossing_p2.x < crossed_p1.x) and (crossing_p2.x < crossed_p2.x):
    return False
  if (crossing_p1.y > crossed_p1.y) and (crossing_p1.y > crossed_p2.y) and (crossing_p2.y > crossed_p1.y) and (crossing_p2.y > crossed_p2.y):
    return False
  if (crossing_p1.y < crossed_p1.y) and (crossing_p1.y < crossed_p2.y) and (crossing_p2.y < crossed_p1.y) and (crossing_p2.y < crossed_p2.y):
    return False
  if (crossing_p1.x == crossing_p2.x) and (crossed_p1.y == crossed_p2.y):
    if (crossed_p1.y < max(crossing_p1.y, crossing_p2.y)) and (crossed_p1.y > min(crossing_p1.y, crossing_p2.y)):
      return True
    else:
      return False
  if crossing_p1.x == crossing_p2.x:
    return False
  if (crossing_p1.y == crossing_p2.y) and (crossed_p1.x == crossed_p2.x):
    if (crossed_p1.x < max(crossing_p1.x, crossing_p2.x)) and (crossed_p1.x > min(crossing_p1.x, crossing_p2.x)):
      return True
    else:
      return False
  if crossing_p1.y == crossing_p2.y:
    return False
  if crossed_p1.y == crossed_p2.y:
    x = Vectors.find_x_of_intersection(crossing_p1, crossing_p2, crossed_p1.y)
    if (x < max(crossed_p1.x, crossed_p2.x)) and (x > min(crossed_p1.x, crossed_p2.x)):
      return True
    return False
  else:
    y = Vectors.find_y_of_intersection(crossing_p1, crossing_p2, crossed_p1.x)
    if (y < max(crossed_p1.y, crossed_p2.y)) and (y > min(crossed_p1.y, crossed_p2.y)):
      return True
    return False

def set_meutual_connection(dv1, dv2):
  dv1.add_connection(dv2)
  dv2.add_connection(dv1)

def is_on_border(world, points):
  for p in points:
    if (p.x == 0) or (p.y == 0) or (p.x == world['width']) or (p.y == world['height']):
      return True
  return False

class DijkstraVertex:

  def __init__(self, point):
    self.point = point
    self.distance = 10000000
    self.connections = []
    self.pred = None

  def __eq__(self, other):
    return self.point == other.point

  def __str__(self):
    if self.pred is None:
      return "point: {}, distance: {}, Pred: None".format(self.point, self.distance)
    return "point: {}, distance: {}, Pred: {}".format(self.point, self.distance, self.pred.point)

  def distance_from(self, other):
    return euclidean_distance(self.point, other.point)

  def add_connection(self, other):
    self.connections.append(other)

class Vectors:

  @staticmethod
  def normalize(point):
      return point/Vectors.norma(point)

  @staticmethod
  def norma(point):
      return math.sqrt((point.x ** 2) + (point.y ** 2))

  @staticmethod
  def find_m(p1, p2):
      if (p1.x - p2.x) == 0:
          return None
      return (p1.y - p2.y)/(p1.x - p2.x)

  @staticmethod
  def find_b(p, m):
      return p.y - (m * p.x)

  @staticmethod
  def find_x_of_intersection(p1, p2, intersection_y):
      m = Vectors.find_m(p1, p2)
      return (intersection_y - Vectors.find_b(p1, m))/m

  @staticmethod
  def find_y_of_intersection(p1, p2, intersection_x):
      m = Vectors.find_m(p1, p2)
      return (m * intersection_x) + Vectors.find_b(p1, m)
