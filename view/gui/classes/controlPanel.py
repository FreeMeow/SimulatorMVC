from tkinter import *

class ControlPanel:

    def __init__(self,root,num_of_frames, width):
        self.root = root
        self.width = width
        self.num_of_frames = num_of_frames
        self.create_controllers()


    def setEngine(self, engine ):
        self.engine = engine


    def create_controllers(self):
        self.frame = Frame(self.root, width=self.width, height=40)
        self.frame.pack(fill='x', pady=10)
        self.play_pause_button = Button(self.frame,width=10, text='Play', height=2, command=self.play_or_pause)
        self.play_pause_button.pack(side='left', padx=10)
        self.reset_button = Button(self.frame,width=10, text='Reset', height=2, command=self.jump_to_start)
        self.reset_button.pack(side='left', padx=10)
        self.timeline = Scale(self.frame, orient=HORIZONTAL, length=250, to=self.num_of_frames, command=self.jump_to_frame)
        self.timeline.pack(side='left')
        self.text_checkbox = Checkbutton(self.frame,text='Show text',command=self.toggle_text)
        self.text_checkbox.pack(side='top')


    def play_or_pause(self):
        isPlaying = self.engine.play_or_pause()
        if isPlaying:
            self.play_pause_button.config( text = 'Pause')
        else:
            self.play_pause_button.config( text = 'Play')


    def jump_to_start(self):
        self.jump_to_frame(0)


    def update_timeline(self,value):
        self.timeline.set(value)

    
    def jump_to_frame(self,newFrame):
        self.engine.jump_to_frame(int(newFrame))


    def toggle_text(self):
        isOn = self.engine.toggle_text()
        if isOn:
            self.text_checkbox.select()
        else:
            self.text_checkbox.deselect()
