# siu bot 입니다

strength = 8
dex = 12
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
move = 7
teleport = 8

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
    
    # 초기쉼
    if infos.stamina <= 0:
        ret_wait    
    
    # 결정
    if data.state == decision :
        data.state = make_decision()
    
    # 가까운 거점으로
    if data.state == return_base :
        if data.pos == None :
            data.pos = find_neer_from_list(infos.pos_me, infos.pos_bases)
        if data.pos == infos.pos_me :
            data.state = decision
            return ret_wait
    
    # 수집하는 것이 목표였다면...
    if data.state == gather:
        if data.pos == None:
            neer_base = find_neer_from_list(infos.pos_me, infos.pos_bases)
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
            data.state = decision
            return ret_wait
                
        if infos.pos_me == data.pos:
            # 이번에 수집한 다음에 손이 가득 찰 예정이라면...
            if infos.r_carrying + infos.myPlane[infos.pos_me] >= infos.max_r_carrying:
                data.state = deposit
                data.pos = find_neer_from_list(infos.pos_me, infos.pos_bases)
            if infos.r_carrying + infos.myPlane[infos.pos_me] < infos.max_r_carrying:
                data.pos = None
            
            return ret_gather

    # 수납
    if data.state == deposit:
        if data.pos == None :
            data.pos = find_neer_from_list(infos.pos_me, infos.pos_bases)
        if infos.pos_me == data.pos:
            data.state = decision
            data.pos = None
            return ret_deposit
    
    # 점유
    if data.state == occupy :
        if data.pos == None or infos.publicPlane[data.pos].r_toOccupy == 0 :
            data.pos = find_to_occupy(infos.pos_me)
        if data.pos == infos.pos_me :
            data.state = decision
            data.pos = None
            return ret_occupy
    
    # 인출
    if data.state == withdraw :
        if data.pos == None :
            data.pos = find_neer_from_list_move(infos.pos_me, infos.pos_bases)
        if data.pos == infos.pos_me :
            data.pos = None
            data.state = decision
            return ret_withdraw
    
    # 거점건설
    if data.state == build_base :
        if data.pos == None :
            data.pos = find_to_buildbase(infos.pos_me)
        elif infos.publicPlane[data.pos].r_toBuildBase == 0 :
            data.pos 
        if data.pos == infos.pos_me :
            data.pos = None
            data.state = return_base
            return ret_build_base
    
    # 텔포건설
    if data.state == build_teleporter :
        if data.pos == None :
            data.pos = find_to_buildteleporter(infos.pos_me)
        if data.pos == infos.pos_me :
            data.pos = None
            data.state = return_base
            return ret_build_teleporter
    
    # 휴식
    if data.state == relax :
        return ret_wait

    # 이동
    
    # 텔레포터 판별 및 이용
    if (get_distance(infos.pos_me, data.pos) > get_move_distance(infos.pos_me, data.pos)) :
        neer_teleport = find_neer_from_list(infos.pos_me, infos.pos_teleporters)
        if infos.pos_me == neer_teleport :
            neer_teleport_from_end = find_neer_from_list(data.pos, infos.pos_teleporters)
            return ret_warp, neer_teleport_from_end[0], neer_teleport_from_end[1]
        x_distance = neer_teleport[0] - infos.pos_me[0]
        y_distance = neer_teleport[1] - infos.pos_me[1]
        if (abs(x_distance) > abs(y_distance)) :
            if (x_distance) < 0 :
                return ret_move, dir_left
            return ret_move, dir_right
        if (y_distance < 0) :
            return ret_move, dir_up
        return ret_move, dir_down
    
    # 그냥 이동
    x_distance = data.pos[0] - infos.pos_me[0]
    y_distance = data.pos[1] - infos.pos_me[1]

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
        

def find_to_occupy(pos, search_range) :
    if infos.publicPlane[pos].r_toOccupy != 0 :
        return pos
    distance = 1
    while distance < search_range :
        count_candidate = distance * 4
        x = pos[0] + distance
        y = pos[1]
        count_checked = 0
        while count_checked < count_candidate :
            # 해당 칸에 점유가 남았다면, 점유
            if infos.publicPlane[x,y].r_toOccupy != 0 :
                return (x,y)

            # 다음에 체크할 칸 좌표 계산
            count_checked = count_checked + 1
            phase = count_checked // distance
            offset = count_checked % distance

            x = pos[0] + (1 - (phase     & 2)) * (distance * (1 -  phase      % 2) - offset)
            y = pos[1] + (1 - (phase - 1 & 2)) * (distance * (1 - (phase - 1) % 2) - offset)

        distance = distance + 1
    return None


def find_to_buildbase(pos, search_range) :
    if infos.publicPlane[pos].r_toBuildBase > 0 and infos.publicPlane[pos].r_toBuildBase < get_original_base(pos) :
        return pos
    distance = 1
    while distance < search_range :
        count_candidate = distance * 4
        x = pos[0] + distance
        y = pos[1]
        count_checked = 0
        while count_checked < count_candidate :
            r_toBB = infos.publicPlane.r_toBuildBase

            if r_toBB > 0 and r_toBB < get_original_base((x,y)):
                return (x,y)

            count_checked = count_checked + 1
            phase = count_checked // distance
            offset = count_checked % distance
            x = pos[0] + (1 - (phase     & 2)) * (distance * (1 -  phase      % 2) - offset)
            y = pos[1] + (1 - (phase - 1 & 2)) * (distance * (1 - (phase - 1) % 2) - offset)

        distance = distance + 1
    return None

def find_new_buildbase(pos) :
    ch_avg = get_pos_average(infos.pos_characters)

def find_to_buildteleporter(pos) :
    return None

def find_neer_from_list(pos, point_list) :
    if point_list == [] :
        return pos
    ret = point_list[0]
    dis_min = get_distance(pos, ret)
    for l in point_list[1:] :
        dis_tmp = get_distance(pos, l)
        if dis_min > dis_tmp :
            ret = l
            dis_min = dis_tmp
    return ret

def find_neer_from_list_move(pos, point_list) :
    if point_list == [] :
        return pos
    ret = point_list[0]
    dis_min = get_move_distance(pos, ret)
    for l in point_list[1:] :
        dis_tmp = get_move_distance(pos, l)
        if dis_min > dis_tmp :
            ret = l
            dis_min = dis_tmp
    return ret

def search_quard_from_list(pos, lists) :
    ret = [0, 0, 0, 0]
    x = pos[0]
    y = pos[1]
    for element in lists :
        if element[0] >= x and element[1] > y :
            ret[0] += 1
        elif element[0] < x and element[1] >= y :
            ret[1] += 1
        elif element[0] <= x and element[1] < y :
            ret[2] += 1
        elif element[0] > x and element[1] <= y :
            ret[3] += 1
    return (ret.index(min(ret)), ret.index(max(ret)))

def make_decision() :
    # 내가 있는 곳이 거점이라면
    if infos.publicPlane[infos.pos_me].r_toBuildBase == 0 :
        if infos.stamina < infos.maxstamina :
            return relax
        if infos.r_carrying > 0 and infos.recent_action_me[0] != ret_withdraw :
            data.pos = infos.pos_me
            return deposit
        if infos.recent_actoin_me[0] == ret_withdraw :
            print()
            
        if infos.publicPlane[infos.pos_me].r_stored > infos.max_r_carrying // 2 and infos.r_carrying < infos.max_r_carrying :
            return withdraw
        else :
            return gather
    else :
        if infos.stamina < infos.max_stamina / 3 :
            return return_base
        if infos.r_carrying > (infos.max_r_carrying * 2) / 3 :
            return occupy
        else :
            return gather

def get_original_resource(pos) :
    return 5 + ((abs(pos[0]) + abs(pos[1])) >> 5)
def get_original_occupy(pos) :
    return int(25 * 1.6 ** ((abs(pos[0]) + abs(pos[1]))/512))
def get_original_base(pos) :
    return int(50 * 6.0 ** ((abs(pos[0]) + abs(pos[1]))/512))
def get_original_teleport(pos) :
    return int(100 * 1.5 ** ((abs(pos[0]) + abs(pos[1]))/512))

def get_distance(p1, p2) :
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_move_distance(p1, p2) :
    tel_for_start = find_neer_from_list(p1, infos.pos_teleporters)
    tel_for_end = find_neer_from_list(p2, infos.pos_teleporters)
    tel_distance = get_distance(p1, tel_for_start) + get_distance(p2, tel_for_end) + 1
    no_tel_distance = get_distance(p1, p2)
    if (tel_distance < no_tel_distance) :
        return tel_distance
    else :
        return no_tel_distance

def get_pos_average(lists) :
    avg = (0, 0)
    for e in lists :
        avg[0] += e[0]
        avg[1] += e[1]
    avg[0] /= len(lists)
    avg[1] /= len(lists)
    return avg

def get_pos_standard_deviation(lists, avg) :
    ret = (0, 0)
    for e in lists :
        ret[0] += abs(e[0] - avg[0]) ** 2
        ret[1] += abs(e[1] - avg[1]) ** 2
    ret[0] /= len(lists)
    ret[1] /= len(lists)
    return (ret[0]**(1/2) , ret[1]**(1/2))

def get_outsider(lists, avg, std_deviation) :
    if (std_deviation[0] < 5 and std_deviation[1] < 5) :
        return None
    ddd = []
    for e in lists :
        ddd.append(abs(e[0] - avg[0]) + abs(e[1] - avg[1]))
    return ddd.index(max(ddd))





# ☆ 이 아래에 있는 if문은 여러분이 이 파일 붙잡고 F5 눌렀을 때도 테스트를 진행해 볼 수 있도록 적어 두었어요
# - 과제를 진행할 때는 이 파일 붙잡고 F5 눌러 실행하면
#   나중에 게임이 종료/중단된 이후에도 interactive에서 각 이름들을 적어 가며 '마지막에 뭐 담겨 있었나'를 볼 수 있어요
if __name__ == '__main__':
    import hw4_core
    hw4_core.run()

