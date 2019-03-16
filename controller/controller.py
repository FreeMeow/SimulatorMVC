from model.model import Model

class Controller:
  def __init__(self):
    self.model = None
    self.view = None

  def check_for_model(self):
    if not self.model:
      raise ValueError("Model hasn't assigned for the Controller.")

  def check_for_view(self):
    if not self.view:
      raise ValueError("View hasn't assigned for the Controller.")
      
  # V -> M
  def load_world_from_file(self,path):
    self.check_for_model()
    return self.model.load_world_from_file(path)

  def run_algorithm_on_world(self,algo,algo_args,tpd):
    self.check_for_model()
    return self.model.run_algorithm_on_world(algo,algo_args,tpd)

  def get_scenerio_for_gui(self):
    self.check_for_model()
    return self.model.get_scenerio_for_gui()

  def get_scenerio_info(self):
    self.check_for_model()
    return self.model.get_scenerio_info()

  def set_const(self,const_name,new_value):
    self.check_for_model()
    return self.model.set_const(const_name,new_value)
  