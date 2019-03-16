import threading
from tkinter import *
import time

from view.gui.classes.controlPanel import ControlPanel
from view.gui.classes.guiEngine import GuiEngine
from view.gui.classes.monitor import Monitor


class ScenerioDisplayer:

    def __init__(self,scenerio,width=600,height=600):
        root = Tk()
        monitor = Monitor(root, width, height)
        control_panel = ControlPanel(root, len(scenerio['frames']),width)
        engine = GuiEngine(control_panel, monitor, scenerio)
        control_panel.setEngine(engine)
        monitor.setEngine(engine)
        try:
            engine.start()
        except TclError as e:
            print("GUI closed.")