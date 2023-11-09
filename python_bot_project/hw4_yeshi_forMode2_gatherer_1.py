'''
공학도를위한창의적컴퓨팅 과제#4

튜토리얼 시나리오#2의 목표를 달성하기 위한 의사 결정 흐름을 갖춘 예시 캐릭터입니다.
이 캐릭터는 중심 칸 주변의 자원을 수집하여 중심 칸 위 거점에 수납하는 것을 목표로 행동합니다.
(그렇다 보니 시나리오#1용 예시 캐릭터와 동등한 느낌으로 의사 결정을 수행해요)

- 여러분이 자신의 캐릭터 모듈을 만들 때 참고할 만한 코드가 적혀 있는 곳에는
  주석으로, NOTE 를 적어 표시해 두었어요.
'''

# 예시 캐릭터들의 이름은 Initialize()에서 infos.idx_me 값을 바탕으로 다시 정해요.
# 그래서 예시 캐릭터 모듈을 여러 개 복붙해 만들어서 각각 import해도 이름이 겹치지 않을 거예요.
stats = ['', 10, 10, 10]

ret_gather = 0
ret_move = 1
ret_occupy = 2
ret_build_base = 3
ret_build_teleporter = 4
ret_deposit = 5
ret_withdraw = 6
ret_warp = 7
ret_submit_request = 8
ret_wait = 9

dir_up = 0
dir_left = 1
dir_right = 2
dir_down = 3

requestcode_gather = 0
requestcode_build_base = 1
requestcode_build_teleporter = 2

data = 3
infos = 3


def Initialize():
    '''
    예시 캐릭터 설명

    Data 관점: 이 예시 캐릭터가 기록해 두면서 의사 결정에 활용하는 Data(를 담을 이름)

    - state: 내가 원래 뭐 하려 했었는지
        0 - 지정한 칸에서 수집하기
        1 - 손에 든 자원을 지정한 칸의 거점에 수납하기

    - pos: 위에서 언급한 '지정한 칸'의 좌표를 담아 둠. None을 담아 두는 경우 (수집할) 새 칸을 찾아야 함
    '''

    # 일단 게임을 시작하면 중심 칸에서 수집하는 것을 목표로 행동할 예정
    data.state = 0
    data.pos = (0, 0)

    stats[0] = f'Bot#02-{infos.idx_me}'


def MakeDecision():
    '''
    예시 캐릭터 설명

    Code 관점: 이 예시 캐릭터의 행동 패턴

    수집하는 것이 목표였다면...
        일단 먼저 수집할 새 칸을 찾아야 한다면 찾아서 기록해 둠
            
        이미 지정한 칸에 도착해 있는 상태라면...
            이번에 수집한 다음에 손이 가득 찰 예정이라면...
                다음 번 행동부터 (0, 0)의 거점에 수납하는 것을 목표로 하기로 기록해 둠
            이번에 수집해도 손이 가득 차지 않는다면...
                다음 번 의사 결정을 수행할 때 새 칸을 찾아야 한다고 기록해 둠
            return ret_gather
        (수집하는 것이 목표지만 아직 도착하지 않은 경우에 대해서는 아래에서 한꺼번에 다룸)
    
    수납하는 것이 목표였다면...
        이미 지정한 칸에 도착해 있는 상태라면...
            다음 번 행동부터 수집하는 것을 목표로 하기로 기록해 둠
            다음 번 의사 결정을 수행할 때 새 칸을 찾아야 한다고 기록해 둠
            return ret_deposit
        (수납하는 것이 목표지만 아직 도착하지 않은 경우에 대해서는 아래에서 한꺼번에 다룸)
    
    뺄셈을 해서 지정한 칸과 현재 칸 사이의 x축 방향 거리와 y축 방향 거리(이하 x거리, y거리) 계산
    |x거리| > |y거리| 라면...
        지정한 칸이 더 왼쪽에 있다면...
            return ret_move, dir_left
        return ret_move, dir_right

    지정한 칸이 더 위에 있다면...
        return ret_move, dir_up
    return ret_move, dir_down
    '''
    
    # 수집하는 것이 목표였다면...
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

