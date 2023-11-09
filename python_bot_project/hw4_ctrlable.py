'''
공학도를위한창의적컴퓨팅 과제#4

hw4_ctrlable.py

Version 0.5.4

미리 만들어 둔, 여러분이 interactive에서 키보드로 직접 조작해볼 수 있는 캐릭터입니다.
내 캐릭터를 만들기 전에 게임 구성 요소들을 구경해 보는 용도로 사용해 주세요.
- 특히, infos에 담겨 있는 각종 Data들을 어떻게 꺼내 다룰 수 있는지 구경해 보면 좋을 것 같아요
'''

# 내 캐릭터의 이름과 힘, 민첩, 체력 능력치를 지정합니다.
# - 이름은 자유롭게 지정할 수 있어요(동명이인이 나오지 않도록 개성 있는 이름을 골라 주세요)
# - 능력치는 모두 0 이상의 int 형식 값이어야 하며, 세 능력치의 합은 30이어야 해요
stats = ['직접_조작중인_내_캐릭터', 10, 10, 10]




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
    # 주의: 공유 평면에 대한 [ ] 수식은 매 번 계산할 때마다 원본 Data의 사본을 만들어 return해요.
    # - 따라서 미래에 비교 등에 사용하기 위해 이번에 얻은 Data를 어딘가에 담아 둘 수 있어요.
    # - 반면, 동일한 [ ] 수식을 여러 번 계산하면 그만큼 사본을 만들게 되어버려 의사 결정에 걸리는 현실 시간이 늘어날 수 있어요.
    #   따라서 아래와 같이, 일단 어딘가에 담아 두고 천천히 . 수식 적어 가며 사용하도록 구성하는 것을 추천해요
    #   (아래 할당문처럼 data.public_cell 같은 이름에다가 담도록 구성한 다음 F5 한 번 눌러주면
    #   그 이후부터는 IDLE이 무리 없이 자동 완성 기능을 제공해 줄 거예요)
    data.public_cell = infos.publicPlane[infos.pos_me]

    
    print()
    print('---------------- 의사 결정 시작')
    print('------------ data 내용물')
    if len(vars(data)):
        for name, value in vars(data).items():
            print(f'{name} = {value}')
    else:
        print('(하나도 없음. data.number = 3 엔터 와 같이 할당문을 적어 새로운 값을 담도록 구성할 수 있어요)')
    print()

    # ----------------------------------------------------
    # 이 아래에 적어둔 문장들을 통해 infos에 담겨 있는 다양한 Data들을 어떻게 사용할 수 있는지 구경해 볼 수 있을 거예요.
    # 주의: infos에 값을 담는 것은 core가 알아서 해 줄 예정이에요. 가급적이면 infos에 담겨 있는 값을 여러분이 직접 변경하지는 말아요.
    #       함부로 변경하면 오류가 발생하거나, 이후에 core가 더 이상 Data를 담아 주지 않게 될 가능성이 있어요.
    #       (백업해 두고 싶은 Data가 있다면 이름 data를 사용해 따로 담아 두면 돼요)
    print('------------ infos 내용물 요약 시작')
    print('--------내 캐릭터 관련 Data')
    print('능력치:', stats)
    print('(힘)들고 있는 자원량:', infos.r_carrying, '/', infos.max_r_carrying)
    print('(힘)이동 기력 소모량 감소 계수:', infos.coef_stamina_cost_reduction_after_move)
    print('(민)이동 후딜레이 계수:', infos.coef_delay_after_move)
    print('(민)작업 후딜레이 계수:', infos.coef_delay_after_work)
    print('(체)기력:', infos.stamina, '/', infos.max_stamina)
    print(f'(체)거점 없는/있는 칸에서 대기시 기력 회복량: {infos.coef_stamina_heal} / {infos.coef_stamina_heal_on_base}')
    print('마지막에 수행한 행동:', infos.recent_action_me)
    print()
    print('-------- 현재 칸 관련 Data')
    print('위치:', infos.pos_me)
    print('(개)자원량:', infos.myPlane[infos.pos_me])
    
    if data.public_cell.r_toOccupy > 0:
        print('(공)  칸 점유 완료까지 남은 자원량:', data.public_cell.r_toOccupy)
    else:
        print('(공)  칸 점유 완료. 이동 후딜레이 계수:', data.public_cell.coef_delay_after_move) # 점유 완료된 칸에서 다른 칸으로 이동/워프할 때 기본 후딜레이에 이 값을 곱해요
    if data.public_cell.r_toBuildBase > 0:
        print('(공)거점 건설 완료까지 남은 자원량:', data.public_cell.r_toBuildBase)
    else:
        print('(공)거점 건설 완료. 수납되어 있는 자원량:', data.public_cell.r_stored)
    if data.public_cell.r_toBuildTeleporter > 0:
        print('(공)텔포 건설 완료까지 남은 자원량:', data.public_cell.r_toBuildTeleporter)
    else:
        print('(공)텔포 건설 완료.')
    print()

    print('-------- 각종 위치 관련 Data')
    # 여기서는 위치 목록을 손쉽게 출력하기 위해 그 목록에 대한 list 형식 값을 만들어 출력하고 있는데,
    # for문이나 [ ] 연산자, len()을 사용할 때는 굳이 이럴 필요 없이 그냥 직접 infos.pos_bases[0] 과 같이 적을 수 있어요
    print('  캐릭터 위치 목록:', list(infos.pos_characters))
    print('    거점 위치 목록:', list(infos.pos_bases))
    print('텔레포터 위치 목록:', list(infos.pos_teleporters))
    print()
    
    print('-------- 요청 관련 Data')
    # infos.myRequest 에는 내가 마지막으로 게시한 요청 Data가 담겨 있어요(게시한 적 없다면 None이 담겨 있음)
    # infos.requests_active 에는, 게시되었고 아직 달성되지 않은 요청 Data들이 담겨 있어요
    # infos.requests_all 에는 이제까지 게시된 모든 요청 Data들이 담겨 있어요
    if len(infos.requests_all):
        print('---- 내 캐릭터가 게시한 요청')
        if infos.myRequest:
            print('일련번호:', infos.myRequest[0])
            print('대상 위치:', infos.myRequest[1])
            if infos.myRequest[2] == 0:
                print('내용: 주변 2칸 범위 안에서 자원', infos.myRequest[3], '개 수집')
            elif infos.myRequest[2] == 1:
                print('내용: 거점 건설 (자원', infos.myRequest[3], '개 어치)')
            elif infos.myRequest[2] == 2:
                print('내용: 텔레포터 건설 (자원', infos.myRequest[3], '개 어치)')
            if infos.request_isCompleted(infos.myRequest[0]):
                print('요청 달성까지 남은 자원량: 이미 달성됨')
            else:
                print('요청 달성까지 남은 자원량:', infos.request_getAmountOfResourcesToComplete(infos.myRequest[0]))
        else:
            print('없음')
        print('---- 내 캐릭터가 게시하지 않은 요청들')
        for request in infos.requests_all:
            if request != infos.myRequest:
                print(f'-- 요청#{request[0]}')
                print('대상 위치:', request[1])
                if request[2] == 0:
                    print('내용: 주변 2칸 범위 안에서 자원', request[3], '개 수집')
                elif request[2] == 1:
                    print('내용: 거점 건설 (자원', request[3], '개 어치)')
                elif request[2] == 2:
                    print('내용: 텔레포터 건설 (자원', request[3], '개 어치)')
                if infos.request_isCompleted(request[0]):
                    print('요청 달성까지 남은 자원량: 이미 달성됨')
                else:
                    print('요청 달성까지 남은 자원량:', infos.request_getAmountOfResourcesToComplete(request[0]))
    else:
        print('(하나도 없음)')
    print()

    # 항목이 너무 많아서 출력 안 하도록 막아 두었어요. 전부 출력해 보려면 아래에 있는 str literal 앞/뒤의 ''' 를 지우면 돼요
    # (출력해 보고 싶은 항목에 대한 문장만 복사해서 다른 곳에 붙여넣어 사용하는 게 더 나을 것 같아요)
    print('-------- (점수 Data를 출력하고 싶다면 .py 파일 내용을 확인해 주세요)')
    '''
    print('-------- 점수 Data')
    print('[0x00] - 수집 행동 수행 횟수:', infos.myScore[0x0])
    print('[0x01] - 이동 행동 수행 횟수:', infos.myScore[0x1])
    print('[0x02] - 점유 행동 수행 횟수:', infos.myScore[0x2])
    print('[0x03] - 거점 행동 수행 횟수:', infos.myScore[0x3])
    print('[0x04] - 텔포 행동 수행 횟수:', infos.myScore[0x4])
    print('[0x05] - 수납 행동 수행 횟수:', infos.myScore[0x5])
    print('[0x06] - 인출 행동 수행 횟수:', infos.myScore[0x6])
    print('[0x07] - 워프 행동 수행 횟수:', infos.myScore[0x7])
    print('[0x08] - 요청 행동 수행 횟수:', infos.myScore[0x8])
    print('[0x09] - 대기 행동 수행 횟수:', infos.myScore[0x9])
    print('[0x0a] - 유효하지 않은 의사 결정 수행 횟수:', infos.myScore[0xa])
    print('[0x0b] - 의사 결정 도중 오류 발생 횟수:', infos.myScore[0xb])
    print('[0x0c] - 총 의사 결정 횟수(MakeDecision() 호출 횟수):', infos.myScore[0xc])
    print('[0x0d] - 의사 결정에 사용한 총 시간(현실 시간 기준, 초 단위):', infos.myScore[0xd])
    print()
    print('[0x10] - 수집한 총 자원량:', infos.myScore[0x10])
    print('[0x11] - 이동 도착지와 중심 사이의 거리의 평균:', infos.myScore[0x11] / infos.myScore[0x1] if infos.myScore[0x1] > 0 else '아직 이동한 적 없음')
    print('[0x12] - 점유에 사용한 총 자원량:', infos.myScore[0x12])
    print('[0x13] - 거점 건설에 사용한 총 자원량:', infos.myScore[0x13])
    print('[0x14] - 텔레포터 건설에 사용한 총 자원량:', infos.myScore[0x14])
    print('[0x15] - 수납한 총 자원량:', infos.myScore[0x15])
    print('[0x16] - 인출한 총 자원량:', infos.myScore[0x16])
    print('[0x17] - 워프한 칸 수:', infos.myScore[0x17])
    print('[0x18] - 자신이 게시했고 달성된 요청 수:', infos.myScore[0x18])
    print('[0x19] - 대기를 통해 회복한 총 기력량:', infos.myScore[0x19])
    print()
    print('[0x1a] - 자신이 수집했고 점유에 사용된 총 자원량:', infos.myScore[0x1a])
    print('[0x1b] - 자신이 수집했고 거점 건설에 사용된 총 자원량:', infos.myScore[0x1b])
    print('[0x1c] - 자신이 수집했고 텔레포터 건설에 사용된 총 자원량:', infos.myScore[0x1c])
    print('[0x1d] - 칸 점유에 기여하여 다른 캐릭터의 이동/워프를 도와 얻은 점수(출발지에 대해 적용):', infos.myScore[0x1d])
    print('[0x1e] - 거점 건설에 기여하여 다른 캐릭터의 수납/인출/대기를 도와 얻은 점수:', infos.myScore[0x1e])
    print('[0x1f] - 텔레포터 건설에 기여하여 다른 캐릭터의 워프를 도와 얻은 점수(출발지/도착지 모두에 대해 적용):', infos.myScore[0x1f])
    print()
    print('[0x20] - 수집 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x20])
    print('[0x21] - 이동 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x21])
    print('[0x22] - 점유 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x22])
    print('[0x23] - 거점 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x23])
    print('[0x24] - 텔포 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x24])
    print('[0x25] - 수납 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x25])
    print('[0x26] - 인출 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x26])
    print('[0x27] - 워프 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x27])
    print('[0x28] - 요청 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x28])
    print('[0x29] - 대기 행동을 수행한 이후에 실제로 적용받은 후딜레이 합:', infos.myScore[0x29])
    print()
    print('[0x2a] - 점유된 칸에서 이동한 횟수:', infos.myScore[0x2a])
    print('[0x2b] - 점유된 칸에서 이동할 때 절약한 후딜레이 합(기력 부족으로 증가한 양은 고려 안 함):', infos.myScore[0x2b])
    print('[0x2c] - 점유된 칸에서 워프한 횟수:', infos.myScore[0x2c])
    print('[0x2d] - 점유된 칸에서 워프할 때 절약한 후딜레이 합(기력 부족으로 증가한 양은 고려 안 함):', infos.myScore[0x2d])
    print()
    print('[0x30] - 수집 요청 달성을 위해 수집한 총 자원량:', infos.myScore[0x30])
    print('[0x31] - 거점 건설 요청 달성을 위해 사용한 총 자원량:', infos.myScore[0x31])
    print('[0x32] - 텔레포터 건설 요청 달성을 위해 사용한 총 자원량:', infos.myScore[0x32])
    print()   
    print('[0x33] - (힘)자원을 들고 이동한 횟수:', infos.myScore[0x33])
    print('[0x34] - (힘)이동할 때 들고 있던 자원량 평균:', infos.myScore[0x34] / infos.myScore[0x1] if infos.myScore[0x1] > 0 else '아직 이동한 적 없음')
    print('[0x35] - (힘)이동할 때 추가로 소모한 기력 합:', infos.myScore[0x35])
    print('[0x36] - (힘)자원을 들고 워프한 횟수:', infos.myScore[0x36])
    print('[0x37] - (힘)워프할 때 들고 있던 자원량 평균:', infos.myScore[0x37] / infos.myScore[0x7] if infos.myScore[0x7] > 0 else '아직 워프한 적 없음')
    print('[0x38] - (힘)워프할 때 추가로 소모한 기력 합:', infos.myScore[0x38])
    print('[0x39] - (민)기력이 충분한 채로 점유/건설/수납한 횟수:', infos.myScore[0x39])
    print('[0x3a] - (민)기력이 충분한 채로 점유/건설/수납할 때 경과한 후딜레이 합:', infos.myScore[0x3a])
    print('[0x3b] - (민)기력이 충분한 채로 점유/건설/수납할 때 절약한 후딜레이 합:', infos.myScore[0x3b])
    print('[0x3c] - (민)기력이 충분한 채로 자원을 들지 않고 이동/워프한 횟수:', infos.myScore[0x3c])
    print('[0x3d] - (민)기력이 충분한 채로 자원을 들지 않고 이동/워프할 때 경과한 후딜레이 합(점유로 인해 감소한 양은 고려 안 함):', infos.myScore[0x3d])
    print('[0x3e] - (민)기력이 충분한 채로 자원을 들지 않고 이동/워프할 때 절약한 후딜레이 합(점유로 인해 감소한 양은 고려 안 함):', infos.myScore[0x3e])
    print('[0x3f] - (체)행동 종료 시점의 기력 평균:', infos.myScore[0x3f] / (infos.myScore[0xc] - 1) if infos.myScore[0xc] > 1 else '이번이 첫 의사 결정임')
    print('[0x40] - (체)기력 부족으로 후딜레이가 증가한 횟수:', infos.myScore[0x40])
    print('[0x41] - (체)기력 부족으로 증가한 후딜레이 합:', infos.myScore[0x41])
    '''
    print()
    

    print('-------- 기타 Data')
    # infos.idx_me 는 Core의 캐릭터 목록에서 내 캐릭터가 몇 번째인지를 나타내요.
    # - 여러분 입장에서는 사실 큰 의미 없는 값이기는 해요.
    #   내 .py 파일을 복사해서 여러 번 import하여 게임에 참여시키고 싶을 때
    #   각 캐릭터가 그래도 조금씩은 다르게 동작하도록 만들고 싶다면
    #   이 값을 사용하여 목표를 달성할 수 있어요
    print('내 캐릭터의 index:', infos.idx_me)
    print('게임에 참여중인 캐릭터 수:', infos.numberOfCharacters)
    print('각 캐릭터가 마지막에 수행한 행동 목록:', list(infos.recent_action_characters))
    print('현재 시각:', infos.current_time, '초')
    if infos.end_time > 10000.0:
        print('종료 예정 시각: (사실상 제한 없음)')
    else:
        print('종료 예정 시각:', infos.end_time, '초')
    print()
    print('------------ infos 내용물 요약 끝')
    print()
    





    # ----------------------------------------------------
    # 이 아래에 적어둔 문장들은 사용자 입력을 다루는 내용들이 담겨 있으니 굳이 구경하지 않아도 돼요.
    

    print('조작 방법')
    print('1. Return할 값(들)이 계산 결과값으로 나오는 수식을 적고 엔터 쳐서 의사 결정을 끝낼 수 있습니다.')
    print('2. 한 줄짜리 Python 문장을 적어서 직접 실행해볼 수 있습니다.')
    print('   (수식 적고 엔터 키 친 경우 계산 결과값을 출력해 줘요)')
    print('3. . 연산자를 적거나 Ctrl + Space를 눌러 가며 이름 목록을 구경할 수 있습니다.')
    print('예시:')
    print('    ret_ 적고 Ctrl + Space -> 각 행동을 선택하기 쉽도록 미리 마련해 둔 이름들 확인')
    print('    dir_ 또는 req 적고 Ctrl + Space -> 이동 또는 요청 게시 행동을 선택할 때 쓸만한 이름들 확인')
    print('    ret_gather 또는 0 적고 엔터 -> 의사 결정의 결과로 수집 행동을 선택(return 0 엔터 와 동일)')
    print('    infos.pos_me 엔터 -> 계산 결과값인, 내 캐릭터의 위치 좌표를 출력')
    print("    print('Hello, World!') 엔터 -> interactive에 Hello, World!를 출력")
    
    while True:
        choice = input('입력하세요>')

        if len(choice) == 0:
            continue

        tokens = choice.replace(',', ' ').split()
        if tokens[0] == 'return':
            result = eval(choice.replace('return', '', 1))
            print(f'return문을 적은 것 같아요. {result} 값을 의사 결정 결과로 return할께요.')
            print('(이 캐릭터를 조작할 때는 그냥 ret_move dir_up 엔터 같은 느낌으로 의사 결정을 수행할 수 있어요)')
            input('계속하려면 엔터 키를 쳐요>')
            return result
            

        if len(tokens) == 0:
            continue

        try:
            result = None
            
            match tokens[0]:
                case '0' | 'ret_gather':
                    if len(tokens) == 1:
                        print('수집 행동을 골랐습니다.')
                        input('계속하려면 엔터 키를 쳐요>')
                        result = ret_gather
                case '1' | 'ret_move':
                    if len(tokens) < 2:
                        print('주의: 이동 행동을 고르긴 했는데 어느 방향으로 이동할 것인지 안 정한 것 같아요.')
                        print('      ret_move dir_up 엔터 같은 느낌으로 값을 두 개 지정하면 돼요.')
                        result = False
                        continue
                    elif len(tokens) == 2:
                        direction = int(eval(tokens[1]))
                        match direction:
                            case 0:
                                print('이동 행동을 골랐습니다. 위 방향(y축 음수 방향)으로 이동합니다.')
                            case 1:
                                print('이동 행동을 골랐습니다. 왼쪽 방향(x축 음수 방향)으로 이동합니다.')
                            case 2:
                                print('이동 행동을 골랐습니다. 오른쪽 방향(x축 양수 방향)으로 이동합니다.')
                            case 3:
                                print('이동 행동을 골랐습니다. 아래 방향(y축 양수 방향)으로 이동합니다.')
                            case _:
                                print('이동 행동을 골랐습니다. 그러나 방향 값이 적절하지 않아서 유효하지 않은 의사 결정으로 간주될 예정입니다.')
                        input('계속하려면 엔터 키를 쳐요>')
                        result = ret_move, direction
                case '2' | 'ret_occupy':
                    if len(tokens) == 1:
                        print('점유 행동을 골랐습니다.')
                        input('계속하려면 엔터 키를 쳐요>')
                        result = ret_occupy
                case '3' | 'ret_build_base':
                    if len(tokens) == 1:
                        print('거점 건설 행동을 골랐습니다.')
                        input('계속하려면 엔터 키를 쳐요>')
                        result = ret_build_base
                case '4' | 'ret_build_teleporter':
                    if len(tokens) == 1:
                        print('텔레포터 건설 행동을 골랐습니다.')
                        input('계속하려면 엔터 키를 쳐요>')
                        result = ret_build_teleporter
                case '5' | 'ret_deposit':
                    if len(tokens) == 1:
                        print('수납 행동을 골랐습니다.')
                        input('계속하려면 엔터 키를 쳐요>')
                        result = ret_deposit
                case '6' | 'ret_withdraw':
                    if len(tokens) == 1:
                        print('인출 행동을 골랐습니다.')
                        input('계속하려면 엔터 키를 쳐요>')
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
                        print(f'워프 행동을 골랐습니다. ({x}, {y})로 워프합니다.')
                        input('계속하려면 엔터 키를 쳐요>')
                        result = ret_warp, x, y
                case '8' | 'ret_submit_request':
                     if len(tokens) < 2:
                        print('주의: 요청 게시 행동을 고르긴 했는데 어떤 종류의 요청을 게시할 것인지 안 정한 것 같아요.')
                        print('      ret_submit_request requestcode_gather 엔터 같은 느낌으로 값을 두 개 지정하면 돼요.')
                        result = False
                        continue
                     elif len(tokens) == 2:
                        requestcode = int(eval(tokens[1]))
                        match requestcode:
                            case 0:
                                print('요청 게시 행동을 골랐습니다. 현재 칸에 대한 수집 요청을 게시합니다.')
                            case 1:
                                print('요청 게시 행동을 골랐습니다. 현재 칸에 대한 거점 건설 요청을 게시합니다.')
                            case 2:
                                print('요청 게시 행동을 골랐습니다. 현재 칸에 대한 텔레포터 건설 요청을 게시합니다.')
                            case _:
                                print('요청 게시 행동을 골랐습니다. 그러나 요청 종류 값이 적절하지 않아서 유효하지 않은 의사 결정으로 간주될 예정입니다.')
                        input('계속하려면 엔터 키를 쳐요>')
                        result = ret_submit_request, requestcode
                case '9' | 'ret_wait':
                    if len(tokens) == 1:
                        print('대기 행동을 골랐습니다.')
                        input('계속하려면 엔터 키를 쳐요>')
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

