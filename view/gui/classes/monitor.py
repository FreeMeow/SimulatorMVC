from tkinter import *
import math
import view.gui.classes.utils.drawer as drawer
class Monitor:

    def __init__(self,root,width,height):
        self.root = root
        self.width = width
        self.height = height
        self.create_canvas()
    

    def setEngine(self, engine):
        self.engine = engine
    

    def create_canvas(self):
        self.canvas = Canvas(self.root, width=self.width, height = self.height)
        self.canvas.pack()
    
    def init_objects(self, vertexes, robot_location, obstacles, additional):
        self.canvas.create_rectangle(1,1,self.width,self.height)
        self.robot = drawer.create_robot(self.canvas,robot_location['position'])
        if 'clusters' in additional:
            vertexes = [{**v,'cluster': next(c_i for c_i,c in enumerate(additional['clusters']) if v_i in c)} for v_i,v in enumerate(vertexes)]
        self.verts = [drawer.create_vertex(self.canvas,v) for v in vertexes]
        self.verts_static = vertexes
        for ob in obstacles:
            self.canvas.create_line(ob[0].x, ob[0].y, ob[1].x, ob[1].y)
    
    def drawFrame(self,frame,ind):
        pos = frame['position']
        ang = frame['angle']
        drawer.update_robot(self.canvas,self.robot,pos,ang)
        for v,v_static,v_live in zip(self.verts,self.verts_static,frame['vertexes']):
            drawer.update_vertex(self.canvas,v,v_static,v_live,ind,self.engine.show_text)
        if 'message' in frame:
            pass
        self.canvas.update()

