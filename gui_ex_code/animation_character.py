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

num = 1

def initialize(timestamp):
	data.sprite = w.newImage(300, 300, cwd + '/src/res/Dead1.png', 800, 860, True)

import time

def update(timestamp):
	global num
	w.setImage(data.sprite, cwd + '/src/res/Dead' + str((num % 6) + 1) + '.png')
	num += 1

w.initialize = initialize
w.update = update

w.start()
