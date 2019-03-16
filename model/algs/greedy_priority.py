import model.utils.global_utils as global_utils 

class Greedy_priority:

  def __init__(self,world,distance_matrix,alg_args):
    self.world = world
    self.distance_matrix = distance_matrix

  def start(self):
    pass

  def next_step(self, current_vertex_ind, vertexes,current_time):
    max_ind = current_vertex_ind
    max_price = 0
    for i,v in enumerate(vertexes): # find the vertex with the maximum price
      current_v_price = global_utils.price(v.cst(current_time),v.p)
      if current_v_price > max_price:
        max_ind = i
        max_price = current_v_price
    return max_ind
  
  def output(self):
    return {}