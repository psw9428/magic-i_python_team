'''
공학도를위한창의적컴퓨팅 과제#4

'내 캐릭터'를 구성하기 위한 문장들을 적기 위한 파일입니다.
'''

# 내 캐릭터의 이름과 힘, 민첩, 체력 능력치를 지정합니다.
# - 이름은 자유롭게 지정할 수 있어요(동명이인이 나오지 않도록 개성 있는 이름을 골라 주세요)
# - 능력치는 모두 0 이상의 int 형식 값이어야 하며, 세 능력치의 합은 30이어야 해요
stats = ['Dummy_shit', 15, 5, 10]




# 이 모듈 안에서 사용할 수 있는 이름들입니다. 해당 의미를 띄는 값을 미리 담아 두도록 지정되어 있습니다.
# 이 이름들은 다른 모듈에서 사용하지 않으므로, 원한다면 자신이 적기 쉬운 다른 이름들을 대신 도입해 다루어도 됩니다.

# 의사 결정 결과를 return할 때 사용할 수 있는 이름들
ret_gather = 0              # 수집
ret_move = 1                # 이동 (값 하나 추가 return 필요. 아래의 dir_up 등을 참고해 주세요)
ret_occupy = 2              # 점유
ret_build_base = 3          # 거점 건설
ret_build_teleporter = 4    # 텔레포터 건설
ret_deposit = 5             # 수납
ret_withdraw = 6            # 인출
ret_warp = 7                # 워프 (값 두 개 추가 return 필요. 워프할 칸에 대한 x, y 좌표를 추가로 return해야 해요)
ret_submit_request = 8      # 요청 게시 (값 하나 추가 return 필요. 아래의 requestcode_gather 등을 참고해 주세요)
ret_wait = 9                # 대기

# 의사 결정 결과로 이동 행동을 선택하여 return하고 싶을 때 사용할 수 있는 이름들
# 예: return ret_move, dir_up 엔터 를 실행하면 현재 칸에서 위 방향(y축 음수 방향)으로 이동하겠다고 고른 셈이 돼요
dir_up = 0
dir_left = 1
dir_right = 2
dir_down = 3

# 의사 결정 결과로 요청 게시 행동을 선택하여 return하고 싶을 때 사용할 수 있는 이름들
# 예: return ret_submit_request, requestcode_gather 엔터 를 실행하면 현재 칸에 대해 수집 요청을 게시하겠다고 고른 셈이 돼요
requestcode_gather = 0
requestcode_build_base = 1
requestcode_build_teleporter = 2


# 게임 진행 도중 담아 두어야 할 Data들이 있다면
# data.number = 3 엔터 와 같이 할당문을 적어 가며 기록해둘 수 있습니다.
# (지금은 3을 담아 두는 것 같이 보이는데,
#  게임 진행 도중에 core가 알아서 적당한 값을 담아줄 거예요)
data = 3

# 게임 내 공개 Data들에 액세스하기 위해 사용하는 이름입니다.
# 자세한 사용 방법은 과제 설명서를 참고해 주세요
# (지금은 3을 담아 두는 것 같이 보이는데,
#  게임 진행 도중에 core가 알아서 적당한 값을 담아줄 거예요)
infos = 3
global usingbase
global BaseTooBarran
global Barran
global Barrancount
# 게임을 시작하기 직전에 한 번 호출되는 함수입니다.
# data에 적절한 Data를 담아 두기 위한 문장들을 적어둘 수 있습니다.
def Initialize():
    global usingbase
    global BaseTooBarran
    global Barran
    global Barrancount
    usingbase = (0, 0)
    BaseTooBarran = False
    Barran = [(0, 0), ]
    Barrancount = 0
    data.state = 0
    data.pos = (0, 0)

    # 캐릭터 이름을 변경하고 싶은 경우 여기서 변경할 수 있어요.
    # 뭐 보통은 굳이 그럴 필요는 없기는 해요
    pass

def manhattan_distance(point1, point2):
    distance = 0
    x1, y1 = point1
    x2, y2 = point2
    distance = abs(x2 - x1) + abs(y2 - y1)
    return distance

    
def closestPoint(arr, fromPoint):
    closest = None
    min_distance = float('inf')

    for point in arr:
        distance = manhattan_distance(point, fromPoint)
        if distance < min_distance:
            min_distance = distance
            closest = point
    return closest

def distToBase(arr, fromPoint):

    distance = list(0 for i in range(0, len(arr)))
    for i in range(0, len(arr)):
        distance[i] = manhattan_distance(arr[i], fromPoint)

    return distance

def swap(a, b):
    temp = a
    a = b
    b = temp

def distanceSort(arr, fromPoint):
    distArr = distToBase(arr, fromPoint)
    for i in range(0, len(arr)-1):
        for j in range(i+1, len(arr)):
            if distArr[i] > distArr[j]:
                swap(arr[i], arr[j])
    
    return arr


def MakeDecision():
    global usingbase
    global BaseTooBarran
    global Barran
    global Barrancount

    if infos.stamina <= 0:
        return ret_wait

    if data.state == 0:

        if data.pos == None:
            x_center = 0
            y_center = 0
            distance = 1
            lookBarran = 0


            while data.pos == None:

                count_candidates = 4 * distance
                x_candidate = x_center + distance
                y_candidate = y_center
                count_checked = 0

                while count_checked < count_candidates and data.pos == None:

                    if infos.myPlane[x_candidate, y_candidate] >= infos.max_r_carrying:
                        data.pos = (x_candidate, y_candidate)

                    count_checked = count_checked + 1

                    phase = count_checked // distance
                    offset = count_checked % distance
                    x_candidate = x_center + (1 - (phase     & 2)) * (distance * (1 -  phase      % 2) - offset)
                    y_candidate = y_center + (1 - (phase - 1 & 2)) * (distance * (1 - (phase - 1) % 2) - offset)

                count_candidates = 4 * distance
                x_candidate = x_center + distance
                y_candidate = y_center
                count_checked = 0

                while count_checked < count_candidates and data.pos == None:
                    if infos.myPlane[x_candidate, y_candidate] > 0:
                        data.pos = (x_candidate, y_candidate)


                    count_checked = count_checked + 1
    
                    phase = count_checked // distance
                    offset = count_checked % distance

                    x_candidate = x_center + (1 - (phase     & 2)) * (distance * (1 -  phase      % 2) - offset)
                    y_candidate = y_center + (1 - (phase - 1 & 2)) * (distance * (1 - (phase - 1) % 2) - offset)
                    
                lookBarran = lookBarran + 1
                distance = distance + 1

            if (lookBarran > 3):
                BaseTooBarran = True
        
        if infos.pos_me == data.pos:

            if infos.r_carrying + infos.myPlane[infos.pos_me] >= infos.max_r_carrying:
                data.state = 1
                data.pos = usingbase
            if infos.r_carrying + infos.myPlane[infos.pos_me] < infos.max_r_carrying:
                data.pos = None
            
            return ret_gather

    if data.state == 2:
        #usingbase를 리셋하는 상태 
        #BaseTooBarren = True 일 때 리셋
        sortArr = distanceSort(infos.pos_bases, infos.pos_me)
        Barran.append(usingbase)
        Barrancount = Barrancount + 1
        #다신 이 버려진 곳으로 오지 않도록... 특수한 상황이 아니라면
        point = 0
        
        for i in Barran:
            if i == closestPoint(infos.pos_bases, infos.pos_me):
                continue
            point = point + 1
        if (point == Barrancount):
            usingbase = closestPoint(infos.pos_bases, infos.pos_me)
        
        
        BaseTooBarran == False
        data.pos = usingbase
        #usingbase로 이동
        if (manhattan_distance(closestPoint(infos.pos_teleporters, infos.pos_me), infos.pos_me) + manhattan_distance(closestPoint(infos.pos_teleporters, usingbase), usingbase)< manhattan_distance(usingbase, infos.pos_me)):
            data.state = 3
            data.pos = closestPoint(infos.pos_teleporters, infos.pos_me)
            ToGo = closestPoint(infos.pos_teleporters, usingbase)
            return ret_wait
        if infos.pos_me == usingbase:
            data.state = 0
        
    
    if data.state == 3:
        if infos.pos_me == data.pos:
            return ret_warp, ToGo[0], ToGo[1]


    #거점에 왔고 다시 수집을 하러 나가야함
    if data.state == 4:
        if infos.stamina + infos.coef_stamina_heal_on_base >= infos.max_stamina:
            data.state = 0
            data.pos = None
            return ret_wait
        else:
            return ret_wait

        

    # 수납하는 것이 목표였다면...
    if data.state == 1:
        # 이미 지정한 칸에 도착해 있는 상태라면 수납
        if infos.pos_me == data.pos:
            if BaseTooBarran == True:
                data.state = 2
            # 다음 번 의사 결정을 수행할 때 새 칸을 찾아야 한다고 기록해 둠
                data.pos = None

            else:
                data.state = 4
                data.pos = None
            return ret_deposit

    x_distance = data.pos[0] - infos.pos_me[0]
    y_distance = data.pos[1] - infos.pos_me[1]

    if abs(x_distance) > abs(y_distance):

        if x_distance < 0:
            return ret_move, dir_left
        
        return ret_move, dir_right
    if y_distance < 0:
        return ret_move, dir_up
    
    return ret_move, dir_down


# ☆ 이 아래에 있는 if문은 여러분이 이 파일 붙잡고 F5 눌렀을 때도 테스트를 진행해 볼 수 있도록 적어 두었어요
# - 과제를 진행할 때는 이 파일 붙잡고 F5 눌러 실행하면
#   나중에 게임이 종료/중단된 이후에도 interactive에서 각 이름들을 적어 가며 '마지막에 뭐 담겨 있었나'를 볼 수 있어요
if __name__ == '__main__':
    import hw4_core
    hw4_core.run()

