import random

class Random_starved:
  def __init__(self,world,distance_matrix,alg_args):
    self.world = world
    self.distance_matrix = distance_matrix
    self.args = alg_args

  def start(self):
    pass

  def next_step(self, current_vertex_ind, vertexes,current_time):
    only_starved = [i for i,v in enumerate(vertexes) if v.cst(current_time) > 0]
    if only_starved:
      return only_starved[random.randint(0,len(only_starved)-1)]
    return current_vertex_ind

  def output(self):
    return {}

