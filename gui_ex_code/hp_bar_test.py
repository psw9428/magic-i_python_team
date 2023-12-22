import gui_core as gui
import os

window_width = 1280
window_height = 720

w = gui.Window('test', window_width, window_height)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data


def initialize(timestamp) :
    data.hpbar_red = w.newRectangle(10, 10, 100, 30, 'red', 1, 'white', True)
    data.hpbar_gray = w.newRectangle(10, 10, 100, 30, 'gray', 1, 'white', True)
    data.HP = 100
    data.MAXHP = 100
    
    w.raiseObject(data.hpbar_red)
    data.tmp = gui.time.perf_counter()

def update(timestamp) :
    if (data.tmp + 0.5 > timestamp) :
        return
    w.resizeObject(data.hpbar_red, int((data.HP / data.MAXHP) * 100), 30, 1)
    data.HP -= 5
    data.tmp = gui.time.perf_counter()

w.initialize = initialize
w.update = update

w.start()

