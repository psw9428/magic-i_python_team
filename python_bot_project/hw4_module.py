'''
공학도를위한창의적컴퓨팅 과제#4

'내 캐릭터'를 구성하기 위한 문장들을 적기 위한 파일입니다.
'''

# 내 캐릭터의 이름과 힘, 민첩, 체력 능력치를 지정합니다.
# - 이름은 자유롭게 지정할 수 있어요(동명이인이 나오지 않도록 개성 있는 이름을 골라 주세요)
# - 능력치는 모두 0 이상의 int 형식 값이어야 하며, 세 능력치의 합은 30이어야 해요
stats = ['MJY', 15, 5, 10]




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

# 게임을 시작하기 직전에 한 번 호출되는 함수입니다.
# data에 적절한 Data를 담아 두기 위한 문장들을 적어둘 수 있습니다.
def Initialize():
    # 캐릭터 이름을 변경하고 싶은 경우 여기서 변경할 수 있어요.
    # 뭐 보통은 굳이 그럴 필요는 없기는 해요
    pass

plane_info =[]
def print_plain() :
    plane_array = []
    size = 100
    half = size//2
    for i in range(0, size) :
        a = []
        for j in range(0, size) :
            a.append('X')
        plane_array.append(a)
    i = -half
    while i <= half :
        j = -half
        while j <= half :
            tmp = infos.publicPlane[i, j]
            #plane_array[i + half][j + half] = tmp.r_toOccupy
            if tmp.r_toOccupy == 0 :
                plane_array[i+half][j+half] = 'O'
            if (tmp.r_toBuildBase > 0 and int(25 * 1.6 ** ((abs(i) + abs(j))/512)) > tmp.r_toBuildBase) :
                plane_array[i+half][j+half] = 'N'
            if (tmp.r_toBuildBase == 0) :
                plane_array[i+half][j+half] = 'B'
            if (tmp.r_toBuildTeleporter == 0) :
                plane_array[i+half][j+half] = 'T'
            if (tmp.count_characters > 0) :
                plane_array[i+half][j+half] = 'P'
            j += 1
        i += 1
    plane_array[infos.pos_me[0] + half][infos.pos_me[1] + half] = '@'
    return plane_array

def manhattan_distance(point1, point2):
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

# 내 캐릭터의 다음 행동을 결정하기 위한 의사 결정을 수행합니다.
def MakeDecision():
    plane_info.append(print_plain())

    if data.state == 0:
        # 수집할 새 칸을 찾아야 한다면...
        if data.pos == None:
            # NOTE 중심 칸에서 가까운 칸부터 체크하며 자원이 남아 있는 칸을 찾아 기록하는 Code 예시예요.
            #      내 캐릭터 모듈 만들 때 가져가서 쓸 수 있어요(미리 Initialize()에서 이름 data.pos를 등재해 두기만 하면 돼요).
            #      이 버전은 효율이 그리 높지 않으니, 다른 부분을 먼저 완성한 다음 살짝 개선해 보는 것을 추천해요
            
            # 3단 콤보-1-1. 중심 칸을 기준으로 거리가 1인 칸부터 체크하기 시작
            # NOTE 중심 칸이 아닌 다른 칸을 기준으로 삼고 싶다면, 또는 거리가 2 이상인 칸부터 체크하고 싶다면 여기를 고치면 돼요.
            #      (중심 칸 자체는 아래 반복 흐름으로는 체크할 수 없으니 별도 Code를 도입해야 해요)
            #      자원 수집 요청 달성에 기여하려면 대상 칸 주변 두 칸 범위 안에서 수집 행동을 해야 한다는 점을 기억해 주세요
            x_center = 0
            y_center = 0
            distance = 1

            # 3단 콤보-1-2. 자원이 있는 칸을 찾아 기록해 둘 때까지...
            while data.pos == None:
                # 3단 콤보-2-1. 해당 거리만큼 떨어진 칸들(4 * distance개) 중 가장 오른쪽에 있는 칸부터 시계방향으로 체크
                count_candidates = 4 * distance
                x_candidate = x_center + distance
                y_candidate = y_center
                count_checked = 0

                # 3단 콤보-2-2. 모든 칸들을 다 체크하거나 자원이 있는 칸을 찾아 기록해 둘 때까지...
                while count_checked < count_candidates and data.pos == None:
                    # 해당 칸에 자원이 있다면 기록
                    if infos.myPlane[x_candidate, y_candidate] > 0:
                        data.pos = (x_candidate, y_candidate)

                    # 3단 콤보-2-3. 다음에 체크할 칸 좌표 계산
                    count_checked = count_checked + 1

                    '''
                    현재 목표상, distance == 2일 때를 보면...
                    __6__
                    _5_7_
                    4_C_0
                    _3_1_
                    __2__
                    ...와 같은 순서로 체크하게 돼요.

                    각각 x거리와 y거리를 나열해 보면서,
                    count_checked 값에 따라 x거리와 y거리를 계산하는 수식을 아래와 같이 세워둘 수 있어요(다른 방법도 많음)
                    c p o  x  y
                    0 0 0 +2  0
                    1 0 1 +1 +1
                    2 1 0  0 +2
                    3 1 1 -1 +1
                    4 2 0 -2  0
                    5 2 1 -1 -1
                    6 3 0  0 -2
                    7 3 1 +1 -1
                    '''
                    phase = count_checked // distance
                    offset = count_checked % distance
                    # distance == 2일 때 [+1, +1, +1, +1, -1, -1, -1, -1]과 [2, 1, 0 -1, 2, 1, 0 -1]을 각 자리별로 곱하는 셈이 돼요
                    x_candidate = x_center + (1 - (phase     & 2)) * (distance * (1 -  phase      % 2) - offset)
                    # x버전 수식을 들고 와서 phase를 phase - 1로 고쳐 적었어요
                    # (수식 1 - (phase - 1) % 2는 수식 phase % 2로 축약 가능하기는 해요)
                    y_candidate = y_center + (1 - (phase - 1 & 2)) * (distance * (1 - (phase - 1) % 2) - offset)

                # 3단 콤보-1-3. 한 칸 더 멀리 있는 칸들을 체크하기 시작
                distance = distance + 1
                
        
        # 이미 지정한 칸에 도착해 있는 상태라면 수집
        # NOTE 두 좌표가 동일한지 재고 싶을 때 == 연산자를 사용할 수 있어요
        if infos.pos_me == data.pos:
            # 이번에 수집한 다음에 손이 가득 찰 예정이라면...
            if infos.r_carrying + infos.myPlane[infos.pos_me] >= infos.max_r_carrying:
                # 다음 번 행동부터 (0, 0)의 거점에 수납하는 것을 목표로 하기로 기록해 둠
                data.state = 1
                # NOTE 중심 칸이 아닌 다른 칸의 거점에 수납하고 싶다면 여기를 고치면 돼요.
                #      어느 거점으로 향할 것인지는, 위에 적혀 있는 '수집할 새 칸을 찾는 Code'를 참고해서 만들 수도 있지만,
                #      미리 infos.pos_bases에 거점이 있는 좌표 목록을 담아 두었으니, 이걸 털어보는 것을 추천해요
                data.pos = (0, 0)
            # 이번에 수집해도 손이 가득 차지 않는다면...
            if infos.r_carrying + infos.myPlane[infos.pos_me] < infos.max_r_carrying:
                # 다음 번 의사 결정을 수행할 때 새 칸을 찾아야 한다고 기록해 둠
                data.pos = None
            
            return ret_gather

    # 수납하는 것이 목표였다면...
    if data.state == 1:
        # 이미 지정한 칸에 도착해 있는 상태라면 수납
        if infos.pos_me == data.pos:
            # 다음 번 행동부터 수집하는 것을 목표로 하기로 기록해 둠
            data.state = 0
            # 다음 번 의사 결정을 수행할 때 새 칸을 찾아야 한다고 기록해 둠
            data.pos = None
            return ret_deposit

    # 이동
    
    # 뺄셈을 해서 지정한 칸과 현재 칸 사이의 x축 방향 거리와 y축 방향 거리(이하 x거리, y거리) 계산
    # NOTE 내 위치와 목적지 사이의 거리를 잴 때는 
    #      내 위치를 원점으로 두고 계산하도록 신경써 두는 것이 편할 거예요
    #
    # NOTE x좌표는 [0], y좌표는 [1]에 담겨 있다는 점,
    #      수학 동네와 다르게 컴퓨터 동네의 2D 좌표계에서 y축은 아래 방향이 양수 방향이라는 점도 기억해 둬요
    x_distance = data.pos[0] - infos.pos_me[0]
    y_distance = data.pos[1] - infos.pos_me[1]

    # |x거리| > |y거리| 라면...
    #
    # NOTE built-in 함수 abs()를 사용하면 간편하게 어떤 숫자 형식(bool 형식 제외 -> 각각 0, 1로 간주) 값에 대한 절대값을 구할 수 있어요
    if abs(x_distance) > abs(y_distance):
        # 지정한 칸이 더 왼쪽에 있다면...
        if x_distance < 0:
            return ret_move, dir_left
        
        return ret_move, dir_right

    # (|x거리| <= |y거리| 면서) 지정한 칸이 더 위에 있다면...
    if y_distance < 0:
        return ret_move, dir_up
    
    return ret_move, dir_down


# ☆ 이 아래에 있는 if문은 여러분이 이 파일 붙잡고 F5 눌렀을 때도 테스트를 진행해 볼 수 있도록 적어 두었어요
# - 과제를 진행할 때는 이 파일 붙잡고 F5 눌러 실행하면
#   나중에 게임이 종료/중단된 이후에도 interactive에서 각 이름들을 적어 가며 '마지막에 뭐 담겨 있었나'를 볼 수 있어요
if __name__ == '__main__':
    import hw4_core
    hw4_core.run()

