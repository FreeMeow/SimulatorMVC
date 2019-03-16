import model.utils.global_utils as global_utils

class Vertex:

    def __init__(self, probability, starvation_time, point):
        self.point = point
        self.p = probability
        self.lv = 0  # last visit time
        self.ts = 0  # total starvation time
        self.st = starvation_time

    def cst(self, current_time):
        return global_utils.time_function(current_time - self.lv - self.st) # calculate elapsed time while considering the Beta factor (See Beta factor for more details)

    def __update_lv(self, current_time):
        self.lv = current_time

    def visit(self, current_time):
        temp_cst = self.cst(current_time)
        self.lv = current_time
        if self.cst(current_time) == 0: 
            self.ts += temp_cst
