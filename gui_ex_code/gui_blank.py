'''
gui 모듈을 사용하기 위한 기본 구조를 미리 적어 둔 파일입니다.

- 여러분은 이 아래에 있는, 함수 initialize()와 update()에 대한
  함수 정의 내용물을 구성함으로써 프로그램을 구성해야 해요

- 중간중간 F5를 눌러 interactive를 켜 둔 다음 진행하면
  IDLE이 함수 호출식 적을 때마다 적당한 툴팁을 읽어 보여줄 거예요
'''

import json
import gui_core as gui
import os

w = gui.Window('test', 1024, 600)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data


def initialize(timestamp):
	with open(cwd + '/src/json/test.json', 'r') as f :
		data.character = dict(json.load(f))
	data.sprite = []
	data.sprite_png = [cwd + '/src/res/sprite1.png', cwd + '/src/res/sprite2.png']
	data.sprite.append(w.newImage(130, 300, data.sprite_png[0], int(210 / 2), int(300 / 2), True))
	data.sprite.append(w.newImage(700, 300, data.sprite_png[0], int(210 / 2), int(300 / 2), True))
	data.bigsprite = []
	data.bigsprite.append(w.newImage(20, 10, data.sprite_png[1], int(687), int(652), False))
	data.bigsprite.append(w.newImage(500, 10, data.sprite_png[1], int(687), int(652), False))
	w.lowerObject(w.newImage(0,0, cwd + '/src/res/background.png', 1024, 766, True))
	data.mousetxt = w.newText(20, 20, 150, '마우스 위치 : ', anchor='nw', fill_color='#FF0000')
	data.cooltime = None
	
	w.resizeObject(data.sprite[0], int(210 / 2), int(300 / 2), 10)
	w.recolorObject(data.sprite[0], '', '#FF0000')
	data.rgb = '#FF0000'


def next_rgb(rgb) :
	rgb = rgb[1:]
	tmp = list(rgb)
	if (rgb[0:2] == 'FF') :
		if (rgb[4:6] != '00') :
			ttt = int(rgb[4:6], 16)
			tmp[4] = format(ttt - 3, '02X')[0]
			tmp[5] = format(ttt - 3, '02X')[1]
		if (rgb[2:4] != 'FF') :
			ttt = int(rgb[2:4], 16)
			tmp[2] = format(ttt + 3, '02X')[0]
			tmp[3] = format(ttt + 3, '02X')[1]
		else :
			tmp[1] = 'A'
	elif (rgb[2:4] == 'FF') :
		if (rgb[0:2] != '00') :
			ttt = int(rgb[0:2], 16)
			tmp[0] = format(ttt - 5, '02X')[0]
			tmp[1] = format(ttt - 5, '02X')[1]
		elif (rgb[4:6] != 'FF') :
			ttt = int(rgb[4:6], 16)
			tmp[4] = format(ttt + 5, '02X')[0]
			tmp[5] = format(ttt + 5, '02X')[1]
		else :
			tmp[3] = 'A'
	elif (rgb[4:6] == 'FF') :
		if (rgb[2:4] != '00') :
			ttt = int(rgb[2:4], 16)
			tmp[2] = format(ttt - 5, '02X')[0]
			tmp[3] = format(ttt - 5, '02X')[1]
		elif (rgb[0:2] != 'FF') :
			ttt = int(rgb[0:2], 16)
			tmp[0] = format(ttt + 5, '02X')[0]
			tmp[1] = format(ttt + 5, '02X')[1]
	return '#' + ''.join(tmp)
	
	

def update(timestamp):
	w.setText(data.mousetxt, '마우스 위치 : ' + str(w.mouse_position_x) + ', ' + str(w.mouse_position_y))
	data.rgb = next_rgb(data.rgb)
	print(data.rgb)
	w.recolorObject(data.mousetxt, data.rgb, data.rgb)
		
		
	if w.mouse_buttons[1] :
		data.cooltime = timestamp
		w.showObject(data.bigsprite[0])
		w.showObject(data.bigsprite[1])
		w.update = attack

def attack(timestamp) :
	if (timestamp < data.cooltime + 2.0) :
		x1, y1 = w.getPosition(data.bigsprite[0])
		x2, y2 = w.getPosition(data.bigsprite[1])
		w.moveObject(data.bigsprite[0], x1 + 0.5, y1)
		w.moveObject(data.bigsprite[1], x2 + 0.2, y2)
	else :
		w.hideObject(data.bigsprite[0])
		w.hideObject(data.bigsprite[1])
		w.moveObject(data.bigsprite[0], 20, 10)
		w.moveObject(data.bigsprite[1], 500, 10)
		data.cooltime = None
		w.update = update

w.initialize = initialize
w.update = update

w.start()
