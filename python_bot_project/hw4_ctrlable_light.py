'''
공학도를위한창의적컴퓨팅 과제#4

hw4_ctrlable_light.py

Version 0.5.4

여러분이 interactive에서 키보드로 직접 조작해볼 수 있는 캐릭터...의 '출력 덜 하는 버전'입니다.
print() 호출식이 덜 적혀 있다는 점을 빼면 hw4_ctrlable.py와 동등한 느낌으로 플레이할 수 있어요.
'''

# 내 캐릭터의 이름과 힘, 민첩, 체력 능력치를 지정합니다.
# - 이름은 자유롭게 지정할 수 있어요(동명이인이 나오지 않도록 개성 있는 이름을 골라 주세요)
# - 능력치는 모두 0 이상의 int 형식 값이어야 하며, 세 능력치의 합은 30이어야 해요
stats = ['나', 10, 10, 10]




# 이 모듈 안에서 사용할 수 있는 이름들입니다. 해당 의미를 띄는 값을 미리 담아 두도록 지정되어 있습니다.
# 이 이름들은 다른 파일에서 사용하지 않으므로, 원한다면 자신이 적기 쉬운 다른 이름들을 대신 도입해 다루어도 됩니다.

# 의사 결정 결과를 return할 때 사용할 수 있는 이름들
# 주의: 원래는 ret어쩌구 등재하는 할당문들도 자유롭게 고쳐 사용해도 되는데,
#       일단 이 아래에 있는 10줄은 그대로 두면 좋겠어요(편의를 위해 강사가 수작을 부려 둠)
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


# 내 캐릭터의 다음 행동을 결정하기 위한 의사 결정을 수행합니다.
def MakeDecision():
    # 여기서는 예시 느낌으로 적어 두기 위해 data의 이름 사전에 각 이름을 등재하고 있어요.
    # (여기 적힌 내용들 중에 data.어쩌구 하면서 수식 적어 가면서 사용하고 있는 부분들은 전부 여기 어딘가에 그 값을 실제로 담는 할당문이 있어요)
    # - 어떤 Data를 굳이 이번 의사 결정이 끝난 이후에도 담아 둘 필요가 없다면
    #   그냥 편하게 local 이름 등재해 가며 진행해도 무방해요.
    #   단, local 이름을 사용하면 IDLE이 자동 완성 기능을 원활히 제공할 수 없게 되니
    #   일단은 아래와 같이 data의 이름 사전을 적극적으로 이용하는 것을 권장해요
    data.r_onCell = infos.myPlane[infos.pos_me]
    data.cell_public = infos.publicPlane[infos.pos_me]

    print()
    print(f'{stats[0]}\'s info | Time: {infos.current_time:.3f} | Pos: {infos.pos_me} | R: {infos.r_carrying}/{infos.max_r_carrying} | St: {infos.stamina}/{infos.max_stamina}')
    print(f'Cell info | R(on myPlane): {data.r_onCell} | ', end='')
    if data.cell_public.r_toOccupy > 0:
        print(f'O: {data.cell_public.r_toOccupy} left, ', end='')
    else:
        print(f'O: x{data.cell_public.coef_delay_after_move:5.3f}, ', end='')

    if data.cell_public.r_toBuildBase > 0:
        print(f'B: {data.cell_public.r_toBuildBase} left, ', end='')
    else:
        print(f'B: {data.cell_public.r_stored} stored, ', end='')
        
    if data.cell_public.r_toBuildTeleporter > 0:
        print(f'T: {data.cell_public.r_toBuildTeleporter} left')
    else:
        print(f'T: Done')
        
    # 원한다면 여기에 별도의 print() 호출식(과 엔터)를 적어서 여러분이 매 의사 결정마다 보고 싶은 값들을 출력하도록 만들 수 있어요.
    # 예를 들어, 이번 튜토리얼 시나리오의 목표에 해당하는 요청을 달성하기 위해 자원이 얼마나 더 필요한지 보고 싶다면 아래 한 줄의 주석을 풀면 돼요:
    #print(infos.request_getAmountOfResourcesToComplete(infos.requests_active[0][0]))

    # ----------------------------------------------------
    # 이 아래에 적어둔 문장들은 사용자 입력을 다루는 내용들이 담겨 있으니 굳이 구경하지 않아도 돼요.
    
    while True:
        choice = input('>')

        if len(choice) == 0:
            continue

        tokens = choice.replace(',', ' ').split()
        if tokens[0] == 'return':
            result = eval(choice.replace('return', '', 1))
            return result
            

        if len(tokens) == 0:
            continue

        try:
            result = None
            
            match tokens[0]:
                case '0' | 'ret_gather':
                    if len(tokens) == 1:
                        result = ret_gather
                case '1' | 'ret_move':
                    if len(tokens) < 2:
                        print('주의: 이동 행동을 고르긴 했는데 어느 방향으로 이동할 것인지 안 정한 것 같아요.')
                        print('      ret_move dir_up 엔터 같은 느낌으로 값을 두 개 지정하면 돼요.')
                        result = False
                        continue
                    elif len(tokens) == 2:
                        direction = int(eval(tokens[1]))
                        result = ret_move, direction
                case '2' | 'ret_occupy':
                    if len(tokens) == 1:
                        result = ret_occupy
                case '3' | 'ret_build_base':
                    if len(tokens) == 1:
                        result = ret_build_base
                case '4' | 'ret_build_teleporter':
                    if len(tokens) == 1:
                        result = ret_build_teleporter
                case '5' | 'ret_deposit':
                    if len(tokens) == 1:
                        result = ret_deposit
                case '6' | 'ret_withdraw':
                    if len(tokens) == 1:
                        result = ret_withdraw
                case '7' | 'ret_warp':
                    if len(tokens) < 3:
                        print('주의: 워프 행동을 고르긴 했는데 어느 칸으로 워프할 것인지 안 정한 것 같아요.')
                        print(f'      ret_warp 0 0 엔터 같은 느낌으로 값을 세 개 지정하면 돼요.')
                        result = False
                        continue
                    elif len(tokens) == 3:
                        x = int(eval(tokens[1]))
                        y = int(eval(tokens[2]))
                        result = ret_warp, x, y
                case '8' | 'ret_submit_request':
                     if len(tokens) < 2:
                        print('주의: 요청 게시 행동을 고르긴 했는데 어떤 종류의 요청을 게시할 것인지 안 정한 것 같아요.')
                        print('      ret_submit_request requestcode_gather 엔터 같은 느낌으로 값을 두 개 지정하면 돼요.')
                        result = False
                        continue
                     elif len(tokens) == 2:
                        requestcode = int(eval(tokens[1]))
                        result = ret_submit_request, requestcode
                case '9' | 'ret_wait':
                    if len(tokens) == 1:
                        result = ret_wait
        finally:
            if result == None:
                try:
                    result = eval(choice)
                    if result != None:
                        print(result)
                except SyntaxError:
                    exec(choice)                
            elif result is not False:
                return result
            
    # 실행 흐름이 여기까지 올 일은 없기는 하지만 혹시 모르니 메시지를 출력하도록 만들어 둠
    print('혹시나 이 메시지를 봤다면 얼른 강사에게 알려주세요. 급함')
    return ret_wait

    

# ☆ 이 아래에 있는 if문은 여러분이 이 파일 붙잡고 F5 눌렀을 때도 테스트를 진행해 볼 수 있도록 적어 두었어요
# - 과제를 진행할 때는 이 파일 붙잡고 F5 눌러 실행하면
#   나중에 게임이 종료/중단된 이후에도 interactive에서 각 이름들을 적어 가며 '마지막에 뭐 담겨 있었나'를 볼 수 있어요
if __name__ == '__main__':
    import hw4_core
    hw4_core.run()

