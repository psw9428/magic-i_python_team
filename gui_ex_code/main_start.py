import gui_core as gui
import os
import winsound
import json
import random

window_width = 1280
window_height = 720

w = gui.Window('test', window_width, window_height)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data
turn_flag = False

main_screen = 0
story_scene = 1
stage1 = 2
stage = 0

global STUN #스턴 코드
STUN = 50099
global POISON #중독 코드
POISON = 20099
global BLEED #출혈 코드
BLEED = 30099
global FEAR #공포 코드
FEAR = 70099
global DEFENSE #대신맞기 코드
DEFENSE = 11199
global HEAL #힐 코드
HEAL = 22299
global STRESSHEAL
STRESSHEAL = 33399

global DESPAIR #절망 붕괴 코드
DESPAIR = 100199
global PARANOIA #편집증 붕괴 코드
PARANOIA = 100299
global SCHIZOPHRENIA #정신착란 붕괴 코드
SCHIZOPHRENIA = 100399

global RESURRECTOIN #기사회생 각성 코드
RESURRECTOIN = 200199
global CALM #차분한 영혼 각성 코드
CALM = 200299
global LAST_DANCE #회광반조 각성 코드
LAST_DANCE = 200399

global WA_SANZ #와 샌즈 각성 치트 코드
WA_SANZ = 999999 

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
	def __init__(self, dir, num, last_delay=None, next_loop=None, skip=False) :
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
		self.skip = skip
	
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
			if (w.mouse_buttons[1] == False or self.tmp + 0.2 > timestamp) :
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
		self.width = 48 * 4
		self.height = 48 * 4
		self.HP = 0
		self.MAXHP = self.HP
		self.stress = 0
		self.speed = 0
		self.hit = 0
		self.miss = 0
		self.img_idx = 0
		self.img_idx_num = 4
		self.show_status = False
		self.src = cwd + '/src/res/sprite/' + self.name + '1.png'
		print(self.src)
		self.img = w.newImage(self.x, self.y, self.src, 48, 48, False)
		self.tmp = 0
		self.shadow = w.newImage(self.x, self.y, cwd+'/src/res/shadow.png', 48, 48, False)
		self.balloon = w.newImage(self.x, self.y, cwd+'/src/res/balloon/balloon1_right.png', 192, 96, False)
		self.balloon_status = False
		self.says = None
		self.state = self.state_class()
		self.collapse = 0
		self.defender = 0
		self.refuse = self.refuse_class()
		self.skill = []
		self.onmouse = False
		self.skill_pos = [(400, 515), (480, 515), (560, 515), (640, 515)]
		self.info_txt = w.newText(500, 500, 500, '', 'white', 'nw', False)
		self.HP_gray = w.newRectangle(0, 0, 100, 20, 'gray', 1, 'white', False)
		self.HP_red = w.newRectangle(0, 0, 100, 20, 'red', 1, 'white', False)
		self.stress_back = w.newRectangle(0, 0, 100, 20, 'black', 1, 'white', False)
		self.stress_bar = w.newRectangle(0, 0, 0, 20, 'white', 1, 'white', False)

	def print_info(self) :
		print(self.name)
		print(self.ID)
		print(self.width)
		print(self.height)
		print(self.HP)
		print(self.speed)
		print(self.miss)
		print(self.says)
		print(self.skill)

	def display_info(self) :
		pass

	def show(self) :
		w.raiseObject(self.img)
		w.raiseObject(self.HP_gray)
		w.raiseObject(self.HP_red)
		w.raiseObject(self.stress_back)
		w.raiseObject(self.stress_bar)
		w.showObject(self.img)
		w.showObject(self.HP_gray)
		w.showObject(self.HP_red)
		w.showObject(self.stress_back)
		w.showObject(self.stress_bar)
		self.show_status = True

	def hide(self) :
		w.hideObject(self.img)
		w.hideObject(self.HP_gray)
		w.hideObject(self.HP_red)
		w.hideObject(self.stress_back)
		w.hideObject(self.stress_bar)
		self.show_status = False
	
	def move(self, xx, yy) :
		self.x = xx
		self.y = yy
		w.moveObject(self.HP_red , xx, yy + self.height + 20)
		w.moveObject(self.HP_gray, xx, yy +  self.height + 20)
		w.moveObject(self.stress_back, xx, yy + self.height + 40)
		w.moveObject(self.stress_bar, xx, yy +  self.height + 40)
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
		if (self.tmp + 0.2 > timestamp) :
			return
		self.src = cwd + '/src/res/sprite/' + self.name + str(self.img_idx % self.img_idx_num + 1) + '.png'
		self.width, self.height = 48 * 4, 48 * 4
		w.setImage(self.img, self.src, self.width, self.height)
		self.img_idx += 1
		self.tmp = gui.time.perf_counter()
	
	def target_me_loop(self, timestamp) :
		if (self.mouse_on_sprite()) :
			w.moveObject(self.shadow, self.x, self.y)
			w.raiseObject(self.shadow)
			w.setImage(self.shadow, cwd+'/src/res/shadow.png', self.width, self.height)
			w.showObject(self.shadow)
			self.show()
			if (w.mouse_buttons[1]) :
				return True
		else :
			w.hideObject(self.shadow)
		return False
	
	def skill_hide(self) :
		for i in self.skill :
			w.hideObject(i.img)
			w.hideObject(i.info_txt)

	def set_HP(self, HP) :
		self.HP = HP
		if (self.HP <= 0) :
			self.HP = 0
		w.resizeObject(self.HP_red, int((self.HP / self.MAXHP) * 100), 20, 1)
		print(self.HP)
	
	def set_stress(self, stress) :
		self.stress = stress
		if (self.stress > 200) :
			self.stress = 200
		w.resizeObject(self.stress_bar, int((self.stress / 200) * 100), 20, 1)
	
	def myturn(self) :
		pass

	class balloon_class :
		def __init__(self, saying, direction = 'right') :
			super().balloon = self
			self.img = w.newImage(super().x, super().y, cwd+'/src/res/balloon/balloon1_'+direction+'.png', False)
			self.make_time = gui.time.perf_counter()
	class skill_class :
		def __init__(self, name, hit, damage, possible, otherEffect, critical, crit_damage) :
			self.name = name
			self.damage = damage
			self.possible = possible
			self.otherEffect = otherEffect # [효과코드, 몇턴, 얼마데미지]
			self.critical = critical
			self.crit_damage = crit_damage
			self.hit = hit
			self.img = 0
			self.x = 0
			self.y = 0
			self.firstFlag = True
			self.info_txt = w.newText(530, 600, 180, '', 'white', anchor='nw', isVisible=False)

		def mouse_on(self) :
			if (self.x + 4 <= w.mouse_position_x <= self.x + 44 and self.y + 4 <= w.mouse_position_y <= self.y + 44) :
				return True
			else :
				return False

		def skill_loop(self, timestamp=0) :
			if (self.mouse_on()) :
				w.setImage(self.img, cwd+'/src/res/skill/'+self.name+'_on.png', 48, 48)
				if (w.mouse_buttons[1]) :
					return True
			else :
				w.setImage(self.img, cwd+'/src/res/skill/'+self.name+'_off.png', 48, 48)
			return False
		
		def display_info(self) :
			info_str = '      ' + str(self.name) + '\n\n'
			info_str += "데미지         : " + str(self.damage) + '\n'
			info_str += "범위   	       : " + str(len(self.possible)) + '\n'
			info_str += "크리티컬 확률   : " + str(self.critical) + '\n'
			info_str += "크리티컬 데미지 : " + str(self.crit_damage) + '\n'
			# if (self.otherEffect != 0) :
			# 	info_str = "효과           : " + str(self.otherEffect[1]) + '턴 동안 ' + str(self.otherEffect[2]) +' 의 데미지로 ' + str(self.otherEffect[0])
			w.setText(self.info_txt, info_str)
			w.raiseObject(self.info_txt)
			w.showObject(self.info_txt)

	class state_class : # [num] : 상태, [턴수 데미지]
		def __init__(self) :
			self.num = 1
			self.poison = []
			self.bleed = []
			self.stun = []
			self.feer = []

	class refuse_class :
		def __init__(self) :
			self.stun = 0
			self.poison = 0
			self.bleed =0
			self.feer = 0


def data_setting(src) :
	with open(src, 'r', encoding='UTF-8') as f :
		dic = dict(json.load(f))
	data_list = {}
	for i in dic :
		data_list[i] = sprite(i)
		tmp = data_list[i]
		tmp.ID = dic[i]["ID"]
		#tmp.width = dic[i]["width"]
		#tmp.height = dic[i]["height"]
		tmp.width = 48 * 4
		tmp.height = 48 * 4
		tmp.speed = dic[i]["speed"]
		#tmp.defense = dic[i]["defense"]
		tmp.miss = dic[i]["miss"]
		tmp.img_idx_num = dic[i]["img_idx_num"]
		#tmp.damage = dic[i]["damage"]
		tmp.HP = dic[i]["HP"]
		tmp.MAXHP = tmp.HP
		tmp.says = dic[i]["says"]
		for j in dic[i]["skill"] :
			a = dic[i]['skill'][j]
			tmp.skill.append(tmp.skill_class(j, a[0], a[1], a[2], a[3], a[4], a[5]))
		for j in range(0, len(tmp.skill)) :
			tmp.skill[j].x = tmp.skill_pos[j][0]
			tmp.skill[j].y = tmp.skill_pos[j][1]
			tmp.skill[j].img = w.newImage(tmp.skill[j].x, tmp.skill[j].y, cwd+'/src/res/skill/'+tmp.skill[j].name+'_off.png', 48, 48, False)
		w.moveObject(tmp.HP_red , tmp.x - 10, tmp.y + tmp.height + 20)
		w.moveObject(tmp.HP_gray, tmp.x - 10, tmp.y + tmp.height + 20)
		w.moveObject(tmp.stress_back, tmp.x - 10, tmp.y + tmp.height + 40)
		w.moveObject(tmp.stress_bar, tmp.x - 10, tmp.y + tmp.height + 40)

	return data_list

#380 515
def stage_setting() :
	data.stageone = stageOne(data.sprite_list, )

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
	data.otherEffect_name = {
		50099 : "스턴", 20099 : "중독", 30099 : "출혈", 
		70099 : "공포", 11199 : "대신 막기", 22299 : "힐", 
		33399 : "스트레스 감소", 100199 : "절망", 100299 : "편집증", 
		100399 : "정신착란", 200199 : "기사회생", 200299 : "차분한 영혼", 
		200399 : "회광반조", 999999 : "와 샌즈"
	}
	data.player_list = data_setting(cwd + '/src/json/player.json')
	data.player_list["방패"].print_info()
	data.shadow = w.newImage(0, 0, cwd + '/src/res/shadow.png', 48, 48, False)
	data.start_back = w.newImage(0, 0, cwd + '/src/res/background/start.png', window_width, window_height, False)
	data.game_status = 0 
	data.flag = False #요긴하게
	#game_intro = scene_class(cwd + '/src/res/intro/intro_logo', 21, 2)
	winsound.PlaySound(cwd + '/src/res/bgm/main_bgm.wav', winsound.SND_ASYNC)
	data.start_btn = btn_class(cwd + '/src/res/button/start_btn', 500, 450, 220, 70)
	#game_intro.scene_func(0.1)
	w.update = update

# def turn(timestamp) :
#     global turn_flag
#     if (turn_flag == False) :
#         data.sprite_list['man'].say = '아 X마려운데 화장실 없냐?'
#         data.sprite_list["man"].show()
#         data.sprite_list["woman"].show()
#         turn_flag = True

#     data.sprite_list["man"].idle_loop(timestamp)
#     data.sprite_list["woman"].idle_loop(timestamp)

data.update_firstFlag = True

def update(timestamp) :
	if (data.game_status == 0) :
		w.showObject(data.start_back)
		data.start_btn.show()
		if (data.start_btn.in_loop()) :
			data.start_btn.hide()
			data.change_update_time = gui.time.perf_counter()
			data.game_status = 1
			scene_class(cwd+'/src/res/scene/intro_scene', 11, 3, skip=True).scene_func(2)
			#data.stageone = stageOne()
	if (data.game_status == 1) :
		data.mob_list = data_setting(cwd + '/src/json/mob.json')
		data.stageone = stageOne(data.player_list, data.mob_list, cwd+'/src/res/background/stage1.png')
		data.stageone.screen_setting()
		data.game_status = 2
		w.update = data.stageone.phase


def sort_speed(char):# speed 내림차순 배열
    sorted_char = sorted(char, key=lambda x: x[1], reverse=True)
	
    return sorted_char
    
# def quick_sort(arr):
# 	if len(arr) <= 1:
# 		return arr
# 	else:
# 		pivot = arr[len(arr) // 2][1]
# 		left = [x for x in arr if x[1] < pivot]
# 		middle = [x for x in arr if x[1] == pivot]
# 		right = [x for x in arr if x[1] > pivot]
		
# 		return quick_sort(right) + middle + quick_sort(left)

# def sort_speed(char):
#     return quick_sort(char)



class stageOne:
	def __init__(self, character, stageOne_mob, src): #창과 방패, 그리고 1스테이지 몹 스프라이트를 받아서 생성된다.
		self.character = []
		for i in character :
			self.character.append(character[i])
		for i in stageOne_mob :
			self.character.append(stageOne_mob[i])
		# self.character[0] = character[0] #0번은 왼쪽에서 첫번째 자리 -- 창의 자리
		# self.character[1] = character[1] #1번은 왼쪽에서 두번째 자리 -- 방패의 자리
		# self.character[2] = stageOne_mob[0] #2번은 왼쪽에서 세번째 자리 -- 1스테이지 몹의 자리
		# self.character[3] = stageOne_mob[1] #3번은 왼쪽에서 네번째 자리 -- 1스테이지 몹의 자리
		# self.character[4] = stageOne_mob[2] #4번은 왼쪽에서 다섯번째 자리 -- 1스테이지 중간보스의 자리
		self.phaseCount = 0 #페이즈 카운터는 이것을 센다. 시작은 0이고 이를 토대로 위에 페이즈 숫자를 띄우면 된다.
		self.nowTurn = 0
		self.nowSprite = None
		self.phaseFirst = True
		self.turnFirst = True
		self.speed = []
		self.stage_img = w.newImage(0, 0, src, window_width, 500, False)
		self.pos_list = [(150, 200), (300, 200), (650, 200), (800, 200), (950, 200)]
		self.status_bar_img = w.newImage(0, 500, cwd+'/src/res/background/status_bar.png', window_width, 220, False)
		self.mouse_txt = w.newText(20, 20, 100, '',fill_color='white', anchor='nw', isVisible=True)

	def screen_setting(self) :
		w.showObject(self.stage_img)
		w.showObject(self.status_bar_img)
		for i in self.character :
			if (i.name == "None") :
				continue
			i.move(self.pos_list[i.ID][0], self.pos_list[i.ID][1])
			i.show()
			

	def sprite_animation_loop(self, timestamp) :
		for i in self.character :
			i.idle_loop(timestamp)

	def select_target(self, timestamp) :
		self.sprite_animation_loop(timestamp)
		for i in self.nowSprite.skill :
			if i.skill_loop(timestamp) :
				w.hideObject(self.selected_skill.info_txt)
				i.display_info()
				self.selected_skill = i
		for i in self.selected_skill.possible :
			if self.character[i].target_me_loop(timestamp):
				self.selected_target = self.character[i]
				self.do_turn()
				w.update = self.phase
	
	def do_turn(self):
		select = self.selected_skill
		target = self.selected_target

		if select.damage < 0: #이거는 힐 또는 대신맞기
			if select.otherEffect == HEAL:	#자 여기에서 잠깐 확인 들어가야함

				if target.collapse == DESPAIR:
					probability = random.randint(1, 100)
					if probability <= 70:
						#힐 개무시함.
						#편집증 대사 하나 나오고 뙇!#########################################################################################################
						return #########################################################################################################

				probability = random.randint(1, 100)
				if select.critical <= probability: #크리티컬이 뜨면
					target.HP -= select.crit_damage
					#크리티컬이라는 효과와 함께 힐 효과 #########################################################################################################

					if target.MAXHP < target.HP:
						target.HP = target.MAXHP
				else:
					target.HP -= select.damage

					#이건 그냥 힐 #########################################################################################################

					if target.MAXHP < target.HP:
						target.HP = target.MAXHP
				return #########################################################################################################
			

			elif select.otherEffect == DEFENSE:
				target.defender = self.nowSprite #딱 한턴만 대신 맞아준다는 소리

				#이거는 이제 방어해주는 모션 넣기 #########################################################################################################

				return #########################################################################################################


			elif select.otherEffect == STRESSHEAL: #창만 가지는 유일무의 스킬. 한턴 쉬고 자기 스트레스 힐하기
				self.nowSprite.stress -= 30


				#여기서 약간 휴식하는 모션 넣기 #########################################################################################################

				return #########################################################################################################



		if 	select.damage >= 0: #이제 주는 데미지일 때
			if self.nowSprite.name == "창":
				probability = random.randint(1, 100)
				if probability <= self.nowSprite.hit: #명중하면
					probability = random.randint(1, 100)
					if probability <= target.miss: #회피하고
					

					#여기서 회피 그림 뙇 뜨고 #########################################################################################################
					
					
						self.nowSprite.stress += 50 #굉장히 스트레스를 많이 받음(연사하지 못하게 방지책)
						return #회피했으니 이후 그 어떤 효과도 안받는다 #########################################################################################################
					
					else:
						target.HP -= select.damage

						#바로 즉사하는 모션 #########################################################################################################
						
						for k, char in enumerate(self.character):
							if target == char:
								self.character[k] = None #죽여버리는 코드 #########################################################################################################

						self.nowSprite.stress += 50 #########################################################################################################

				else:
					
					#빗나감 효과 #########################################################################################################

					self.nowSprite.stress += 50
					return #명중 안하면 빗나감이니 그것도 어떤 효과도 안받는다 #########################################################################################################
		
				


			if target.defender != None: #맞아주는 애가 있을 때...
				defended = target
				target = target.defender #### 유의
				defended.defender = None #원래 애의 defender를 이제 없애고, 대신 맞아주는 애로 타겟을 바꿈
			probability = random.randint(1, 100)
			if probability <= select.hit: #명중하면
				probability = random.randint(1, 100)
				if probability <= target.miss: #회피하고
					

					#여기서 회피 그림 뙇 뜨고 #########################################################################################################

					return #회피했으니 이후 그 어떤 효과도 안받는다 #########################################################################################################

				else:
					probability = random.randint(1, 100)
					if select.critical <= probability: #크리티컬이 뜨면
						doDamage = select.crit_damage
					else:
						doDamage = select.damage

					target.HP -= doDamage
					#때려 #########################################################################################################
			else:
				#빗나감 #########################################################################################################
				return #명중 안하면 빗나감이니 그것도 어떤 효과도 안받는다

			for status in select.otherEffect: #그리고 이제 그냥 데미지 말고 다른 추가적인 효과들이 있나 확인

				if status[0] == STUN: #스턴일 때
					#########################################################################################################
					probability = random.randint(1, 100)
					if target.refuse.stun <= probability: #스턴 저항이면 아무 일도 안일어남
						pass
					else:
						target.state.num *= 5 #아니면 스턴

						if target.collapse == LAST_DANCE: #그런데 회광반조이면 아무 일도 일어나면 안되지
							target.state.num /= 5
						

				if status[0] == POISON:
					#########################################################################################################
					probability = random.randint(1, 100)
					if target.refuse.poison <= probability:


						pass
					else:
						target.state.num *= 2

						if target.collapse == LAST_DANCE:
							target.state.num /= 2
						else:
							target.state.poison[0] = status[1]
							target.state.poison[1] = status[2]


				if status[0] == BLEED:
					#########################################################################################################
					probability = random.randint(1, 100)
					if target.refuse.bleed <= probability:

						pass
					else:
						target.state.num *= 3


						if target.collapse == LAST_DANCE:
							target.state.num /= 3
						else:
							target.state.bleed[0] = status[1]
							target.state.bleed[1] = status[2]



				if status[0] == FEAR:
					#########################################################################################################
					target.state.num *= 7

					if target.collapse == LAST_DANCE:
						target.state.num /= 7
					else:
						target.stress += status[2] #당장 스트레스를 받아(일회성인 스트레스 공격도 있을 것이기 때문에 ex) (70099, 0, 100) 이런거
						target.state.fear[0] = status[1]
						target.state.fear[1] = status[2]
					if target.stress >= 100:
						if target.collapse == None:
							target.collapse = random.choice([100199, 100199, 100199, 100299, 100299, 100399, 100399, 200199, 200299, 200399]) 
						#대사
							if self.nowSpriter.collapse == LAST_DANCE: #근데 회광반조이라면, 순식간에 피가 차야해. 그래서 MAXHP로 HP를 바꿔
								self.nowSprite.HP = self.nowSprite.MAXHP
								self.nowSprite.stress = 0
								self.nowSprite.state.num = 1
						pass
					if target.stress >= 200:
						target.stress = 200
						target.HP = 0
						for k, char in enumerate(self.character):
								if target == char:
									self.character[k] = None
									return
		return


	def phase(self, timestamp): 
		#self.phaseCount = phaseCount + 1 #페이즈카운트는 페이즈 함수가 받는 숫자인데, 재귀 형태로 실행을 할 예정이다. ex) 1페이즈 이후 2페이즈 돌입 시, phase(1)이 실행.... 이는 페이즈카운터를 2로 맞추는 효과
										#(마치 리스트마냥 0번은 1페이즈, 1번은 2페이즈....)
		#thisphase = self.phaseCount #조금 변수를 난발하는 느낌이 없잖아 있긴 함. thisphase는 페이즈 카운터랑 똑같은 숫자라는 뜻. 
		
		w.setText(self.mouse_txt, 'x : ' + str(w.mouse_position_x) +'  y : ' + str(w.mouse_position_y))
		self.sprite_animation_loop(timestamp)
		#여기에 페이즈 나타내는 전광판을 만들어야 할 텐데(지금 생각은 원이고 지름이 80이고 중심이 640, 80 이면 좋을 듯
		#페이즈가 새로고침 될 때마다 원이 눈이 감기듯 그 전부 검정 되지 말고 위 아래로 조금만 검정인 프레임 다음, 완전 검정 프레임, 그리고 다시 위 아래 조금만 검정인 프레임, 그리고 숫자 바뀐 원
		#이렇게 숫자 바뀌면 디테일적인 면에서 좀 재밌을 듯. 재생시키면 페이즈 카운터가 살아있듯이 눈 깜빡 하니까 숫자가 바뀐거니 
		#그때 쓰는 변수가 thisphase
		
		if (self.phaseFirst) :
			speed = []
			for char in self.character:
				if char == None: #뒤지면 None이 되버리기 때문에... 얘는 시체야. speed에 넣을 이유가??없다.
					continue
				else:
					speed.append([char.ID, char.speed]) #ID와 속도를 튜플로 리스트에 우겨넣음
					self.speed = sort_speed(speed) #그리고 그 튜플 리스트를 속도 빠른 순서로 후루룩 배열함. 그리고 거기서 ID만 쏙 빼서 리스트로 정리함
			self.phaseFirst = False
		
		if (self.turnFirst) :
			if (self.nowSprite != None) :
				self.nowSprite.skill_hide()
			self.nowSprite = self.character[self.speed[self.nowTurn][0]]
			print(self.nowSprite.name)
			self.nowSprite.set_HP(self.nowSprite.HP)
			self.nowSprite.set_stress(self.nowSprite.stress)
			if self.nowSprite.name != "창" and self.nowSprite.name != "방패":
				self.selected_skill = self.nowSprite.skill[0]
				self.selected_target = self.character[random.choice([0, 1])]
				self.do_turn()
				self.nowTurn += 1
				self.turnFirst = True
				return

			else:	
				for i in self.nowSprite.skill :
					w.showObject(i.img)
					w.raiseObject(i.img)
				self.turnFirst = False
				#self.turn(self.speed[self.nowTurn])
				#print(self.nowSprite.name)
			
		
		for i in self.nowSprite.skill :
			if i.skill_loop(timestamp) :
				i.display_info()
				self.selected_skill = i
				w.update = self.select_target
				self.turnFirst = True
				self.nowTurn += 1





w.initialize = initialize
w.update = update

w.start()