import math
from model.entities.point import Point

def json_to_world(json):
  return {
    'name' : json["name"],
    'width' : json["width"],
    'height' : json["height"],
    'robot' : json_to_robot(json["robot"]),
    'obstacles' : json_to_obstacles(json["obstacles"]),
    'visit_points' : json_to_visit_points(json["visit_points"]),
  }

def json_to_robot(json):
  robot = {
    'walk_speed': 10,
    'rotation_speed': math.pi / 20,
    'start_angle': 0,
    'start_point': 0
  }
  robot.update(json)
  return robot

def json_to_obstacles(json):
  obstacles = []
  for json_obs in json:
    obs = [json_to_point(p) for p in json_obs]
    obstacles.append(obs)
  return obstacles

def json_to_visit_points(json):
  visit_points = []
  for vp in json:
    vis_po = {}
    vis_po.update(vp)
    vis_po['position'] = json_to_point(vp['position'])
    visit_points.append(vis_po)
  return visit_points

def json_to_point(json):
  return Point(json[0],json[1])