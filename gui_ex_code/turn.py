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
import random
import main_start



window_width = 1280
window_height = 720

w = gui.Window('test', window_width, window_height)
cwd = str(os.getcwd()).replace('\\', '/')
data = w.data

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
		for i in self.nowSprite :
			i.skill_loop(timestamp)
		for i in self.skill.possible :
			self.character[i].target_me_loop(timestamp)
		

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
					speed.append((char.ID, char.speed)) #ID와 속도를 튜플로 리스트에 우겨넣음
					self.speed = sort_speed(speed) #그리고 그 튜플 리스트를 속도 빠른 순서로 후루룩 배열함. 그리고 거기서 ID만 쏙 빼서 리스트로 정리함
			self.phaseFirst = False
		
		if (self.turnFirst) :
			self.nowSprite = self.character[self.speed[self.nowTurn]]
			for i in self.nowSprite.skill :
				w.showObject(i.img)
			self.turnFirst = False
			#self.turn(self.speed[self.nowTurn])
		
		for i in self.nowSprite.skill :
			if (i.skill_loop(timestamp)) :

			

		#if (info_speed[self.nowTurn]) :
		
		# for i in info_speed: #그러면 info_speed 에는 속도 빠른 놈부터 ID가 쫘라라라락 들어있는 거임
		# 	for char in self.character: #스테이지에 참여중인 것들 중에서...
		# 		if info_speed[i] == char.ID: #info_speed의 i번째랑 똑같은 ID를 가진 애를 찾음
		# 			self.turn(char.ID) #아 여기서 알아야 할 것이, ID가 위치랑 똑같은 거임. 이제 그 아이디를 가진 애 턴을 실행시킴(여기서부터는 turn 함수를 보면 됨)


		# 			#턴에 해당하는 애의 배경이 조금 밝에 빛나면 베스트, 그게 아니더라도 화살표가 머리 위에 뾱 뜨면 좋지
		# 			#동시에 걔의 스탯
		# 			#HP
		# 			#스트레스
		# 			#미친 여부
		# 			#방어력
		# 			#명중률
		# 			#회피율
					


		# 			if self.character[0] == None: #아 턴이 끝났는데, 창이 죽었네
		# 				#gameover #그럼 져야지. 불만 없지?
						

		# 				#여기에 game over 되면 나오는 화면이 등장해야함!


		# 				pass
		# 			if self.character[2] == None and self.character[3] == None and self.character[4] == None: #턴 끝나고 적팀이 다 뒤졌네?
		# 				#stage end #잘했어 이 스테이지는 끝이야


		# 				#여기에 다음 스테이지로 넘어가는 부분 등장해야함!


		# 				pass
		# self.phase(self.phaseCount)#루프로 모두의 턴이 다 돌고 이제 다음 페이즈가 시작이 된다.
	'''	
	def turn(self, pos): #이거는 개별 턴 함수임
		#check if who's condition
		if self.character[pos].state.num % 2 == 0: #중독되면 state.num의 정수가 기본 1이었다가 2를 곱해. 즉, 지금 2로 나누었는데, 나머지가 0이면, 얘는 2를 곱했다는거지. 그러니까. 중독이라는거야.
			self.character[pos].state.poison[0] -= 1 #state에는 poison튜플이 있는데 이건 (남은 쳐맞는 턴수, 쳐맞을 때 데미지)의 튜플이지. 턴수 하나 줄이고
			self.character[pos].HP -= self.character[pos].state.poison[1] #데미지 넣고
			if self.character[pos].HP <= 0: #데미지 받았는데 죽었네? 수고링
				if pos == 1: #그런데 죽은게 방패였네
					self.character[pos].HP == self.character[pos].MAXHP #그럼 부활
					self.character[pos].stress += 10 #스트레스 조금 받고
					self.character[0].stress += 5 #창도 스트레스 조금 받고
				else:
					self.character[pos] = None #None으로 바꿔


					#사망 대사 뽷 나와주고


				return #그리고 이 turn함수를 빠져 나와야함
			
				#여기서 return을 쓰는게 맞는지 모르겠네?


			if self.character[pos].state.posion[0] == 0: #다 맞았다. 지금을 끝으로 더이상 중독이 아니야
				self.character[pos].state.poison[1] = 0 #데미지도 0으로 만들고
				self.character[pos].state.num  /=  2 #이제 2로 나눠줘


		if self.character[pos].state.num % 3 == 0: #중독이랑 같은 메커니즘(2, 3, 5, 7 얘네가 소수라 서로 겹칠 일도 없고, 수학적으로 완벽한 설정법인듯 하하)
			self.character[pos].state.bleed[0] -= 1 #이것도 마찬가지


			#이쯤에서 잠깐 돌아보는, state에 뭐가 있어야 하는지
			#state에는 일단 정수, 기본적으로 1인 친구가 존재
			#그리고
			#poison = (턴수, 데미지)
			#bleed = (턴수, 데미지)
			#fear = (턴수, 스트레스 양)
			#끝

			self.character[pos].HP -= self.character[pos].state.bleed[1]
			if self.character[pos].HP <= 0: #데미지 받았는데 죽었네? 수고링
				if pos == 1: #그런데 죽은게 방패였네
					self.character[pos].HP == self.character[pos].MAXHP #그럼 부활
					self.character[pos].stress += 10 #스트레스 조금 받고
					self.character[0].stress += 5 #창도 스트레스 조금 받고
				else:
					self.character[pos] = None #None으로 바꿔


					#사망 대사 뽷 나와주고


				return #그리고 이 turn함수를 빠져 나와야함
			
				#여기서 return을 쓰는게 맞는지 모르겠네?
			if self.character[pos].state.bleed[0] == 0:
				self.character[pos].state.bleed[1] = 0
				self.character[pos].state.num  /= 3

		if self.character[pos].state.num % 7 == 0: #얘가 스트레스인데
			self.character[pos].state.fear[0] -= 1
			self.character[pos].stress += self.character[pos].state.fear[1] #데미지랑 다르게 빼는게 아니라 더해야 함
			if self.character[pos].stress >= 100: #이제 붕괴인데 원래 붕괴인 얘였으면 뭔가 달라지면 안되니까
				if self.character[pos].collapse == None: #원래 붕괴였니? 물어보고
					self.character[pos].collapse = random.choice([100199, 100199, 100199, 100299, 100299, 100399, 100399, 200199, 200299, 200399]) #붕괴 아니면 요롷게(70프로 확률 미침, 30프로 각성)
					if self.character[pos].collapse == LAST_DANCE: #근데 회광반조이라면, 순식간에 피가 차야해. 그래서 MAXHP로 HP를 바꿔
						self.character[pos].HP = self.character[pos].MAXHP
						self.character[pos].stress = 0
						self.character[pos].state.num = 1
				pass
			if self.character[pos].stress >= 200: #그런데 스트레스가 너무 쌓였네. 200이 되어버렸네. 심장마비로 죽어야겠지?
				if pos == 1: #그런데 죽은게 방패였네
					self.character[pos].HP == self.character[pos].MAXHP #그럼 부활
					self.character[pos].stress += 10 #스트레스 조금 받고
					self.character[0].stress += 5 #창도 스트레스 조금 받고
				else:
					self.character[pos] = None #None으로 바꿔


					#사망 대사 뽷 나와주고
				return #그리고 이 turn함수를 빠져 나와야함
			
				#여기서 return을 쓰는게 맞는지 모르겠네?
			
			if self.character[pos].fear[0] == 0:
				self.character[pos].state.num /= 7
			

			#이쯤에서 알아보는, collapse에 뭐가 있나
			#collapse에는 붕괴코드가 있음. 끝

		if self.character[pos].state.num % 5 == 0: #이건 그냥 스턴.....
			self.character[pos].state.num /= 5 #바로 스턴 풀고
			return #턴 끝
		
		match self.character[pos].collapse: #데미지 정산은 끝났고, 턴마다 미치거나 각성한 애들이 뭐라뭐라 하는 부분!!
			case 100199: #절망일 경우
				#despair
				if pos == 0:
					other = 1
				elif pos == 1:
					other = 0
					#진짜 미련하게 코드를 짜기는 했다.... 무튼 지금을 pos라고 받았으니, 스트레스는 창과 방패만 받으니까. 나머지 애 위치를 other로 받는거야
				if self.character[other] is not None: #근데 나머지 한명이 죽지 않았을 때만 나머지 애한테 헛소리를 하면서 스트레스를 줘
					self.character[other].stress += 15
				#스트레스 주는 대사 #예를 들면 아저씨 우리 도망가요. 네? 이제 그만 하자구요 이런거 // 또는 아저씨는 이런 X발 안해먹는다고 했잖아! 이런거
				probability = random.randint(1, 100) #그리고 70프로 확률로 헛소리 하면서 턴 넘기기
				if probability <= 70: #딱 70프로에 들어왔다면
					#안해먹어 대사 #예를 들어 이제 더이상은 무리야... 이런거
					return #턴 끝
			case 100299: #이건 상대방의 힐은 안받는거라서 지금 뭔가 행동을 하지는 않아
				pass
			case 100399: #이건 정신착란인데
				if pos == 1: #방패라면
					probability = random.randint(1, 100)
					if probability <= 50: #50프로 확률로
						#안해먹어 대사 #턴을 넘겨버리는거지
						return
					else:
						target = random.randint(0, 4) #턴을 넘기는게 아니라면 자신을 포함 
						if self.character[target] is not None: #아 근데 살아있는 대상에게만
							self.character[target].HP -= 5 #5만큼의 주먹질을 하고

							if target.HP <= 0: #근데 때렸는데 죽었네
								for i, char in enumerate(self.character):
									if target == char:
										self.character[i] = None
										return


						else: #그게 아니라면 그냥 턴 넘기기
						#헛것을 보는 대사
							return

				elif pos == 0: #근데 창이라면?
					probability = random.randint(1, 100)
					if probability <= 60: #60프로의 확률로
						self.character[pos].state.num *= 5 #스스로에게 스턴을 걸어버리는거지
						#비명 지르기
						return #그리고 턴 끝내버리기
			case 200199:
				#기사회생
				if pos == 0:
					other = 1
				elif pos == 1:
					other = 0 #똑같이 다른 캐릭터를 other로 붙잡고
				if self.character[other] is not None: #안죽었다면
					self.character[pos].speed += 2 
					self.character[other].speed += 2 #둘다 속도가 2 빨라짐
					self.character[pos].HP += 5
					if self.character[pos].HP > self.character[pos].MAXHP:
						self.character[pos].HP = self.character[pos].MAXHP #그리고 자기 피도 5 채움

				else: #나머지 팀원 죽었어 ㅠㅠ
					self.character[pos].speed += 2 #혼자만 빨라지고
					self.character[pos].HP += 5 #혼자만 체력 회복
					if self.character[pos].HP > self.character[pos].MAXHP:
						self.character[pos].HP = self.character[pos].MAXHP #그리고 자기 피도 5 채움
				pass
			case 200299:
				#차분한 영혼
				if pos == 0:
					other = 1
				elif pos == 1:
					other = 0 #이것도 뭐 다른 팀원 other에 넣는거
				if self.character[other] is not None:
					self.character[pos].stress -= 15
					self.character[other].stress -= 15
				else:
					self.character[pos].stress -= 15
				#할 수 있어 대사
				
			case 200399:
				#회광반조
				self.character[pos].HP  -= self.character[pos].MAXHP / 4 #4턴만 살아있는 회광반조. 대신 그동안 같은 팀원 무적.
			case 999999:
				#무의식의 극의
				pass
			case _:
				pass
			
		
		#do the turn
		#select skill and target
		if pos >= 2:
			select = self.character[pos].skill
			target = random.choice(select.possible)

		if select.damage < 0: #이거는 힐 또는 대신맞기
			if select.otherEffect == HEAL:	#자 여기에서 잠깐 확인 들어가야함

				if target.collapse == DESPAIR:
					probability = random.randint(1, 100)
					if probability <= 70:
						#힐 개무시함.


						#편집증 대사 하나 나오고 뙇!


						return


				#select는 self.character[pos].skill 중 하나일 것이라는 거지.
				#skill 안에는 여러가지가 있는데

				#skill 안에는 otherEffect가 있어
				#힐이면 otherEffect = 22299
				#대신맞기이면 otherEffect = 11199
				
				
				#그리고 공격 스킬이면
				#otherEffect는 이제 튜플의 리스트가 돼.
				#스턴, 출혈, 중독 다 들어간 미친 스킬일 경우
				#otherEffect = [(50099, 0, 0)스턴, (20099, 턴수, 턴당 데미지)중독, (30099, 턴수, 턴당 데미지)출혈, (70099, 0(일회성), 턴당 스트레스)스트레스]

				probability = random.randint(1, 100)
				if select.critical <= probability: #크리티컬이 뜨면
					target.HP -= select.crit_damage

					#크리티컬이라는 효과와 함께 힐 효과


					if target.MAXHP < target.HP:
						target.HP = target.MAXHP
				else:
					target.HP -= select.damage

					#이건 그냥 힐

					if target.MAXHP < target.HP:
						target.HP = target.MAXHP
				return
			

			elif select.otherEffect == DEFENSE:
				target.defender = self.character[pos] #딱 한턴만 대신 맞아준다는 소리

				#이거는 이제 방어해주는 모션 넣기

				#여기에서 또 주의
				#self.character[pos]에는 defender 이라는 변수 존재. 얘는 원래 (None, 0)값임

			elif select.otherEffect == STRESSHEAL: #창만 가지는 유일무의 스킬. 한턴 쉬고 자기 스트레스 힐하기
				self.character[pos].stress -= 30


				#여기서 약간 휴식하는 모션 넣기



		if 	select.damage >= 0: #이제 주는 데미지일 때
			if pos == 0:
				probability = random.randint(1, 100)
				if probability <= self.character[pos].hit: #명중하면
					probability = random.randint(1, 100)
					if probability <= target.miss: #회피하고
					

					#여기서 회피 그림 뙇 뜨고
						self.character[pos].stress += 50 #굉장히 스트레스를 많이 받음(연사하지 못하게 방지책)
						return #회피했으니 이후 그 어떤 효과도 안받는다
					
					else:
						target.HP -= select.damage

						#바로 즉사하는 모션

						self.character[pos].stress += 50
						return

				else:
					self.character[pos].stress += 50
					return #명중 안하면 빗나감이니 그것도 어떤 효과도 안받는다
		
				


			if target.defender is not None: #맞아주는 애가 있을 때...
				defended = target
				target = target.defender #### 유의
				defended.defender = None #원래 애의 defender를 이제 없애고, 대신 맞아주는 애로 타겟을 바꿈
			probability = random.randint(1, 100)
			if probability <= select.hit: #명중하면
				probability = random.randint(1, 100)
				if probability <= target.miss: #회피하고
					

					#여기서 회피 그림 뙇 뜨고

					return #회피했으니 이후 그 어떤 효과도 안받는다
				else: 
					if target.collapse == LAST_DANCE:
						target.HP -= 0
						return
					else:
						probability = random.randint(1, 100)
						if select.critical <= probability: #크리티컬이 뜨면
							target.HP -= select.crit_damage
						else:
							target.HP -= select.damage
				
			else:
				return #명중 안하면 빗나감이니 그것도 어떤 효과도 안받는다
		

			if target.HP <= 0: #체력이 0 아래로 내려가면
				for i, char in enumerate(self.character):
					if target == char:
						self.character[i] = None #죽여버리는 코드
			

			for status in select.otherEffect: #그리고 이제 그냥 데미지 말고 다른 추가적인 효과들이 있나 확인


				#알아야 할 것... self.character 에는 refuse도 있음. refuse안에 이제 stun, poison, bleed 계수 있음



				if status[0] == STUN: #스턴일 때
					probability = random.randint(1, 100)
					if target.refuse.stun <= probability: #스턴 저항이면 아무 일도 안일어남

						#저항해도 모션은 똑같이 맞는모션


						pass
					else:
						target.state.num *= 5 #아니면 스턴


						#맞는모션

						if target.collapse == LAST_DANCE: #그런데 회광반조이면 아무 일도 일어나면 안되지
							target.state.num /= 5
						



				if status[0] == POISON:
					probability = random.randint(1, 100)
					if target.refuse.poison <= probability:


						#맞는 모션

						pass
					else:
						target.state.num *= 2

						#맞는 모션


						if target.collapse == LAST_DANCE:
							target.state.num /= 2
						else:
							target.state.poison[0] = status[1]
							target.state.poison[1] = status[2]



				if status[0] == BLEED:
					probability = random.randint(1, 100)
					if target.refuse.bleed <= probability:

						#맞는 모션



						pass
					else:
						target.state.num *= 3


						#맞는 모션


						if target.collapse == LAST_DANCE:
							target.state.num /= 3
						else:
							target.state.bleed[0] = status[1]
							target.state.bleed[1] = status[2]



				if status[0] == FEAR:
					target.state.num *= 7

					#맞는 모션


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
							if self.character[pos].collapse == LAST_DANCE: #근데 회광반조이라면, 순식간에 피가 차야해. 그래서 MAXHP로 HP를 바꿔
								self.character[pos].HP = self.character[pos].MAXHP
								self.character[pos].stress = 0
								self.character[pos].state.num = 1
						pass
					if target.stress >= 200:
						target.stress = 200
						target.HP = 0
						for i, char in enumerate(self.character):
								if target == char:
									self.character[i] = None
									return

					return
			

			

		
			




		



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

w.start()'''
