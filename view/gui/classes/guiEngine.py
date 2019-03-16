import time

class GuiEngine:
    def __init__(self,control_panel,monitor,scenerio):
        self.control_panel = control_panel
        self.monitor = monitor
        
        self.scenerio = scenerio

        self.is_playing = False
        self.show_text = True,
        self.frame_index = 0


    def start(self):
        world = self.scenerio['world']
        additional = self.scenerio['alg_output']
        self.monitor.init_objects(world['visit_points'],world['visit_points'][world['robot']['start_point']],world['obstacles'],additional)
        prev_frame_index = -1
        while self.frame_index < len(self.scenerio['frames']):
            time.sleep(0.025)
            if self.frame_index != prev_frame_index:
                self.monitor.drawFrame(self.scenerio['frames'][self.frame_index],self.frame_index)
            else:
                self.monitor.canvas.update()
            prev_frame_index = self.frame_index
            self.control_panel.update_timeline(self.frame_index)
            if self.is_playing and self.frame_index + 1 < len(self.scenerio['frames']):
                self.frame_index += 1


    def play_or_pause(self):
        if self.is_playing:
            self.is_playing = False
        else:
            self.is_playing = True
        return self.is_playing


    def jump_to_frame(self,newFrame):
        self.frame_index = newFrame

    
    def toggle_text(self):
        self.show_text = not self.show_text 
        return self.show_text
