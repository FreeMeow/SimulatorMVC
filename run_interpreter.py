from controller.controller import Controller
from view.viewInterpreter import ViewInterpreter
from model.model import Model

import sys

def run():
  c = Controller()
  v = ViewInterpreter(c)
  m = Model(c)
  c.model = m
  c.view = v
  if len(sys.argv) >= 2:
    # print(sys.argv[1])
    v.prestart(sys.argv[1])
  else:
    v.prestart()
  v.start()

run()