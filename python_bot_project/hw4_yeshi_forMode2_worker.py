'''
공학도를위한창의적컴퓨팅 과제#4

튜토리얼 시나리오#2의 목표를 달성하기 위한 의사 결정 흐름을 갖춘 예시 캐릭터입니다.
이 캐릭터는 중심 칸의 거점에서 자원을 인출하며 중심 칸에서 (0, 8)까지 차례대로 점유를 수행합니다.

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
        0 - 지정한 칸의 거점에서 손이 가득 찰 때까지 인출
        1 - 지정한 칸을 향해 이동하며, 점유되지 않은 칸을 점유

    - pos: 위에서 언급한 '지정한 칸'의 좌표를 담아 둠. None을 담아 두는 경우 새 칸을 찾아야 함
    '''

    # 일단 게임을 시작하면 중심 칸의 거점에서 손이 가득 찰 때까지 자원을 인출하는 것을 목표로 행동함
    data.state = 0
    data.pos = (0, 0)

    stats[0] = f'Bot#02-{infos.idx_me}'


def MakeDecision():
    '''
    예시 캐릭터 설명

    Code 관점: 이 예시 캐릭터의 행동 패턴

    인출하는 것이 목표였다면...
        일단 먼저 인출할 거점을 정해야 한다면 현재 칸에서 가장 가까운 거점을 찾아 지정해 둠
            
        이미 지정한 칸에 도착해 있는 상태라면...
            거점에 자원이 하나도 없다면...
                return ret_wait
            
            이번에 인출한 다음에 손이 가득 찰 예정이라면...
                다음 번 행동부터 (0, 8)까지 이동하며 점유하는 것을 목표로 하기로 기록해 둠
                
            return ret_withdraw
        (인출하는 것이 목표지만 아직 도착하지 않은 경우에 대해서는 아래에서 한꺼번에 다룸)
    
    점유하는 것이 목표였다면...
        현재 칸이 점유되어 있지 않다면...
            다음 번 행동부터 인출을 목표로 하기로 기록해 둠
            다음 번 의사 결정을 수행할 때 새 칸을 찾아야 한다고 기록해 둠
            return ret_occupy
    
        (점유하는 것이 목표지만 아직 도착하지 않은 경우에 대해서는 아래에서 한꺼번에 다룸)
    
    뺄셈을 해서 지정한 칸과 현재 칸 사이의 x축 방향 거리와 y축 방향 거리(이하 x거리, y거리) 계산
    |x거리| > |y거리| 라면...
        지정한 칸이 더 왼쪽에 있다면...
            return ret_move, dir_left
        return ret_move, dir_right

    지정한 칸이 더 위에 있다면...
        return ret_move, dir_up
    return ret_move, dir_down
    '''
    
    # 인출하는 것이 목표였다면...
    if data.state == 0:
        # 인출할 거점을 정해야 한다면...
        if data.pos == None:
            # NOTE 현재 칸에서 가장 가까운 거점을 찾는 Code 예시예요.
            #      중심 칸에는 항상 거점이 있으니, 공유 평면 위에는 항상 최소 한 개의 거점이 존재해요 -> 거점 찾기는 절대 실패하지 않아요

            # 일단 거점 목록에 있는 0번째 좌표가 '가장 가까운 거점의 좌표'라고 가정
            data.pos = infos.pos_bases[0]
            distance_nearest = abs(infos.pos_me[0] - data.pos[0]) + abs(infos.pos_me[1] - data.pos[1])
            
            # 가정이 맞는지 검증
            for pos_candidate in infos.pos_bases:
                distance_candidate = abs(infos.pos_me[0] - pos_candidate[0]) + abs(infos.pos_me[1] - pos_candidate[1])
                
                # 반례 발견시 가정 수정
                if distance_candidate < distance_nearest:
                    data.pos = pos_candidate
            
        # 이미 지정한 칸에 도착해 있는 상태라면...
        # NOTE 두 좌표가 동일한지 재고 싶을 때 == 연산자를 사용할 수 있어요
        if infos.pos_me == data.pos:
            # NOTE 자주 사용할 예정인 값은 미리 계산해 담아 두고 진행할 수 있어요.
            #      이렇게 하면 코드 적기도 쉽고, 의사 결정에 걸리는 (현실) 시간도 그럭저럭 절약될 거예요
            r_stored = infos.publicPlane[infos.pos_me].r_stored
            
            # 거점에 자원이 하나도 없다면 대기
            if r_stored == 0:
                return ret_wait
            
            # 이번에 인출한 다음에 손이 가득 찰 예정이라면...
            if infos.r_carrying + r_stored >= infos.max_r_carrying:
                # 다음 번 행동부터 (0, 8)까지 이동하며 점유하는 것을 목표로 하기로 기록해 둠
                data.state = 1
                # NOTE 다른 칸을 목적지로 지정하고 싶은 경우 여기를 고치면 돼요
                data.pos = (0, 8)
            
            return ret_withdraw

    # 점유하는 것이 목표였다면...
    if data.state == 1:
        # 현재 칸이 점유되어 있지 않다면...
        if infos.publicPlane[infos.pos_me].r_toOccupy > 0:
            # 다음 번 행동부터 인출을 목표로 하기로 기록해 둠
            data.state = 0
            # 다음 번 의사 결정을 수행할 때 새 칸을 찾아야 한다고 기록해 둠
            data.pos = None
            
            return ret_occupy
        

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

