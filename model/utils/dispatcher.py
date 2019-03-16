import copy
import importlib
import math
import model.utils.dijakstra as dijakstra
import model.utils.dispatcher_utils as dispatcher_utils
from model.entities.vertex import Vertex
from model.entities.point import Point

def run_algorithm_on_world(world,alg_name,alg_args,tpd):
  vertexes = create_vertexes_from_visit_points(world)
  algo = import_algorithm(alg_name)
  patrol,alg_output = start_patrol(world,algo,alg_args,tpd,vertexes)
  statistic = caclulate_statistic(world,vertexes,alg_name,tpd)
  return {
    'world': world,
    'frames': patrol,
    'statistic': statistic,
    'alg_output': alg_output,
  }

def create_vertexes_from_visit_points(world):
  return [Vertex(vp['probability'],vp['starvation'],vp['position']) for vp in world['visit_points']]

def import_algorithm(alg_name):
  try:
    algo_module = importlib.import_module('model.algs.{}'.format(alg_name)) # dynamic import of module by alg name
    return getattr(algo_module,alg_name.capitalize())
  except ModuleNotFoundError:
    raise NameError("the algorithm: '{}' doesn't exist!".format(alg_name))

def start_patrol(world,algo_type,alg_args,tpd,vertexes):
  distance_matrix = create_distance_matrix(world)
  global_time = 0
  robot = {
    'position': vertexes[world['robot']['start_point']].point,
    'current_vertex': world['robot']['start_point'],
    'angle': world['robot']['start_angle'],
    'walk_speed': world['robot']['walk_speed'],
    'rotation_speed': world['robot']['rotation_speed'],
  }
  patrol = []
  algo = algo_type(world,distance_matrix,alg_args)
  algo.start() # some of the algorithms has preprocessing to do so the dispatcher let them do the calculations first
  while global_time < tpd:
    next_vertex = algo.next_step(robot['current_vertex'],vertexes,global_time)
    frames_of_path = path_to_goal(robot, world, next_vertex) # get the frames of the current path
    for i,f in enumerate(frames_of_path): # check each frame if it has an unexcpected visit (if a visit-point is in the best way to target)
      v_props = []
      for j,v in enumerate(vertexes):
        if f['position'] == v.point:
          v.visit(global_time + i)
        v_props.append({ # adding metadata to each frame to display later in gui view
          'last_visit': v.lv,
          'total_starvation': v.ts,
          'is_target': next_vertex == j,
        })
      f['vertexes'] = v_props

    robot['current_vertex'] = next_vertex
    robot['angle'] = frames_of_path[-1]['angle'] # update robot's angle to last angle in path
    global_time += len(frames_of_path)
    vertexes[next_vertex].visit(global_time)
    patrol.extend(frames_of_path)
  
  alg_output = algo.output() # collecting output from the algorithm if exists (for example: the clusters)
  return patrol,alg_output

def path_to_goal(robot, world, next_vertex):
  return complex_path_steps(world,robot['angle'],robot['current_vertex'],next_vertex)

def create_distance_matrix(world):
  vps = world['visit_points']
  matrix = [[0] * len(vps)] * len(vps)
  for i,_ in enumerate(vps):
    for j,_ in enumerate(vps):
      matrix[i][j] = complex_path_length(world,i,j)
  return matrix

def complex_path_length(world,vp_src,vp_dst):
  return len(complex_path_steps(world,0,vp_src,vp_dst))

def complex_path_steps(world,current_angle,vp_src,vp_dst):
  path = dijakstra.get_points_path_with_dijakstra(world,world['visit_points'][vp_src]['position'],world['visit_points'][vp_dst]['position'])
  frames = [{'position':path[0],'angle':current_angle}]
  if len(path) > 1:
    for i in range(0, len(path) - 1):
      frames += simple_path_steps(path[i],frames[-1]['angle'], path[i + 1], world['robot']['walk_speed'], world['robot']['rotation_speed'])
  return frames

def simple_path_steps(p_src,current_angle, p_dst,walk_speed,rotation_speed):
  frames = []
  target_angle = dispatcher_utils.calculate_new_angle(p_src,p_dst)
  frames = dispatcher_utils.get_rotation_frames(current_angle,target_angle,p_src,rotation_speed)
  total_distance = int(math.sqrt(((p_dst.x - p_src.x)**2) + ((p_dst.y - p_src.y)**2)))
  for step in range(0,total_distance,walk_speed):
      frames.append({'angle': target_angle, 'position': Point(p_src.x + math.cos(target_angle) * step,p_src.y + math.sin(target_angle)* step)})
  frames.append({'angle': target_angle, 'position':p_dst})
  return frames

def caclulate_statistic(world,vertexes,alg_name,tpd):
  for v in vertexes: # visit all vertexes at the end of the patrol to sum up the cst of all the vertexes
    v.visit(tpd)
  stat = {
    'total_price': sum([v.ts * v.p for v in vertexes]),
    'alg_name': alg_name,
    'tpd': tpd,
    'num_of_vertexes': len(vertexes)
  }
  return stat
