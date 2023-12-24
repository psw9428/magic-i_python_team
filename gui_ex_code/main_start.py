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


sans_first = True
sans_status = 0
sans = False
tmptmp = 0
def sans_loop(timestamp) :
	global sans
	if (sans) :
		return
	global sans_status
	global tmptmp
	if (sans_status == 3) :
		if (w.keys['s']) :
			print('s')
			print('sans!!!!')
			sans_status = 4
			sans = True
			winsound.PlaySound(cwd+'/src/res/bgm/sans.wav', winsound.SND_ASYNC + winsound.SND_LOOP)
	elif (sans_status == 2) :
		if (w.keys['n']) :
			print('n')
			sans_status = 3
			tmptmp = gui.time.perf_counter()
	elif (sans_status == 1) :
		if (w.keys['a']) :
			print('a')
			sans_status = 2
			tmptmp = gui.time.perf_counter()
	elif (w.keys['s']) :
		print('s')
		sans_status = 1
		tmptmp = gui.time.perf_counter()
	if (tmptmp + 1 < timestamp) :
		sans_status = 0
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
		w.raiseObject(self.img)
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
		self.says = None
		self.state = self.state_class()
		self.collapse = 0
		self.defender = 0
		self.refuse = self.refuse_class()
		self.skill = []
		self.onmouse = False
		self.skill_pos = [(400, 515), (480, 515), (560, 515), (640, 515)]
		self.info_txt = w.newText(800, 515, 500, '', 'white', 'nw', False)
		self.HP_gray = w.newRectangle(0, 0, 100, 20, 'gray', 1, 'white', False)
		self.HP_red = w.newRectangle(0, 0, 100, 20, 'red', 1, 'white', False)
		self.stress_back = w.newRectangle(0, 0, 100, 20, 'black', 1, 'white', False)
		self.stress_bar = w.newRectangle(0, 0, 0, 20, 'white', 1, 'white', False)
		self.arrow_img = w.newImage(0, 0, cwd + '/src/res/arrow.png', 96, 96, False)
		self.sans_img = w.newImage(0, 0, cwd+'/src/res/sans/sayain1.png', 192, 192, False)
		self.hit_animation = self.hit_class(self)
		self.balloon = None

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

	def display_info(self, x = 800, y = 515) :
		info_str = '이름 : ' + self.name +'\n\n'
		info_str += '체력 : ' + str(self.HP) + '/' + str(self.MAXHP) + '\n'
		info_str += '스트레스 : ' + str(self.stress) + '/200\n'
		info_str += '회피율 : ' + str(self.miss) + '\n'
		info_str += '\n'
		if self.state.num % POISON == 0 :
			info_str += '독 : '+str(self.state.poison[0])+'턴 동안 '+str(self.state.poison[1])+'의 데미지\n'
		if self.state.num % BLEED == 0 :
			info_str += '출혈 : '+str(self.state.bleed[0])+'턴 동안 '+str(self.state.bleed[1])+'의 데미지\n'
		if self.state.num % STUN == 0 :
			info_str += '기절 : 한턴 동안 행동불가\n'
		if self.state.num % FEAR == 0 :
			info_str += '공포'

		w.moveObject(self.info_txt, x, y)
		w.setText(self.info_txt, info_str)
		w.raiseObject(self.info_txt)
		w.showObject(self.info_txt)

	def show_arrow(self) :
		w.moveObject(self.arrow_img, self.x + 10, self.y - 80)
		w.raiseObject(self.arrow_img)
		w.showObject(self.arrow_img)

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
		w.hideObject(self.info_txt)
		w.hideObject(self.img)
		w.hideObject(self.HP_gray)
		w.hideObject(self.HP_red)
		w.hideObject(self.stress_back)
		w.hideObject(self.stress_bar)
		w.hideObject(self.sans_img)
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
		if (self.tmp + 0.2 > timestamp or self.name == "Dead") :
			return
		self.src = cwd + '/src/res/sprite/' + self.name + str(self.img_idx + 1) + '.png'
		self.width, self.height = 48 * 4, 48 * 4
		w.setImage(self.img, self.src, self.width, self.height)
		if (sans and (self.name == "창" or self.name == "방패")) :
			w.moveObject(self.sans_img, self.x - 20, self.y + 10)
			w.showObject(self.sans_img)
			w.setImage(self.sans_img, cwd+'/src/res/sans/say'+str(self.img_idx+1)+'.png', 192, 192)
			w.raiseObject(self.sans_img)
		self.img_idx += 1
		if (self.img_idx % self.img_idx_num == 0) :
			self.img_idx = 0
		self.tmp = gui.time.perf_counter()
	
	def target_me_loop(self, timestamp) :
		if (self.mouse_on_sprite()) :
			w.moveObject(self.shadow, self.x, self.y)
			w.raiseObject(self.shadow)
			w.setImage(self.shadow, cwd+'/src/res/shadow.png', self.width, self.height)
			w.showObject(self.shadow)
			self.display_info()
			self.show()
			if (w.mouse_buttons[1]) :
				w.hideObject(self.shadow)
				return True
		else :
			w.hideObject(self.info_txt)
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
	
	def set_stress(self, stress) :
		self.stress = stress
		if (self.stress > 200) :
			self.stress = 200
		w.resizeObject(self.stress_bar, int((self.stress / 200) * 100), 20, 1)

	class balloon_class :
		def __init__(self, sprite, say, duration) :
			self.img = w.newImage(0, 0, cwd+'/src/res/balloon/balloon1_right.png', 192, 96, False)
			self.sprite = sprite
			self.say_str = say
			self.txt = w.newText(0, 0, 150, '', 'white', 'nw', False)
			self.sayFirst = True
			self.tmp = 0
			self.duration = duration
		
		def say_loop(self, timestamp) :
			if (self.sayFirst) :
				w.moveObject(self.img, self.sprite.x, self.sprite.y-56)
				w.raiseObject(self.img)
				w.setText(self.txt, self.say_str)
				w.moveObject(self.txt, self.sprite.x + 20, self.sprite.y-36)
				w.raiseObject(self.txt)
				w.showObject(self.img)
				w.showObject(self.txt)
				self.sayFirst = False
				self.tmp = gui.time.perf_counter()
				return
			elif self.tmp + self.duration > timestamp :
				return
			w.hideObject(self.img)
			w.hideObject(self.txt)
			self.sayFirst = True
			self.sprite.balloon = None

	class skill_class :
		def __init__(self, name, damage, hit, possible, otherEffect, critical, crit_damage) :
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
			info_str += "범위   	     : " + str(len(self.possible)) + '\n'
			info_str += "명중률          : " + str(self.hit) + '\n'
			info_str += "크리티컬 확률   : " + str(self.critical) + '\n'
			info_str += "크리티컬 데미지 : " + str(self.crit_damage) + '\n'
			# if (self.otherEffect != 0) :
			# 	info_str = "효과           : " + str(self.otherEffect[1]) + '턴 동안 ' + str(self.otherEffect[2]) +' 의 데미지로 ' + str(self.otherEffect[0])
			w.setText(self.info_txt, info_str)
			w.raiseObject(self.info_txt)
			w.showObject(self.info_txt)
		
	class hit_class :
		def __init__(self, sprite) :
			self.if_hit = False
			self.if_critical = False
			self.if_heal = False
			self.if_stress_heal = False
			self.if_miss = False
			self.value = 0
			self.num1_img = w.newImage(0, 0, cwd + '/src/res/number/green0.png', 96, 96, False)
			self.num2_img = w.newImage(0, 0, cwd + '/src/res/number/red0.png', 96, 96, False)
			self.critical_img = w.newImage(0, 0, cwd + '/src/res/critical.png', 96, 96, False)
			self.miss_img = w.newImage(0, 0, cwd+'/src/res/miss.png', 96, 96, False)
			self.sprite = sprite
			self.tmp = 0
			self.cnt = 0
		
		def loop(self, timestamp) :
			if (self.if_miss) :
				self.miss_loop(timestamp)
			elif (self.if_heal) :
				self.heal_loop(timestamp)
			elif (self.if_hit) :
				self.hit_loop(timestamp)
			else :
				return
			if (self.max_cnt == self.cnt) :
				self.if_hit = False
				self.if_critical = False
				self.if_stress_heal = False
				self.if_heal = False
				self.if_miss = False
				w.hideObject(self.num1_img)
				w.hideObject(self.num2_img)
				w.hideObject(self.critical_img)
				w.hideObject(self.miss_img)
				self.value = 0
				self.cnt = 0 
				self.max_cnt = 0

		def miss_loop(self, timestamp) :
			if (self.cnt == 0) :
				self.max_cnt = 20
				w.moveObject(self.miss_img, self.sprite.x-20, self.sprite.y)
				w.raiseObject(self.miss_img)
				w.showObject(self.miss_img)
			if (self.tmp + 0.1 > timestamp) :
				return
			x, y = w.getPosition(self.miss_img)
			w.moveObject(self.miss_img, x, y-2)
			self.cnt += 1
			self.tmp = gui.time.perf_counter()

		def hit_loop(self, timestamp) :
			if (self.cnt == 0) :
				self.max_cnt = 20
				num1 = int(self.value // 10)
				num2 = int(self.value % 10)
				if (num1 == 0) :
					w.setImage(self.num1_img, cwd+'/src/res/number/none.png', 96, 96)
				else :
					w.setImage(self.num1_img, cwd+'/src/res/number/red'+str(num1)+'.png', 96, 96)
				w.setImage(self.num2_img, cwd+'/src/res/number/red'+str(num2)+'.png', 96, 96)
				if (self.if_critical) :
					w.setImage(self.critical_img, cwd+'/src/res/critical.png', 96, 96)
					if (num1 == 0) :
						w.moveObject(self.critical_img, self.sprite.x+40, self.sprite.y-10)
					else :
						w.moveObject(self.critical_img, self.sprite.x, self.sprite.y-10)
					w.raiseObject(self.critical_img)
					w.showObject(self.critical_img)
				w.moveObject(self.num1_img, self.sprite.x-40, self.sprite.y-10)
				w.moveObject(self.num2_img, self.sprite.x+40, self.sprite.y-10)
				w.showObject(self.num1_img)
				w.showObject(self.num2_img)
				w.raiseObject(self.num1_img)
				w.raiseObject(self.num2_img)
			if (self.tmp + 0.1 > timestamp) :
				return
			num1_x, num1_y = w.getPosition(self.num1_img)
			num2_x, num2_y = w.getPosition(self.num2_img)
			crit_x, crit_y = w.getPosition(self.critical_img)
			w.moveObject(self.num1_img, num1_x, num1_y+1)
			w.moveObject(self.num2_img, num2_x, num2_y+1)
			w.moveObject(self.critical_img, crit_x, crit_y+1)
			self.cnt += 1
			self.tmp = gui.time.perf_counter()

		def heal_loop(self, timestamp) :
			if (self.cnt == 0) :
				self.max_cnt = 20
				num1 = int(self.value // 10)
				num2 = int(self.value % 10)
				if (num1 == 0) :
					w.setImage(self.num1_img, cwd+'/src/res/number/none.png', 96, 96)
				else :
					w.setImage(self.num1_img, cwd+'/src/res/number/green'+str(num1)+'.png', 96, 96)
				w.setImage(self.num2_img, cwd+'/src/res/number/green'+str(num2)+'.png', 96, 96)
				if (self.if_critical) :
					w.setImage(self.critical_img, cwd+'/src/res/critical.png', 96, 96)
					if (num1 == 0) :
						w.moveObject(self.critical_img, self.sprite.x+40, self.sprite.y)
					else :
						w.moveObject(self.critical_img, self.sprite.x, self.sprite.y)
					w.raiseObject(self.critical_img)
					w.showObject(self.critical_img)
				w.moveObject(self.num1_img, self.sprite.x-40, self.sprite.y)
				w.moveObject(self.num2_img, self.sprite.x+40, self.sprite.y)
				w.showObject(self.num1_img)
				w.showObject(self.num2_img)
				w.raiseObject(self.num1_img)
				w.raiseObject(self.num2_img)
			if (self.tmp + 0.1 > timestamp) :
				return
			num1_x, num1_y = w.getPosition(self.num1_img)
			num2_x, num2_y = w.getPosition(self.num2_img)
			crit_x, crit_y = w.getPosition(self.critical_img)
			w.moveObject(self.num1_img, num1_x, num1_y-1)
			w.moveObject(self.num2_img, num2_x, num2_y-1)
			w.moveObject(self.critical_img, crit_x, crit_y-1)
			self.cnt += 1
			self.tmp = gui.time.perf_counter()


	class state_class : # [num] : 상태, [턴수 데미지]
		def __init__(self) :
			self.num = 1
			self.poison = []
			self.bleed = []
			self.stun = 0
			self.fear = []

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
		tmp.defender = dic[i]["defender"]
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
	game_intro = scene_class(cwd + '/src/res/intro/intro_logo', 21, 2)
	winsound.PlaySound(cwd + '/src/res/bgm/main_bgm.wav', winsound.SND_ASYNC + winsound.SND_LOOP)
	data.start_btn = btn_class(cwd + '/src/res/button/start_btn', 500, 450, 220, 70)
	game_intro.scene_func(0.1)
	#w.update = update

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
			scene_class(cwd+'/src/res/scene/intro_scene', 11, 2, skip=True).scene_func(2)
			#data.stageone = stageOne()
	elif (data.game_status == 1) :
		data.mob_list = data_setting(cwd + '/src/json/mob.json')
		data.stageone = stageOne(data.player_list, data.mob_list, cwd+'/src/res/background/stage1.png')
		data.stageone.screen_setting()
		data.game_status = 2
		w.update = data.stageone.phase
	
	elif (data.game_status == 2) :
		scene_class(cwd+'/src/res/ending/win', 1, 5).scene_func(3)
	elif (data.game_status == 3) :
		scene_class(cwd+'/src/res/ending/loose', 1, 5).scene_func(3)	


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
		self.nowPhase = 0
		self.nowSprite = None
		self.phaseFirst = True
		self.turnFirst = True
		self.speed = []
		self.stage_img = w.newImage(0, 0, src, window_width, 500, False)
		self.pos_list = [(150, 200), (300, 200), (650, 200), (850, 200), (1050, 200)]
		self.status_bar_img = w.newImage(0, 500, cwd+'/src/res/background/status_bar.png', window_width, 220, False)
		self.mouse_txt = w.newText(20, 20, 100, '',fill_color='white', anchor='nw', isVisible=True)
		self.log_txt = w.newText(1000, 500, 200, '', 'white', 'nw', False)
		self.log_str = ''
		self.mob_time = 0

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
			if (i == None) :
				continue
			i.idle_loop(timestamp)

	def log_print(self) :
		w.setText(self.log_txt, self.log_str)
		w.raiseObject(self.log_txt)
		w.showObject(self.log_txt)
		self.log_str = ''
	
	def do_check(self):
		if self.nowSprite.name == "Dead":
			return

		if self.nowSprite.state.num % 2 == 0: #중독되면 state.num의 정수가 기본 1이었다가 2를 곱해. 즉, 지금 2로 나누었는데, 나머지가 0이면, 얘는 2를 곱했다는거지. 그러니까. 중독이라는거야.
			self.nowSprite.state.poison[0] -= 1 #state에는 poison튜플이 있는데 이건 (남은 쳐맞는 턴수, 쳐맞을 때 데미지)의 튜플이지. 턴수 하나 줄이고
			self.nowSprite.HP -= self.nowSprite.state.poison[1] #데미지 넣고 #################################################################
			self.nowSprite.hit_animation.if_hit = True
			self.nowSprite.hit_animation.value = self.nowSprite.state.poison[1]
			if self.nowSprite.HP <= 0: #데미지 받았는데 죽었네? 수고링
				if self.nowSprite.name == "방패": #그런데 죽은게 방패였네
					self.nowSprite.HP = self.nowSprite.MAXHP #그럼 부활 ######################################################
				else:
					self.nowSprite.name = "Dead" ##################################################################
					self.speed.remove([self.nowSprite.ID, self.nowSprite.speed])
					for fix in self.character:
						for skill in fix.skill:
							skill.possible.remove(self.nowSprite.ID) ##########################################################
					return


					#사망 대사 뽷 나와주고


				return #그리고 이 turn함수를 빠져 나와야함
			
				#여기서 return을 쓰는게 맞는지 모르겠네?


			if self.nowSprite.state.posion[0] == 0: #다 맞았다. 지금을 끝으로 더이상 중독이 아니야
				self.nowSprite.state.poison[1] = 0 #데미지도 0으로 만들고
				self.nowSprite.state.num  /=  2 #이제 2로 나눠줘


		if self.nowSprite.state.num % 3 == 0: #중독이랑 같은 메커니즘(2, 3, 5, 7 얘네가 소수라 서로 겹칠 일도 없고, 수학적으로 완벽한 설정법인듯 하하)
			self.nowSprite.state.bleed[0] -= 1 #이것도 마찬가지
			self.nowSprite.hit_animation.if_hit = True
			self.nowSprite.hit_animation.value += self.nowSprite.state.bleed[1]
			self.nowSprite.HP -= self.nowSprite.state.bleed[1] ##############################################################################
			if self.nowSprite.HP <= 0: #데미지 받았는데 죽었네? 수고링
				if self.nowSprite.name == "방패": #그런데 죽은게 방패였네
					self.nowSprite.HP = self.nowSprite.MAXHP #그럼 부활 ######################################################
				else:
					self.nowSprite.name = "Dead" ##################################################################
					self.speed.remove([self.nowSprite.ID, self.nowSprite.speed])
					for fix in self.character:
						for skill in fix.skill:
							skill.possible.remove(self.nowSprite.ID) ##########################################################
					return


					#사망 대사 뽷 나와주고 ##########################################


				return #그리고 이 turn함수를 빠져 나와야함
			
				#여기서 return을 쓰는게 맞는지 모르겠네?
			if self.nowSprite.state.bleed[0] == 0:
				self.nowSprite.state.bleed[1] = 0
				self.nowSprite.state.num  /= 3

		# if self.nowSprite.state.num % 7 == 0: #얘가 스트레스인데
		# 	#self.nowSprite.state.fear[0] -= 1
		# 	#self.nowSprite.stress += self.nowSprite.state.fear[1] #데미지랑 다르게 빼는게 아니라 더해야 함
		# 	if self.nowSprite.stress >= 100: #이제 붕괴인데 원래 붕괴인 얘였으면 뭔가 달라지면 안되니까
		# 		if self.nowSprite.collapse == None: #원래 붕괴였니? 물어보고
		# 			self.nowSprite.collapse = random.choice([100199, 100199, 100199, 100299, 100299, 100399, 100399, 200199, 200299, 200399]) #붕괴 아니면 요롷게(70프로 확률 미침, 30프로 각성)
		# 			if self.nowSprite.collapse == LAST_DANCE: #근데 회광반조이라면, 순식간에 피가 차야해. 그래서 MAXHP로 HP를 바꿔
		# 				self.nowSprite.HP = self.nowSprite.MAXHP
		# 				self.nowSprite.stress = 0
		# 				self.nowSprite.state.num = 1
		# 		pass
		# 	if self.nowSprite.stress >= 200: #그런데 스트레스가 너무 쌓였네. 200이 되어버렸네. 심장마비로 죽어야겠지?
		# 		if self.nowSprite.name == "방패": #그런데 죽은게 방패였네
		# 			self.nowSprite.HP = self.nowSprite.MAXHP #그럼 부활 ######################################################
		# 			self.nowSprite.stress -= 20

		# 		else:
		# 			self.nowSprite.name = "Dead" ##################################################################
		# 			self.speed.remove([self.nowSprite.ID, self.nowSprite.speed])
		# 			for fix in self.character:
		# 				for skill in fix.skill:
		# 					skill.possible.remove(self.nowSprite.ID) ##########################################################
		# 			return


		# 			#사망 대사 뽷 나와주고
		# 		return #그리고 이 turn함수를 빠져 나와야함
			
		# 		#여기서 return을 쓰는게 맞는지 모르겠네?
			
		# 	if self.nowSprite.fear[0] == 0:
		# 		self.nowSprite.state.num /= 7
			

		# 	#이쯤에서 알아보는, collapse에 뭐가 있나
		# 	#collapse에는 붕괴코드가 있음. 끝

		if self.nowSprite.state.num % 5 == 0: #이건 그냥 스턴.....
			self.nowSprite.state.num /= 5 #바로 스턴 풀고
			return #턴 끝
		
		match = self.nowSprite.collapse #데미지 정산은 끝났고, 턴마다 미치거나 각성한 애들이 뭐라뭐라 하는 부분!!
		if match == 100199: #절망일 경우
			probability = random.randint(1, 100) #그리고 70프로 확률로 헛소리 하면서 턴 넘기기
			if probability <= 70: #딱 70프로에 들어왔다면
				#안해먹어 대사 #예를 들어 이제 더이상은 무리야... 이런거
				return #턴 끝 ########################################################턴 넘기기라고 위에 뜨면 좋을 듯
		elif match == 100299:
			pass
		elif match == 100399: #이건 정신착란인데
			if self.nowSprite.name == "방패": #방패라면
				probability = random.randint(1, 100)
				if probability <= 50: #50프로 확률로
					#안해먹어 대사 #턴을 넘겨버리는거지
					return
				else:
					target = random.randint(0, 4) #턴을 넘기는게 아니라면 자신을 포함 
					if self.character[target].name != "Dead": #아 근데 살아있는 대상에게만
						self.character[target].HP -= 5 #5만큼의 주먹질을 하고

						if target.HP <= 0: #근데 때렸는데 죽었네
							if target.name == "방패": #그런데 죽은게 방패였네
								target.HP = target.MAXHP #그럼 부활
							else:
								target.name = "Dead" ##################################################################
								self.speed.remove([target.ID, target.speed])
								for fix in self.character:
									for skill in fix.skill:
										skill.possible.remove(target.ID) ##########################################################
								return



						else: #그게 아니라면 그냥 턴 넘기기 #############################################
						#헛것을 보는 대사
							return

			elif self.nowSprite.name == "창": #근데 창이라면?
				probability = random.randint(1, 100)
				if probability <= 60: #60프로의 확률로
					self.nowSprite.state.num *= 5 #스스로에게 스턴을 걸어버리는거지
					#비명 지르기
					return #그리고 턴 끝내버리기
			elif match == 200199:
				#기사회생
				if self.nowSprite.name == "창":
					other = 1
				elif self.nowSprite.name == "방패":
					other = 0
				if self.character[other].name != "Dead": #안죽었다면
					self.nowSprite.speed += 2 
					self.character[other].speed += 2 #둘다 속도가 2 빨라짐
					self.nowSprite.HP += 5
					if self.nowSprite.HP > self.nowSprite.MAXHP:
						self.nowSprite.HP = self.nowSprite.MAXHP #그리고 자기 피도 5 채움

				else: #나머지 팀원 죽었어 ㅠㅠ
					self.nowSprite.speed += 2 #혼자만 빨라지고
					self.nowSprite.HP += 5 #혼자만 체력 회복
					if self.nowSprite.HP > self.nowSprite.MAXHP:
						self.nowSprite.HP = self.nowSprite.MAXHP #그리고 자기 피도 5 채움
				pass
			elif match == 200299:
				if self.nowSprite.name == "창":
					other = 1
				elif self.nowSprite.name == "방패":
					other = 0
				if self.character[other].name != "Dead":
					self.nowSprite.stress -= 15
					self.character[other].stress -= 15
				else:
					self.nowSprite.stress -= 15
				#할 수 있어 대사
				
			elif match == 200399:
				#회광반조
				self.nowSprite.HP  -= self.nowSprite.MAXHP / 4 #4턴만 살아있는 회광반조. 대신 그동안 같은 팀원 무적.
				if self.nowSprite.HP <= 0: #근데 때렸는데 죽었네
							if self.nowSprite.name == "방패": #그런데 죽은게 방패였네
								self.nowSprite.HP = self.nowSprite.MAXHP #그럼 부활
							else:
								self.now.name = "Dead" ##################################################################
								self.speed.remove([self.nowSprite.ID, self.nowSprite.speed])
								for fix in self.character:
									for skill in fix.skill:
										skill.possible.remove(self.nowSprite.ID) ##########################################################
								return
			if sans:
				self.character[0].skill[0].hit = 100
				self.character[0].stress = 0
				self.character[0].miss = 100
				self.character[1].miss = 100
				###
				for i in self.character[2:] :
					if (i.name == "Dead") :
						continue
					i.miss = 0

	def do_turn(self):
		if self.nowSprite.name == "Dead":
			return
		select = self.selected_skill
		target = self.selected_target

		print(self.selected_skill.name + ' -> ' + self.selected_target.name)
		self.log_str += '\n\n' + self.selected_skill.name + ' -> ' + self.selected_target.name + '\n'
		if select.damage < 0: #이거는 힐 또는 대신맞기
			if select.otherEffect == HEAL:	#자 여기에서 잠깐 확인 들어가야함

				if target.collapse == DESPAIR:
					probability = random.randint(1, 100)
					if probability <= 70:
						#힐 개무시함.
						#편집증 대사 하나 나오고 뙇!#########################################################################################################
						return #########################################################################################################

				probability = random.randint(1, 100)
				self.selected_target.hit_animation.if_heal = True
				if select.critical <= probability: #크리티컬이 뜨면
					self.selected_target.hit_animation.if_critical = True
					target.HP -= select.crit_damage
					self.selected_target.hit_animation.value = select.crit_damage
					#크리티컬이라는 효과와 함께 힐 효과 #########################################################################################################

					if target.MAXHP < target.HP:
						target.HP = target.MAXHP
				else:
					self.selected_target.hit_animation.value = select.damage
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
				print('신의 권능 발동')
				self.log_str += '신의 권능 발동\n'
				probability = random.randint(1, 100)
				if probability <= self.selected_skill.hit: #명중하면
					self.log_str += '명중'
					print('명중', end='')
					probability = random.randint(1, 100)
					if probability <= target.miss: #회피하고
						self.log_str += '했으나 회피\n'
						print('했으나 회피')
						self.selected_target.hit_animation.if_miss =True

					#여기서 회피 그림 뙇 뜨고 #########################################################################################################
					
					
						self.nowSprite.stress += 50 #굉장히 스트레스를 많이 받음(연사하지 못하게 방지책)
						if self.nowSprite.stress >= 100: #이제 붕괴인데 원래 붕괴인 얘였으면 뭔가 달라지면 안되니까
							if self.nowSprite.collapse == None: #원래 붕괴였니? 물어보고
								self.nowSprite.collapse = random.choice([100199, 100199, 100199, 100299, 100299, 100399, 100399, 200199, 200299, 200399]) #붕괴 아니면 요롷게(70프로 확률 미침, 30프로 각성)
							if self.nowSprite.collapse == LAST_DANCE: #근데 회광반조이라면, 순식간에 피가 차야해. 그래서 MAXHP로 HP를 바꿔
								self.nowSprite.HP = self.nowSprite.MAXHP
								self.nowSprite.stress = 0
								self.nowSprite.state.num = 1
						if self.nowSprite.stress >= 200: #그런데 스트레스가 너무 쌓였네. 200이 되어버렸네. 심장마비로 죽어야겠지?
							if self.nowSprite.name == "방패": #그런데 죽은게 방패였네
								self.nowSprite.HP = self.nowSprite.MAXHP #그럼 부활 ######################################################
								self.nowSprite.stress -= 20

							else:
								self.nowSprite.name = "Dead" ##################################################################
								self.speed.remove([self.nowSprite.ID, self.nowSprite.speed])
								for fix in self.character:
									for skill in fix.skill:
										try:
											skill.possible.remove(self.nowSprite.ID) ##########################################################
										except:
											continue
								return

								#사망 대사 뽷 나와주고
						return #회피했으니 이후 그 어떤 효과도 안받는다 #########################################################################################################
					
					else:
						self.log_str += '\n'
						print('')
						target.HP -= select.damage
						self.selected_target.hit_animation.value = 99
						self.selected_target.hit_animation.if_hit = True
						self.selected_target.hit_animation.if_critical = True
						#바로 즉사하는 모션 #########################################################################################################

						self.nowSprite.stress += 50 #########################################################################################################
						if self.nowSprite.stress >= 100: #이제 붕괴인데 원래 붕괴인 얘였으면 뭔가 달라지면 안되니까
							if self.nowSprite.collapse == None: #원래 붕괴였니? 물어보고
								self.nowSprite.collapse = random.choice([100199, 100199, 100199, 100299, 100299, 100399, 100399, 200199, 200299, 200399]) #붕괴 아니면 요롷게(70프로 확률 미침, 30프로 각성)
							if self.nowSprite.collapse == LAST_DANCE: #근데 회광반조이라면, 순식간에 피가 차야해. 그래서 MAXHP로 HP를 바꿔
								self.nowSprite.HP = self.nowSprite.MAXHP
								self.nowSprite.stress = 0
								self.nowSprite.state.num = 1
						if self.nowSprite.stress >= 200: #그런데 스트레스가 너무 쌓였네. 200이 되어버렸네. 심장마비로 죽어야겠지?
							if self.nowSprite.name == "방패": #그런데 죽은게 방패였네
								self.nowSprite.HP = self.nowSprite.MAXHP #그럼 부활 ######################################################
								self.nowSprite.stress -= 20

							else:
								self.nowSprite.name = "Dead" ##################################################################
								self.speed.remove([self.nowSprite.ID, self.nowSprite.speed])
								for fix in self.character:
									for skill in fix.skill:
										skill.possible.remove(self.nowSprite.ID) ##########################################################
								return

								#사망 대사 뽷 나와주고
						return
				else:
					self.log_str += '빗나감\n'
					self.selected_target.hit_animation.if_miss = True
					print('빗나감')
					#빗나감 효과 #########################################################################################################

					self.nowSprite.stress += 50
					return #명중 안하면 빗나감이니 그것도 어떤 효과도 안받는다 #########################################################################################################				


			if target.defender != None: #맞아주는 애가 있을 때...
				self.log_str += target.defender.name + '가 대신 맞아줌\n'
				print(target.defender.name + '가 대신 맞아줌')
				defended = target
				target = target.defender #### 유의
				defended.defender = None #원래 애의 defender를 이제 없애고, 대신 맞아주는 애로 타겟을 바꿈
			probability = random.randint(1, 100)
			if probability <= select.hit: #명중하면
				self.log_str += select.name + '명중'
				print(select.name + '명중', end='')
				probability = random.randint(1, 100)
				if probability <= target.miss: #회피하고
					print('했으나 회피')
					self.log_str += '했으나 회피\n'
					target.hit_animation.if_miss = True
					#여기서 회피 그림 뙇 뜨고 #########################################################################################################
					return #회피했으니 이후 그 어떤 효과도 안받는다 #########################################################################################################
				else:
					target.hit_animation.if_hit = True
					probability = random.randint(1, 100)
					if select.critical <= probability: #크리티컬이 뜨면
						target.hit_animation.if_critical = True
						print(select.name + ' 크리티컬!')
						self.log_str += '크리티컬!\n'
						doDamage = select.crit_damage
					else:
						print()
						doDamage = select.damage

					print(target.name + '에게 ' + str(doDamage) +'피해를 입힘')
					self.log_str += target.name + '에게 ' + str(doDamage) +'피해를 입힘\n'
					target.hit_animation.value = doDamage
					target.HP -= doDamage
					#때려 #########################################################################################################
					if target.HP <= 0: #데미지 받았는데 죽었네? 수고링
						if target.name == "방패": #그런데 죽은게 방패였네
							target.HP = target.MAXHP #그럼 부활 ######################################################
						else:
							target.name = "Dead" ##################################################################
							self.speed.remove([target.ID, target.speed])
							for fix in self.character:
								for skill in fix.skill:
									try :
										skill.possible.remove(target.ID) ##########################################################
									except :
										continue
						return

					#사망 대사 뽷 나와주고
			else:
				print(select.name + '빗나감')
				self.log_str += '빗나감'
				target.hit_animation.if_miss = True
				#빗나감 #########################################################################################################
				return #명중 안하면 빗나감이니 그것도 어떤 효과도 안받는다

			if (select.otherEffect == None) :
				return

			for status in select.otherEffect: #그리고 이제 그냥 데미지 말고 다른 추가적인 효과들이 있나 확인

				if status[0] == STUN: #스턴일 때
					#########################################################################################################
					probability = random.randint(1, 100)
					if target.refuse.stun <= probability: #스턴 저항이면 아무 일도 안일어남
						pass
					else:
						if target.state.num % 5 == 0:
							pass
						else:
							target.state.num *= 5

						if target.collapse == LAST_DANCE: #그런데 회광반조이면 아무 일도 일어나면 안되지
							if target.state.num % 5 == 0:
								target.state.num /= 5
						

				if status[0] == POISON:
					#########################################################################################################
					probability = random.randint(1, 100)
					if target.refuse.poison <= probability:

						pass
					else:
						if target.state.num % 2 == 0:
							pass
						else:
							target.state.num *= 2

						if target.collapse == LAST_DANCE:
							if target.state.num % 2 == 0:
								target.state.num /= 2
						else:
							target.state.poison[0] = status[1]
							target.state.poison[1] = status[2]


				if status[0] == BLEED:
					probability = random.randint(1, 100)
					if target.refuse.bleed <= probability:

						pass
					else:
						if target.state.num % 3 == 0:
							pass
						else:
							target.state.num *= 3


							if target.collapse == LAST_DANCE:
								if target.state.num % 3 == 0:
									target.state.num /= 3
							else:
								target.state.bleed[0] = status[1]
								target.state.bleed[1] = status[2]


				if status[0] == FEAR:
					if target.state.num % 7 == 0:
						pass
					else:
						target.state.num *= 7

					if target.collapse == LAST_DANCE:
						if target.state.num % 7 == 0:
							target.state.num /= 7
					else:
						target.stress += status[2] #당장 스트레스를 받아(일회성인 스트레스 공격도 있을 것이기 때문에 ex) (70099, 0, 100) 이런거
						#target.state.fear[0] = status[1]
						#target.state.fear[1] = status[2]
					if target.stress >= 100:
						if target.collapse == None:
							target.collapse = random.choice([100199, 100199, 100199, 100299, 100299, 100399, 100399, 200199, 200299, 200399]) 
						#대사
							if self.nowSpriter.collapse == LAST_DANCE: #근데 회광반조이라면, 순식간에 피가 차야해. 그래서 MAXHP로 HP를 바꿔
								self.nowSprite.HP = self.nowSprite.MAXHP
								self.nowSprite.stress = 0
								self.nowSprite.state.num = 1
						pass
					if target.stress >= 200: #그런데 스트레스가 너무 쌓였네. 200이 되어버렸네. 심장마비로 죽어야겠지?
						if target.name == "방패": #그런데 죽은게 방패였네
							target.HP = target.MAXHP #그럼 부활 ######################################################
							self.nowSprite.stress -= 20

						else:
							self.character[k].name = "Dead" ##################################################################
							self.speed.remove([target.ID, target.speed])
							for fix in self.character:
								for skill in fix.skill:
									skill.possible.remove(target.ID) ##########################################################
							return


							#사망 대사 뽷 나와주고
						return #그리고 이 turn함수를 빠져 나와야함

		return
	
	def available_num(self) :
		tmp = 0
		for i in self.character :
			if i != None :
				tmp += 1
		return tmp

	def select_target(self, timestamp) :
		sans_loop(timestamp)
		self.sprite_animation_loop(timestamp)
		for i in self.nowSprite.skill :
			if i.skill_loop(timestamp) :
				w.hideObject(self.selected_skill.info_txt)
				i.display_info()
				self.selected_skill = i
		for i in self.selected_skill.possible :
			if self.character[i].name == "Dead":
				continue
			if self.character[i].target_me_loop(timestamp):
				self.selected_target = self.character[i]
				self.do_turn()
				self.log_print()
				self.nowSprite.set_HP(self.nowSprite.HP)
				self.nowSprite.set_stress(self.nowSprite.stress)
				self.mob_time = gui.time.perf_counter()
				if (self.selected_target.HP <= 0) :
					self.selected_target.balloon = self.selected_target.balloon_class(self.selected_target, random.choice(self.selected_target.says["death"]), 2)
					self.character[self.selected_target.ID].name = "Dead"
					w.setImage(self.selected_target.img, cwd+'/src/res/sprite/Dead.png', 192, 192)
					w.hideObject(self.selected_target.info_txt)
					#self.selected_target.hide()
				w.hideObject(self.nowSprite.arrow_img)
				self.set_bar()
				w.update = self.phase
	
	def hit_animation_loop(self, timestamp) :
		for i in self.character :
			if (i == None) :
				continue
			i.hit_animation.loop(timestamp)
		
		
	def set_bar(self) :
		for i in self.character :
			if (i.name == "Dead") :
				continue
			i.set_HP(i.HP)
			i.set_stress(i.stress)

	def phase(self, timestamp): 
		#self.phaseCount = phaseCount + 1 #페이즈카운트는 페이즈 함수가 받는 숫자인데, 재귀 형태로 실행을 할 예정이다. ex) 1페이즈 이후 2페이즈 돌입 시, phase(1)이 실행.... 이는 페이즈카운터를 2로 맞추는 효과
										#(마치 리스트마냥 0번은 1페이즈, 1번은 2페이즈....)
		#thisphase = self.phaseCount #조금 변수를 난발하는 느낌이 없잖아 있긴 함. thisphase는 페이즈 카운터랑 똑같은 숫자라는 뜻. 
		
		w.setText(self.mouse_txt, 'x : ' + str(w.mouse_position_x) +'  y : ' + str(w.mouse_position_y))
		self.sprite_animation_loop(timestamp)
		self.hit_animation_loop(timestamp)
		sans_loop(timestamp)
		if (sans) :
			global sans_first
			if (sans_first) :
				for i in self.character[:2] :
					i.balloon = i.balloon_class(i, random.choice(i.says["awaken"]), 4)
				sans_first = False
				self.character[0].stress = 0
				self.character[1].stress = 0
				self.character[0].miss = 100
				self.character[0].skill[0].hit = 100
				self.character[1].miss = 100
				self.character[1].hit = 100
				for i in self.character[2:] :
					if (i.name == "Dead") :
						continue
					i.miss = 0
		for i in self.character :
			#if (i.name == "Dead") :
			#	continue
			if (i.balloon != None) :
				i.balloon.say_loop(timestamp)
		#여기에 페이즈 나타내는 전광판을 만들어야 할 텐데(지금 생각은 원이고 지름이 80이고 중심이 640, 80 이면 좋을 듯
		#페이즈가 새로고침 될 때마다 원이 눈이 감기듯 그 전부 검정 되지 말고 위 아래로 조금만 검정인 프레임 다음, 완전 검정 프레임, 그리고 다시 위 아래 조금만 검정인 프레임, 그리고 숫자 바뀐 원
		#이렇게 숫자 바뀌면 디테일적인 면에서 좀 재밌을 듯. 재생시키면 페이즈 카운터가 살아있듯이 눈 깜빡 하니까 숫자가 바뀐거니 
		#그때 쓰는 변수가 thisphase

		if (self.mob_time + 2 > timestamp) :
			return
		
		if (self.phaseFirst or self.nowTurn == self.available_num()) :
			self.nowTurn = 0
			self.nowPhase += 1
			speed = []
			for char in self.character:
				if char.name == "Dead": #뒤지면 None이 되버리기 때문에... 얘는 시체야. speed에 넣을 이유가??없다.
					continue
				else:
					speed.append([char.ID, char.speed]) #ID와 속도를 튜플로 리스트에 우겨넣음
					self.speed = sort_speed(speed) #그리고 그 튜플 리스트를 속도 빠른 순서로 후루룩 배열함. 그리고 거기서 ID만 쏙 빼서 리스트로 정리함
			self.phaseFirst = False
		
		if (self.turnFirst) :
			if (self.nowSprite != None) :
				self.nowSprite.skill_hide()
				w.hideObject(self.nowSprite.arrow_img)
				w.hideObject(self.nowSprite.info_txt)
				w.hideObject(self.selected_target.info_txt)
			try :
				self.nowSprite = self.character[self.speed[self.nowTurn][0]]
			except :
				self.nowTurn += 1
				return
			self.do_check()
			self.nowSprite.show_arrow()
			print('\n\n')
			print(self.nowSprite.name + '의 턴!  HP : ' + str(self.nowSprite.HP))
			self.set_bar()
			if self.nowSprite.name != "창" and self.nowSprite.name != "방패":
				self.selected_skill = self.nowSprite.skill[0]
				self.selected_target = self.character[random.choice([0, 1])]
				self.nowSprite.display_info()
				self.do_turn()
				self.log_print()
				if self.character[0].name == "Dead" :
					# 게임종료######################################################################
					data.game_status = 3
					w.update = update
					pass
				if self.character[2].name == "Dead" and self.character[3].name == "Dead" and self.character[4].name == "Dead":
					data.game_status = 2
					w.update = update
					# 게임완료######################################################################
					pass
				self.nowTurn += 1
				self.turnFirst = True
				self.mob_time = gui.time.perf_counter()
				self.set_bar()
				if (self.nowSprite.name != "Dead") :
					self.nowSprite.balloon = None
					self.nowSprite.balloon = self.nowSprite.balloon_class(self.nowSprite, random.choice(self.nowSprite.says["hit"]), 2)
				return

			else:
				self.nowSprite.display_info(190, 590)
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