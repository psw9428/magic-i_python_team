import json
import gui_core as gui
import os

w = gui.Window('test', 1024, 720)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data

def mouse_on_img(number) :
	x, y = w.getPosition(number)
	width, height = w.getSize(number)
	mouse_x = w.mouse_position_x
	mouse_y = w.mouse_position_y
	if (x <= mouse_x <= x + width and y <= mouse_y <= y + height) :
		return True
	else :
		return False

def resize_img(number, src, multi_number) :
	width, height = w.getSize(number)
	print(width, height)
	w.setImage(number, src, int(width * multi_number), int(height * multi_number))

def initialize(timestamp) :
	data.sprite_png = w.newImage(130, 300, cwd + '/src/res/sprite1.png', int(210 / 2), int(300 / 2), True)
	data.background = w.newImage(0, 0, cwd + '/src/res/background.png', 1024, 766, True)
	w.lowerObject(data.background)
	w.raiseObject(data.sprite_png)
	data.mouse_status = False
	

def update(timestamp):
	if (mouse_on_img(data.sprite_png)) :
		if (data.mouse_status == True) :
			return
		data.mouse_status = True
		data.pos = w.getPosition(data.sprite_png)
		data.size = w.getSize(data.sprite_png)
		w.moveObject(data.sprite_png, data.pos[0] - int(data.size[0] / 2), data.pos[1] - int(data.size[1] / 2))
		resize_img(data.sprite_png, cwd + '/src/res/sprite1.png', 2)
	elif (data.mouse_status == True) :
		w.setImage(data.sprite_png, cwd + '/src/res/sprite1.png', 105, 150)
		w.moveObject(data.sprite_png, data.pos[0], data.pos[1])
		data.mouse_status = False

w.initialize = initialize
w.update = update

w.start()
