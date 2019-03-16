from controller.controller import Controller
from view.viewCLI import ViewCLI
from model.model import Model

def run():
  c = Controller()
  v = ViewCLI(c)
  m = Model(c)
  c.model = m
  c.view = v

  v.start()

run()