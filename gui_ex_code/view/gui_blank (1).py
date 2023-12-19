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


w = gui.Window('test', 1280, 720)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data

global enemyCount
global phaseCount
	
class stageOne:
	def __init__(self, character, stageOne_mob):
		self.character = []
		self.character[0] = character[0]
		self.character[1] = character[1]
		self.character[2] = stageOne_mob[0]
		self.character[3] = stageOne_mob[1]
		self.character[4] = stageOne_mob[2]
	
	def phase(self, num):
		speed = []
		for char in self.character:
			speed.append(char.ID, char.speed)
		info_speed = sort_speed(speed)
		for i in info_speed:
			for char in self.character:
				if info_speed[i] == char.ID:
					self.turn(i))
					if self.character[0] == None and self.character[1] == None:
						#game over.
						w.stop()
					if self.character[2] == None and self.character[3] == None and self.character[4] == None:
						#stage end
						pass
		self.phase(num+1)
		
	def turn(self, pos):
		#check if who's condition
		if self.character[pos].state.num % 2 == 0:
			self.character[pos].state.poison[0] -= 1
			self.character[pos].HP = self.character[pos].HP - self.character[pos].state.poison[1]
			if self.character[pos].HP <= 0:
				self.character[pos] = None
				return
			if self.character[pos].state.posion[0] == 0:
				self.character[pos].state.poison[1] = 0
				self.character[pos].state.num  /=  2
		if self.character[pos].state.num % 3 == 0:
			self.character[pos].state.bleed[0] -= 1
			self.character[pos].HP = self.character[pos].HP - self.character[pos].state.bleed[1]
			if self.character[pos].HP <= 0:
				self.character[pos] = None
				return
			if self.character[pos].state.bleed[0] == 0:
				self.character[pos].state.bleed[1] = 0
				self.character[pos].state.num  /= 2
		if self.character[pos].state.num % 5 == 0:
			self.character[pos].state.num /= 5
			return
		
		#do the turn
		#select 



		



		pass

		
		

def initialize(timestamp):
	pass

def sort_speed(char):
	#char는 캐릭터 ID, 속도 튜플의 리스트
	char_id = list(0 for i in range(0, len(char)))
	char_speed = list(0 for i in range(0, len(char)))
	for i in range(0, len(char)):
		char_id[i], char_speed[i] = char[i]
	
	#char_speed 내림차순으로 sorting
	for i in range(0, len(char_speed)-1):
		for j in range(i+1, len(char_speed)):
			if char_speed[j] > char_speed[i]:
				tmp = char_id[i]
				char_id[i] = char_id[j]
				char_id[j] = tmp

	return char_id

def stage1__(timestamp):
	global enemyCount
	global phaseCount

	
def turn__(timestamp):


	





def update(timestamp):
# 	w.setText(data.mousetxt, '마우스 위치 : ' + str(w.mouse_position_x) + ', ' + str(w.mouse_position_y))
		
# 	if w.mouse_buttons[1] :
# 		data.cooltime = timestamp
# 		w.showObject(data.bigsprite[0])
# 		w.showObject(data.bigsprite[1])
# 		w.update = attack

# def attack(timestamp) :
# 	if (timestamp < data.cooltime + 2.0) :
# 		x1, y1 = w.getPosition(data.bigsprite[0])
# 		x2, y2 = w.getPosition(data.bigsprite[1])
# 		w.moveObject(data.bigsprite[0], x1 + 0.5, y1)
# 		w.moveObject(data.bigsprite[1], x2 + 0.2, y2)
# 	else :
# 		w.hideObject(data.bigsprite[0])
# 		w.hideObject(data.bigsprite[1])
# 		w.moveObject(data.bigsprite[0], 20, 10)
# 		w.moveObject(data.bigsprite[1], 500, 10)
# 		data.cooltime = None
# 		w.update = update
	
#배경 이미지 1개
#시작 화면 컷씬
	
	#캐릭터 구성요소

	#이름
	#ID
	#체력
	#스트레스
	#속도
	#치명타
	#방어력
	#회피
	#이미지(평상시 4개, 공격 3개, 맞는 거 1개, 붕괴 1개, 각성 1개, 시체 1개, 회피 1개)
	#스킬
		#instantKill = True(창), instantKill = False(다른 모든 애들 + 3스테이지의 창)
		#데미지
		#가하는 스트레스
		#otherEffect = False(그냥 데미지만), otherEffect = True(스턴 혹은 다른 이펙트 있음)
	
	#effectArrary = [stun, stress, bleed, downstress, posion, block]
	#stressAmount = 0
	#bleedDamage = 0
	#downstress = 0
	#poisonAmount = 0
	#스턴: 기절 효과
	#스트레스: 스트레스 가하는 공격
	#출혈: 턴당 데미지 가하는 것
	#대사 승리, 죽음, 각성, 붕괴, 치명타, 막타

	#==================================초반 컷씬==========================================
	#=====================================================================================
	w.update = start
	#==================================스테이지 1=========================================
	w.update = stage1

	w.update = scene1

	#==================================스테이지 2=========================================
	w.update = stage2

	w.update = scene2

	#==================================스테이지 3=========================================
	w.update = stage3

	w.update = ending
	w.update = select1
	w.update = select2


	w.stop()








	

w.initialize = initialize
w.update = update

w.start()
