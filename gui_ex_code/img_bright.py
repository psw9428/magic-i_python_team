import gui_core as gui
import os
from PIL import Image, ImageTk, ImageEnhance

w = gui.Window('test', 1024, 720)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data

class scene_class :
    def __init__(self, dir, num) :
        self.dir = dir
        self.num = num
        self.idx = 0
        self.cnt = 0
        self.tmp = None
        self.img_list = []
        for i in range(0, num) :
            self.img_list.append(Image.open(dir+str(i + 1) + '.png'))
            for j in range(0, 6) :
                self.img_list[i] = ImageEnhance.Brightness(self.img_list[i]).enhance(0.5)
    
    def scene_func(self) :
        self.tmp = gui.time.perf_counter()
        w.update = self.scene_func__
        
    def scene_func__(self, timestamp) :
        if (self.tmp + 0.1 > timestamp) :
            return
        if (self.cnt < 6) :
            enhancer = ImageEnhance.Brightness(self.img_list[self.idx])
            self.img_list[self.idx] = enhancer.enhance(2)
            #w.internals_neednolook.canvas.create_image(0, 0, anchor=gui.tkinter.NW, image=self.img_list[self.idx], state=gui.tkinter.NORMAL)
            tk_img = ImageTk.PhotoImage(self.img_list[self.idx])
            labell = gui.tkinter.Label(image=tk_img)
            labell.image = tk_img
            labell.place(x = 0, y = 0)
            self.cnt += 1
        elif (self.cnt == 6 and self.tmp + 2 > timestamp) :
            return
        elif (self.cnt < 12) :
            enhancer = ImageEnhance.Brightness(self.img_list[self.idx])
            self.img_list[self.idx] = enhancer.enhance(0.5)
            #w.internals_neednolook.canvas.create_image(0, 0, anchor=gui.tkinter.NW, image=self.img_list[self.idx], state=gui.tkinter.NORMAL)
            tk_img = ImageTk.PhotoImage(self.img_list[self.idx])
            labell = gui.tkinter.Label(image=tk_img)
            labell.image = tk_img
            labell.place(x = 0, y = 0)
            self.cnt += 1
            if (self.cnt == 12) :
                self.cnt = 0
                self.idx += 1
                if (self.idx == self.num) :
                    w.update = update
        self.tmp = gui.time.perf_counter()
        

def scence_func(dir, num) :
    for i in range(1, num + 1) :
        img = Image.open(dir + str(i) + '.png')
        for j in range(0, 3) :
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.5)
        for j in range(0, 3) :
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(2)
            tk_img = ImageTk.PhotoImage(img)
            labell = gui.tkinter.Label(image = tk_img)
            labell.image = tk_img
            labell.place(x=0, y=0)
            gui.time.sleep(0.5)    


def initialize(timestamp) :
    a = scene_class(cwd + '/src/res/scene/intro_scene', 11)
    a.scene_func()

def update(timestamp) :
    pass

w.initialize = initialize
w.update = update

w.start()
