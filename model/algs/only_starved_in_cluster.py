from collections import deque
import model.utils.global_utils as global_utils 
import model.utils.algo_utils as algo_utils

class Only_starved_in_cluster:

  def __init__(self,world,distance_matrix,alg_args):
    self.world = world
    self.distance_matrix = distance_matrix
    self.args = alg_args
    self.queue = deque([])

  def start(self):
    self.clusters = algo_utils.dbscan_clustering(
      self.world['visit_points'],
      int(self.args['maxd']), # maximum distance (See DBSCAN prop for more details)
      int(self.args['minp']) # minimum points (See DBSCAN prop for more details)
    )

  def next_step(self, current_vertex_ind, vertexes,current_time):
    if not self.queue: #if queue of next visits is empty
      max_cluster = self.clusters[0]
      max_price = 0
      for cluster in self.clusters: # find the cluster with the highest price
        cluster_price = 0
        for v_i in cluster: # calculate cluster's price
          v = vertexes[v_i]
          cluster_price += global_utils.price(v.cst(current_time),v.p)
        if cluster_price > max_price:
          max_cluster = cluster
          max_price = cluster_price

      # sort cluster so the robot visit the highest price in the cluster first
      vs_of_cluster = [(i,global_utils.price(vertexes[i].cst(current_time),vertexes[i].p)) for i in max_cluster]
      vs_of_cluster = [v for v in vs_of_cluster if v[1] > 0] # filter out all vertexes in cluster that has price=0
      vs_of_cluster.sort(key = lambda v:v[1], reverse = True)
      self.queue.extend(map(lambda v:v[0],vs_of_cluster))

    if self.queue:
      next_v = self.queue.popleft()
    else:
      next_v = current_vertex_ind
    return next_v

  def output(self):
      return {
        'clusters': self.clusters
      }