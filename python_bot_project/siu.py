# 수집과 점유가 목적인 봇 만들기

#   수집을 할지 인출을 할지 결정

strength = 10
dex = 10
stamina = 10



stats = ['siu', strength, dex, stamina]

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

return_base = 0
decision = 1
gather = 2
deposit = 3
withdraw = 4
occupy = 5
build_base = 5
build_teleporter = 5
relax = 6

data = 3
infos = 3


plane_info =[]
def print_plain() :
    plane_array = []
    size = 31
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

def Initialize():
    data.state = 0
    data.pos = (0, 0)


def MakeDecision():
    
    plane_info.append(print_plain())
    
    
    if data.state == decision :
        data.state = make_decision()
    
    if data.state == return_base :
        if data.pos == None :
            data.pos = find_neerest_from_list(infos.pos_bases)
        if data.pos == infos.pos_me :
            data.state = decision
            return ret_wait
    
    # 수집하는 것이 목표였다면...
    if data.state == gather:
        if data.pos == None:
            neer_base = find_neerest_from_list(infos.pos_bases)
            x_center = neer_base[0]
            y_center = neer_base[1]
            distance = 1

            while data.pos == None:
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

                distance = distance + 1
                
        if infos.pos_me == data.pos:
            # 이번에 수집한 다음에 손이 가득 찰 예정이라면...
            if infos.r_carrying + infos.myPlane[infos.pos_me] >= infos.max_r_carrying:
                # 다음 번 행동부터 (0, 0)의 거점에 수납하는 것을 목표로 하기로 기록해 둠
                data.state = deposit
                # NOTE 중심 칸이 아닌 다른 칸의 거점에 수납하고 싶다면 여기를 고치면 돼요.
                #      어느 거점으로 향할 것인지는, 위에 적혀 있는 '수집할 새 칸을 찾는 Code'를 참고해서 만들 수도 있지만,
                #      미리 infos.pos_bases에 거점이 있는 좌표 목록을 담아 두었으니, 이걸 털어보는 것을 추천해요
                data.pos = find_neerest_from_list(infos.pos_bases)
            # 이번에 수집해도 손이 가득 차지 않는다면...
            if infos.r_carrying + infos.myPlane[infos.pos_me] < infos.max_r_carrying:
                # 다음 번 의사 결정을 수행할 때 새 칸을 찾아야 한다고 기록해 둠
                data.pos = None
            
            return ret_gather

    # 수납하는 것이 목표였다면...
    if data.state == deposit:
        # 이미 지정한 칸에 도착해 있는 상태라면 수납
        if infos.pos_me == data.pos:
            # 다음 번 행동부터 수집하는 것을 목표로 하기로 기록해 둠
            data.state = decision
            # 다음 번 의사 결정을 수행할 때 새 칸을 찾아야 한다고 기록해 둠
            data.pos = None
            return ret_deposit
    
    if data.state == occupy :
        if data.pos == None :
            data.pos = find_to_occupy()
        else :
            if infos.publicPlane[data.pos].r_toOccupy == 0 :
                data.pos = None
                return ret_wait
        if data.pos == infos.pos_me :
            data.state = decision
            data.pos = None
            return ret_occupy
        
    if data.state == withdraw :
        if data.pos == None :
            data.pos = find_neerest_from_list(infos.pos_bases)
        if data.pos == infos.pos_me :
            data.pos = None
            data.state = occupy
            return ret_withdraw

    # 이동
    try :
        x_distance = data.pos[0] - infos.pos_me[0]
        y_distance = data.pos[1] - infos.pos_me[1]
    except :
        return ret_wait

    if x_distance == 0 and y_distance == 0 : 
        return ret_wait

    if abs(x_distance) > abs(y_distance):
        if x_distance < 0:
            return ret_move, dir_left
        return ret_move, dir_right

    if y_distance < 0:
        return ret_move, dir_up    
    return ret_move, dir_down



def find_neerest(value) :
    if value == 0 :
        distance = 0
        while distance < 5 :
            count_candidate = distance * 4
            x = infos.pos_me[0] + distance
            y = infos.pos_me[1]
            count_checked = 0
            while count_checked < count_candidate :
                # 해당 칸에 자원이 있다면 기록
                if infos.publicPlane[x,y].toBuildBase < get_original_base() or infos.publicPlane[x,y].toBuildTeleporter < get_original_teleport(x,y) :
                    return (x,y)

                # 3단 콤보-2-3. 다음에 체크할 칸 좌표 계산
                count_checked = count_checked + 1
                phase = count_checked // distance
                offset = count_checked % distance
                # distance == 2일 때 [+1, +1, +1, +1, -1, -1, -1, -1]과 [2, 1, 0 -1, 2, 1, 0 -1]을 각 자리별로 곱하는 셈이 돼요
                x = infos.pos_me[0] + (1 - (phase     & 2)) * (distance * (1 -  phase      % 2) - offset)
                # x버전 수식을 들고 와서 phase를 phase - 1로 고쳐 적었어요
                # (수식 1 - (phase - 1) % 2는 수식 phase % 2로 축약 가능하기는 해요)
                y = infos.pos_me[1] + (1 - (phase - 1 & 2)) * (distance * (1 - (phase - 1) % 2) - offset)

            # 3단 콤보-1-3. 한 칸 더 멀리 있는 칸들을 체크하기 시작
            distance = distance + 1
    else :
        distance = 0
        while distance < 5 :
            count_candidate = distance * 4
            x = infos.pos_me[0] + distance
            y = infos.pos_me[1]
            count_checked = 0
            while count_checked < count_candidate :
                # 해당 칸에 자원이 있다면 기록
                if infos.publicPlane[x,y].toBuildBase == 0 and value == 1 :
                    return (x,y)
                if infos.publicPlane[x,y].toBuildTeleporter == 0 and value == 2 :
                    return (x,y)

                # 3단 콤보-2-3. 다음에 체크할 칸 좌표 계산
                count_checked = count_checked + 1
                phase = count_checked // distance
                offset = count_checked % distance
                # distance == 2일 때 [+1, +1, +1, +1, -1, -1, -1, -1]과 [2, 1, 0 -1, 2, 1, 0 -1]을 각 자리별로 곱하는 셈이 돼요
                x = infos.pos_me[0] + (1 - (phase     & 2)) * (distance * (1 -  phase      % 2) - offset)
                # x버전 수식을 들고 와서 phase를 phase - 1로 고쳐 적었어요
                # (수식 1 - (phase - 1) % 2는 수식 phase % 2로 축약 가능하기는 해요)
                y = infos.pos_me[1] + (1 - (phase - 1 & 2)) * (distance * (1 - (phase - 1) % 2) - offset)

            # 3단 콤보-1-3. 한 칸 더 멀리 있는 칸들을 체크하기 시작
            distance = distance + 1
    return None
        

def find_to_occupy() :
    if infos.publicPlane[infos.pos_me].r_toOccupy != 0 :
        return infos.pos_me
    distance = 1
    while distance < 5 :
        count_candidate = distance * 4
        x = infos.pos_me[0] + distance
        y = infos.pos_me[1]
        count_checked = 0
        while count_checked < count_candidate :
            # 해당 칸에 자원이 있다면 기록
            if infos.publicPlane[x,y].r_toOccupy != 0 :
                return (x,y)

            # 3단 콤보-2-3. 다음에 체크할 칸 좌표 계산
            count_checked = count_checked + 1
            phase = count_checked // distance
            offset = count_checked % distance
            # distance == 2일 때 [+1, +1, +1, +1, -1, -1, -1, -1]과 [2, 1, 0 -1, 2, 1, 0 -1]을 각 자리별로 곱하는 셈이 돼요
            x = infos.pos_me[0] + (1 - (phase     & 2)) * (distance * (1 -  phase      % 2) - offset)
            # x버전 수식을 들고 와서 phase를 phase - 1로 고쳐 적었어요
            # (수식 1 - (phase - 1) % 2는 수식 phase % 2로 축약 가능하기는 해요)
            y = infos.pos_me[1] + (1 - (phase - 1 & 2)) * (distance * (1 - (phase - 1) % 2) - offset)

        # 3단 콤보-1-3. 한 칸 더 멀리 있는 칸들을 체크하기 시작
        distance = distance + 1

def find_neerest_from_list(point_list) :
    if point_list == [] :
        return (0, 0)
    ret = point_list[0]
    dis_min = abs(infos.pos_me[0] - ret[0]) + abs(infos.pos_me[1] - ret[1])
    for l in point_list[1:] :
        dis_tmp = abs(infos.pos_me[0] - l[0]) + abs(infos.pos_me[1] - l[1])
        if dis_min > dis_tmp :
            ret = l
            dis_min = dis_tmp
    return ret

def make_decision() :
    # 내가 있는 곳이 거점이라면 
    if infos.publicPlane[infos.pos_me].r_toBuildBase == 0 :
        if infos.r_carrying > 0 :
            return deposit
        #if infos.stamina < (stamina * 4) / 3 :
        #    return relax
        if infos.publicPlane[infos.pos_me].r_stored > 0 :
            return withdraw
        else :
            return gather
    else :
        #if infos.stamina < (stamina * 4) / 3 :
        #    return return_base
        if infos.r_carrying > (infos.max_r_carrying * 2) / 3 :
            return occupy
        else :
            return gather 

def get_original_resource(x, y) :
    return 5 + ((abs(x) + abs(y)) >> 5)
def get_original_occupy(x, y) :
    return int(25 * 1.6 ** ((abs(x) + abs(y))/512))
def get_original_base(x, y) :
    return int(50 * 6.0 ** ((abs(x) + abs(y))/512))
def get_original_teleport(x, y) :
    return int(100 * 1.5 ** ((abs(x) + abs(y))/512))




# ☆ 이 아래에 있는 if문은 여러분이 이 파일 붙잡고 F5 눌렀을 때도 테스트를 진행해 볼 수 있도록 적어 두었어요
# - 과제를 진행할 때는 이 파일 붙잡고 F5 눌러 실행하면
#   나중에 게임이 종료/중단된 이후에도 interactive에서 각 이름들을 적어 가며 '마지막에 뭐 담겨 있었나'를 볼 수 있어요
if __name__ == '__main__':
    import hw4_core
    hw4_core.run()

