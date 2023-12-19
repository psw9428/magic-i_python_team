import gui_core as gui
import os

window_width = 1280
window_height = 720

w = gui.Window('test', window_width, window_height)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data

class btn_class : 
    def __init__(self, src, x, y, width, height) :
        self.img = w.newImage(x, y, src + '_off.png', width, height, False)
        self.src = src
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def show(self) :
        w.showObject(self.img)
    
    def hide(self) :
        w.hideObject(self.img)
    
    def in_loop(self) :
        if (mouse_on_img(self.img)) :
            w.setImage(self.img, self.src + '_on.png', self.width, self.height)
            if (w.mouse_buttons[1]) :
                return True
        else :
            w.setImage(self.img, self.src + '_off.png', self.width, self.height)
        return False


class scene_class :
    def __init__(self, dir, num) :
        self.dir = dir
        self.num = num
        self.idx = 0
        self.cnt = 0
        self.tmp = None
        self.img_list = []
        self.flag = False
        self.delay_sec = 0
        for i in range(0, num) :
            self.img_list.append(w.newImage(0, 0, dir+str(i+1)+'.png', window_width, window_height, False))
    
    def scene_func(self, delay_sec = 2) :
        self.delay_sec = delay_sec
        self.tmp = gui.time.perf_counter()
        w.update = self.scene_func__
        
    def scene_func__(self, timestamp) :
        # if (self.tmp + 0.1 > timestamp) :
        #     return
        if (self.flag == False) :
            w.showObject(self.img_list[self.idx])
            self.flag = True
        if (self.tmp + self.delay_sec > timestamp) :
            return
        if (self.flag == True) :
            w.hideObject(self.img_list[self.idx])
            self.flag = False
        # if (self.tmp + 2.5 > timestamp) :
        #     return
        self.idx += 1
        if (self.idx == self.num) :
            w.update = update
        self.tmp = gui.time.perf_counter()

def mouse_on_img(number) :
	x, y = w.getPosition(number)
	width, height = w.getSize(number)
	mouse_x = w.mouse_position_x
	mouse_y = w.mouse_position_y
	if (x <= mouse_x <= x + width and y <= mouse_y <= y + height) :
		return True
	else :
		return False

def main_screen() :
    data.btn = w.newImage(500, 450, cwd+'/src/res/button/start_btn1.png', 220, 70, True)
    if (mouse_on_img(data.btn)) :
        w.setImage(data.btn, '/src/res/button/start_btn2.png', 220, 70)



def initialize(timestamp) :
    data.game_status = 0
    data.flag = False
    game_intro = scene_class(cwd + '/src/res/intro_logo_screen', 1)
    game_intro.scene_func(4)
    data.start_btn = btn_class(cwd + '/src/res/button/start_btn', 500, 450, 220, 70)
    data.start_btn.show()


def update(timestamp) :
    data.start_btn.in_loop()


w.initialize = initialize
w.update = update

w.start()
