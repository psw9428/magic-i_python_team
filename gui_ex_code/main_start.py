import gui_core as gui
import os
import winsound
import json

window_width = 1280
window_height = 720

w = gui.Window('test', window_width, window_height)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data
turn_flag = False

main_screen = 0
story_scene = 1
stage1 = 2

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
        self.img = w.newImage(0, 0, dir+'1.png', window_width, window_height, False)
        for i in range(0, num) :
            self.img_list.append(w.newImage(0, 0, dir+str(i+1)+'.png', window_width, window_height, False))
    
    def scene_func(self, delay_sec = 2) :
        self.delay_sec = delay_sec
        self.tmp = gui.time.perf_counter()
        w.update = self.scene_func__

    def scene_func__(self, timestamp) :
        if (self.idx == 0) :
            w.showObject(self.img)
        elif (self.idx != self.num) :
            w.setImage(self.img, self.dir+str(self.idx+1)+'.png')
        if (self.tmp + self.delay_sec > timestamp) :
            return
        # if (self.idx == 0) :
        #     w.showObject(self.img)
        # elif (self.idx != self.num) :
        #     w.setImage(self.img, self.dir+str(self.idx+1)+'.png')
        self.idx += 1
        if (self.idx == self.num + 1) :
            if(self.last_delay != None) :
                gui.time.sleep(self.last_delay)
            w.hideObject(self.img)
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
        self.damage = 0
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
        self.shadow = w.newImage(self.x, self.y, cwd+'/src/res/shadow.png', 48, 48, False)
        self.balloon = w.newImage(self.x, self.y, cwd+'/src/res/balloon/balloon1_right.png', 192, 96, False)
        self.balloon_status = False
        self.says = None
        self.status = 'normal'

    def print_info(self) :
        print(self.name)
        print(self.ID)
        print(self.width)
        print(self.height)
        print(self.hp)
        print(self.damage)
        print(self.speed)
        print(self.critical)
        print(self.defense)
        print(self.miss)
        print(self.says)

    def show(self) :
        w.raiseObject(self.img)
        w.showObject(self.img)
        self.show_status = True

    def hide(self) :
        w.hideObject(self.img)
        self.show_status = False
    
    def move(self, xx, yy) :
        self.x = xx
        self.y = yy
        w.moveObject(self.img, xx, yy)

    def mouse_on_sprite(self) :
        if (self.x <= w.mouse_position_x <= self.x + self.width and self.y <= w.mouse_position_y <= self.y + self.height) :
            return True
        else :
            return False
    
    def say_balloon(self, timestamp, saying, duration) :
        if (data.change_update_time + duration < timestamp) :
            w.hideObject(self.balloon)
            w.hideObject(self.say)
            return
        if (self.balloon_status == False) :
            x = self.x + int(self.width / 2)
            y = self.y - self.height
            w.moveObject(self.balloon, x, y)
            w.raiseObject(self.balloon)
            w.showObject(self.balloon)
            self.say = w.newText(x + 20, y + 25, 152, saying, 'white', anchor='nw')
            self.balloon_status = True
        
    def idle_loop(self, timestamp) :
        if (self.say != None) :
            self.say_balloon(timestamp, self.say, 4)
        if (self.mouse_on_sprite()) :
            w.moveObject(self.shadow, self.x, self.y)
            w.raiseObject(self.shadow)
            w.setImage(self.shadow, cwd+'/src/res/shadow.png', self.width, self.height)
            w.showObject(self.shadow)
            self.show()
        else :
            w.hideObject(self.shadow)
        if (self.tmp + 0.2 > timestamp) :
            return
        if (self.show_status == False) :
            self.show()
        self.src = cwd + '/src/res/sprite/' + self.name + str(self.img_idx % self.img_idx_num + 1) + '.png'
        self.width, self.height = 48 * 4, 48 * 4
        w.setImage(self.img, self.src, self.width, self.height)
        self.img_idx += 1
        self.tmp = gui.time.perf_counter()

    def myturn(self) :
        pass


    class balloon :
        def __init__(self, saying, direction = 'right') :
            super().balloon = self
            self.img = w.newImage(super().x, super().y, cwd+'/src/res/balloon/balloon1_'+direction+'.png', False)
            self.make_time = gui.time.perf_counter()
    class skill :
        def __init__(self) :
            self.name = ''
            self.damage = 0
            self.stress = 0


def data_setting() :
    with open(cwd + '/src/json/test.json', 'r', encoding='UTF-8') as f :
        dic = dict(json.load(f))
    data.sprite_list = {}
    for i in dic :
        data.sprite_list[i] = sprite(i)
        tmp = data.sprite_list[i]
        tmp.ID = dic[i]["ID"]
        tmp.width = dic[i]["width"]
        tmp.height = dic[i]["height"]
        tmp.speed = dic[i]["speed"]
        tmp.critical = dic[i]["critical"]
        tmp.defense = dic[i]["defense"]
        tmp.miss = dic[i]["miss"]
        tmp.img_idx_num = dic[i]["img_idx_num"]
        tmp.damage = dic[i]["damage"]
        tmp.hp = dic[i]["hp"]
        tmp.hp_max = tmp.hp
        tmp.says = dic[i]["says"]

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
    data_setting()
    data.sprite_list["man"].print_info()
    data.shadow = w.newImage(0, 0, cwd + '/src/res/shadow.png', 48, 48, False)
    data.start_back = w.newImage(0, 0, cwd + '/src/res/background/start.png', window_width, window_height, False)
    data.game_status = 0 # 라운드 판별..?
    data.flag = False #요긴하게
    data.sprite_list["man"].move(300, 300)
    data.sprite_list["woman"].move(600, 300)
    game_intro = scene_class(cwd + '/src/res/intro/intro_logo', 21, 2)
    winsound.PlaySound(cwd + '/src/res/bgm/main_bgm.wav', winsound.SND_ASYNC)
    data.start_btn = btn_class(cwd + '/src/res/button/start_btn', 500, 450, 220, 70)
    game_intro.scene_func(0.1)

def turn(timestamp) :
    global turn_flag
    if (turn_flag == False) :
        data.sprite_list['man'].say = '아 X마려운데 화장실 없냐?'
        data.sprite_list["man"].show()
        data.sprite_list["woman"].show()
        turn_flag = True

    data.sprite_list["man"].idle_loop(timestamp)
    data.sprite_list["woman"].idle_loop(timestamp)




def update(timestamp) :

    if (data.game_status == 0) :
        w.showObject(data.start_back)
        data.start_btn.show()
        if (data.start_btn.in_loop()) :
            data.start_btn.hide()
            data.change_update_time = gui.time.perf_counter()
            data.game_status = story_scene
            scene_class(cwd+'/src/res/scene/intro_scene', 11, 3).scene_func(2)
    if (data.game_status == 1) :
        pass




w.initialize = initialize
w.update = update

w.start()