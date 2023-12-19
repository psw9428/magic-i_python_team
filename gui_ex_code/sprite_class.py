import gui_core as gui
import os

window_width = 1200
window_height = 720

w = gui.Window('test', window_width, window_height)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data

class sprite :
    def __init__(self) :
        self.name = ''
        self.ID = 0
        self.hp = 0
        self.hp_max = self.hp
        self.stress = 0
        self.speed = 0
        self.critical = 0
        self.defense = 0
        self.miss = 0
        self.src = ''

    class skill :
        def __init__(self) :
            self.name = ''
            self.damage = 0
            self.stress = 0
            

