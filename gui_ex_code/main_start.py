import gui_core as gui
import os
import winsound

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
    def __init__(self, dir, num, last_delay = None, next_loop = None) :
        self.dir = dir
        self.num = num
        self.idx = 0
        self.cnt = 0
        self.tmp = None
        self.img_list = []
        self.flag = False
        self.delay_sec = 0
        self.last_delay = last_delay
        self.next_loop = next_loop
        for i in range(0, num) :
            self.img_list.append(w.newImage(0, 0, dir+str(i+1)+'.png', window_width, window_height, False))
    
    def scene_func(self, delay_sec = 2) :
        self.delay_sec = delay_sec
        self.tmp = gui.time.perf_counter()
        w.update = self.scene_func__
        
    def scene_func__(self, timestamp) :
        if (self.flag == False) :
            w.showObject(self.img_list[self.idx])
            if (self.idx != 0) :
                w.hideObject(self.img_list[self.idx - 1])
            self.flag = True
        if (self.tmp + self.delay_sec > timestamp) :
            return
        self.idx += 1
        self.flag = False
        if (self.idx == self.num) :
            if (self.last_delay != None) :
                gui.time.sleep(self.last_delay)
            w.hideObject(self.img_list[self.idx - 1])
            if (self.next_loop == None) :
                w.update = update
            else :
                w.update = self.next_loop
        self.tmp = gui.time.perf_counter()

class sprite :
    def __init__(self, name = 'man') :
        self.name = name
        self.ID = 0
        self.x = 0
        self.y = 0
        self.width = 48
        self.height = 48
        self.hp = 0
        self.hp_max = self.hp
        self.stress = 0
        self.speed = 0
        self.critical = 0
        self.defense = 0
        self.miss = 0
        self.img_idx = 0
        self.img_idx_num = 4
        self.show_status = False
        self.src = cwd + '/src/res/sprite/' + self.name + '1.png'
        self.img = w.newImage(self.x, self.y, self.src, self.width, self.height, False)
        self.tmp = 0

    def show(self) :
        w.showObject(self.img)
        w.show_status = True
    
    def move(self, xx, yy) :
        w.moveObject(self.img, xx, yy)

    def idle_loop(self, timestamp) :
        if (self.tmp + 0.2 > timestamp) :
            return
        if (self.show_status == False) :
            self.show()
        self.src = cwd + '/src/res/sprite/' + self.name + str(self.img_idx % self.img_idx_num + 1) + '.png'
        w.setImage(self.img, self.src, self.width * 3, self.height * 3)
        self.img_idx += 1
        self.tmp = gui.time.perf_counter()

    class skill :
        def __init__(self) :
            self.name = ''
            self.damage = 0
            self.stress = 0
    


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
    data.start_back = w.newImage(0, 0, cwd + '/src/res/background/start.png', window_width, window_height, False)
    data.man = sprite('man')
    data.man.move(300,300)
    game_intro = scene_class(cwd + '/src/res/intro/intro_logo', 21, 2)
    winsound.PlaySound(cwd + '/src/res/bgm/main_bgm.wav', winsound.SND_ASYNC)
    data.start_btn = btn_class(cwd + '/src/res/button/start_btn', 500, 450, 220, 70)
    game_intro.scene_func(0.1)


def update(timestamp) :
    w.showObject(data.start_back)
    data.start_btn.show()
    if (data.start_btn.in_loop()) :
        data.start_btn.hide()
        w.update = data.man.idle_loop


w.initialize = initialize
w.update = update

w.start()
