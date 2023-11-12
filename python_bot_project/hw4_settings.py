'''
공학도를위한창의적컴퓨팅 과제#4

hw4_settings.py

Version 0.5.4

과제를 진행하는 도중에 직접 각종 설정들을 고쳐볼 수 있는 파일입니다.

아래에 나열된 할당문들을 구경해 보고, 필요한 경우 직접 고쳐 보세요.
(망했다 싶으면 압축 파일에 들어 있을 원본 파일로 다시 교체하면 돼요)

'''

# 게임의 모드를 지정합니다.
# 0: '본 게임'에 해당하는, 가장 기본적인 모드입니다.
#	- 초기 요청이 없는 상태로 시작합니다
#	- 게임 내 시계로 10,000초(약 세 시간) 동안 자유롭게 행동하고 그 결과를 토대로 과제 점수를 매깁니다
# 1: 튜토리얼 시나리오#1 - 수집 연습용
#	- 중심(0, 0) 주변 두 칸 범위 안에서 자원을 25만큼 수집해 달라는 요청이 게시되어 있습니다
#	- 제한 시간 없이, 요청을 달성할 때까지 진행됩니다
# 2: 튜토리얼 시나리오#2 - 점유 연습용
#	- 초기 요청이 없는 상태로 시작합니다
#	- 제한 시간 없이, (0, 1)부터 (0, 8)까지의 여덟 칸을 점유할 때까지 진행됩니다
# 3: 튜토리얼 시나리오#3 - 건설 연습용
#	- (4, 4) 자리의 칸에 거점을 건설해 달라는 요청이 게시되어 있습니다
#   - 중심 칸 거점에 매 초마다 1만큼의 자원이 자동 수납됩니다
#     (해당 자원은 0번째 캐릭터가 수집한 것으로 간주해요)
#	- 제한 시간 없이, 요청을 달성할 때까지 진행됩니다
# 4: 튜토리얼 시나리오#4 - 이동/워프 연습용
#	- 초기 요청이 없는 상태로 시작합니다
#	- 중심 칸, 그리고 x, y 각각 [-256, 255] 범위 안 정사각형 영역에 있는 '임의의' 칸에 텔레포터가 건설되어 있습니다
#   - x, y 각각 [-256, 255] 범위 안 정사각형 영역에 있는 모든 칸들에 대해 [0, 100] 범위의 '임의의' 양만큼 점유 기여량이 부여되어 있습니다
#	  (텔레포터 위치 및 칸별 점유 기여량을 변경하고 싶은 경우 이 아래에 있는 이름 seedForTest에 이전과 다른 값을 담도록 할당문을 고쳐 적어 주세요)
#	- 제한 시간 없이, 모든 캐릭터가 (255, -256)에 도착할 때까지 진행됩니다
# 5: 튜토리얼 시나리오#5 - 요청 게시 연습용
#	- 초기 요청이 없는 상태로 시작합니다
#	- (-64, -64) 자리의 칸에 대해 거점 건설 요청과 자원 수집 요청을 직접 게시해야 합니다
#	- 제한 시간 없이, 두 요청이 모두 달성될 때까지 진행합니다
#	- 주의: 이 시나리오는 캐릭터가 한 명만 있을 때는 (내가 직접 내 요청을 달성해야 하므로) 의미가 별로 없을 수도 있습니다.
#			'본 게임'에서 요청 게시는 굳이 모든 캐릭터가 다 하지는 않아도 무방하니 보통은 이 시나리오를 무시해도 됩니다.
#			그래도 해 보고 싶은 경우 위의 세 튜토리얼을 모두 통과한 캐릭터들을 추가로 투입(.py 파일 째로 복사해서 이름 바꾸고 저장한 다음 게임에 추가)한 다음 진행해 봐요
#   - 주의: 요청을 게시하지 않은 채 건설을 미리 끝내버리는 경우 그 시점부터 새 건설 요청을 게시할 수 없게 되므로 시나리오를 끝낼 수 없게 됩니다.
#           요청을 게시하려면 내 캐릭터가 해당 칸 위에 있어야 하므로, 자꾸 테스트가 끝나지 않는다면 내 캐릭터가 먼저 달려가서 빠르게 요청을 게시할 수 있도록 만들어 봐요
#
# TODO 향후 몇 가지 모드들이 더 추가될 수 있어요
mode = 2


# 각 시나리오에 대해 미리 만들어 둔 예시 캐릭터들을 자동으로 추가할 것인지 여부를 지정합니다.
# - 원한다면 직접 import문을 적어 수동으로 각 캐릭터를 추가할 수 있습니다.
#   그렇기는 하지만 어떤 예시 캐릭터들은 자신이 담당하는 시나리오의 목표를 달성하기 위해 구성되어 있으니
#   다른 mode에서는 정상적으로 동작하지 않을 수 있습니다
# TODO 예시 캐릭터는 나중에 더 추가될 수 있어요
add_yeshi_characters_forScenario = True


# 시나리오#4 에서 사용하는, 초기 텔레포터 위치를 결정하기 위한 값을 지정합니다.
# - None으로 지정하는 경우 현실 시각 값에 따라 위치가 결정됩니다(아마 매 실행마다 달라질 거예요)
# - 텔레포터 위치를 고정시켜 둔 채 게임을 여러 번 해 보고 싶다면 None 대신 적당한 int/float/str 형식 literal을 적어 두세요.
seed_forMode4 = None


# 어떤 캐릭터의 의사 결정 도중, 또는 의사 결정 유효성 체크 과정에서 문제가 생겼을 때 그와 관련한 내용을 interactive에 출력할 것인지를 지정합니다.
print_error_messages = True

# 어떤 캐릭터의 의사 결정 도중, 또는 의사 결정 유효성 체크 과정에서 문제가 생겼을 때 게임 진행을 일시 정지할 것인지 여부를 지정합니다. (해당 캐릭터에 대한 패널티 대기 행동을 수행하기 직전에 일시 정지합니다)
pause_after_error = True


# 게임에 참여할 캐릭터들(을 구성해 둔 모듈들)에 대한 import문을 여기에 적어 주세요.
# - 자신 또는 다른 친구가 적어 둔 다른 .py 파일을 import할 수 있어요
# - 직접 조작 가능한 캐릭터를 추가하고 싶을 때는 hw4_ctrlable 모듈을 import하면 돼요
# - 제출하기 전에 친구들이 만들어 둔 캐릭터들을 한데 모아 게임을 진행해 봐도 좋아요
# 주의: 동일한 모듈을 여러 번 import하면 안 돼요. 내 캐릭터의 사본을 함께 추가하고 싶다면 .py 파일 째로 복사해 놓고 각각 따로 import해 주세요.
#import hw4_ctrlable
#import hw4_yeshi_forMode1
import Jun

# (여기 있는 if문 내용물은 지우지 말고, 특정 캐릭터만 잠시 빼 두고 싶다면 주석으로 막아 두는 것을 권장해요)
# 튜토리얼 시나리오에 대한 예시 캐릭터들을 추가하는 Code예요.
# - 어떤 캐릭터 모듈들이 예시 용도로 준비되어 있는지 구경해 봐요
# - 예시 캐릭터들도 이 아래에서 '주목'할 캐릭터로 지정할 수 있어요
# TODO 예시 캐릭터는 나중에 더 추가될 수 있어요
if add_yeshi_characters_forScenario:
    if mode == 1:
        import hw4_yeshi_forMode1
    if mode == 2:
        # 수집가 셋 + 작업자 하나 조합
        # (파일 이름은 서로 다르지만 수집가 셋 모두 의사 결정 흐름이 동일해요)
        import hw4_yeshi_forMode1
        import hw4_yeshi_forMode2_gatherer_1
        import hw4_yeshi_forMode2_gatherer_2
        import hw4_yeshi_forMode2_worker
    if mode == 3:
        # 효율이 몹시 낮은 예시 캐릭터 둘을 마련해 두었어요.
        # 무작정 (4, 4)까지 이동한 다음 그 근처에서 직접 자원을 수집하며 건설에 참여해요
        import hw4_yeshi_forMode3_impatient
        # 중심 칸의 거점에 매 초마다 1씩 수납되는 자원을 인출해 가며 건설에 참여해요
        import hw4_yeshi_forMode3_lazy


# '주목'할 캐릭터를 지정합니다. 위의 import문을 통해 추가한 캐릭터(모듈)들 중 하나를 골라 지정할 수 있습니다.
# 지정된 캐릭터가 행동할 때마다 interactive에 관련 정보를 출력합니다.
# None으로 두는 경우 아무 캐릭터도 지정하지 않은 것으로 간주합니다.
# - 동시에 한 캐릭터만 주목할 수 있습니다. 여러 캐릭터에 대한 행동 정보를 확인하고 싶은 경우 아래의 print_log_for_all_characters를 True로 지정해 봐요
# - MakeDecision() 정의 내용물 적으면서 중간중간 print() 호출식을 적어서 여러분이 직접 적절한 시점에 적절한 메시지를 출력하도록 만들어도 돼요
#   (물론 제출하기 전에는 지워 놓고 제출해야 해요)
# 주의: 본 게임을 진행하는 경우 출력하는 내용이 너무 많아서 '렉'이 걸릴 수 있습니다.
focal_character = None

# (주목할 캐릭터를 포함하여) 모든 캐릭터들이 행동할 때마다 interactive에 관련 정보를 출력할 것인지를 지정합니다.
# 주의: 출력하면서 본 게임을 진행하는 경우 내용이 너무 많아서 IDLE이 '렉'걸릴 수 있습니다.
print_log_for_all_characters = False



# 게임 종료 이후 캐릭터별 점수를 파일에 저장할 것인지를 지정합니다.
# True로 지정하는 경우 .py 파일들이 있는 그 폴더에 result.csv 파일을 만들어 저장하게 됩니다.
# 주의: .csv 파일을 Excel 등으로 열어 두는 경우 저장에 실패해서 오류가 발생할 수 있어요.
#       복잡한 통계 처리를 해 보고 싶은 친구들은 일단 먼저 사본 파일을 만들어서 그거로 작업을 하는 것을 추천해요
export_result = True

# 게임 종료 이후 공유 평면 및 각 개인 평면들을 파일에 저장할 것인지를 지정합니다.
# True로 지정하는 경우 .py 파일들이 있는 그 폴더에 publicPlane.bmp, privatePlane#[idx].bmp 파일을 만들어 저장하게 됩니다.
export_planes = True

# 게임 종료 이후 interactive에 결과 요약 내용을 출력할 것인지를 지정합니다.
# 어떤 내용을 출력할 것인지는 mode 값에 따라 조금씩 다릅니다.
print_summarized_result = True






# -----------------------------------------------------------------------------------
# 이 아래에 적어 둔 내용은 고치면 안 돼요! (안 봐도 괜찮아요)

modules = []

def verify_settings():
    global focal_character

    # mode 값은 int 형식이어야 하며 [0, 5] 사이의 값이어야 함
    if 'mode' not in globals() or type(mode) != int or mode < -1 or mode > 5:
        e = ValueError('hw4_settings.mode 값은 0, 1, 2, 3, 4, 5 중 하나로 지정해야 해요.')
        raise e
    elif mode == -1:
        input('주의: 현재 hw4_settings.mode 값이 -1로 지정되어 있습니다.\n' +
              '내가 건드린 거 아닌데 이 메시지를 보고 있다면 강사가 실수한 것이니 얼른 연락해 주세요.\n' +
              '아무튼, hw4_settings.py를 열어 mode 값을 다른 것으로 지정한 다음 다시 실행하는 것을 권장합니다.\n' +
              '그래도 궁금하니 게임을 시작해 보고 싶다면 엔터 키를 입력하세요(Ctrl + C를 눌러 게임을 중단할 수 있습니다)>')
            
    # mode 값이 4인 경우 seed_forMode4 값은 None이거나, int/float/str 형식 중 하나여야 함
    if mode == 4 and ('seed_forMode4' not in globals() or seed_forMode4 != None and type(seed_forMode4) != int and type(seed_forMode4) != float and type(seed_forMode4) != str):
        e = TypeError('hw4_settings.seed_forMode4 값은 None이거나, 그 형식이 int/float/str 중 하나여야 해요.')
        raise e
    
    # print_error_messages 값은 bool 형식이어야 함
    if 'print_error_messages' not in globals() or type(print_error_messages) != bool:
        e = TypeError('hw4_settings.print_error_messages 값은 bool 형식 True 또는 False로 지정해야 해요.')
        raise e
    
    # import해 둔 캐릭터(모듈)들 종합
    obj = None
    import __main__ as main_module

    for name, obj in globals().items():
        if name == 'focal_character' or name == 'hw4_core' or name == '__builtins__':
            continue
        
        if type(obj) == type(main_module):
            
            # 중복 import 체크
            if obj in modules:
                e = ValueError(obj.__name__ + ' 모듈이 여러 번 import되었어요. 캐릭터의 사본을 함께 추가하고 싶은 경우 .py 파일 째로 복사해서 각각 따로 import해 주세요.')
                raise e

            # 캐릭터 유효성 체크
            if 'stats' not in vars(obj):
                e = NameError(obj.__name__ + ' 모듈 이름 사전에 이름 stats가 등재되어 있지 않아요. 캐릭터 능력치 정보를 잘 지정해 두어야 해요.')
                raise e

            if 'Initialize' not in vars(obj):
                e = NameError(obj.__name__ + ' 모듈 이름 사전에 이름 Initialize가 등재되어 있지 않아요. Data 초기화용 함수에 대한 함수 정의를 잘 적어 두어야 해요.')
                raise e

            if 'MakeDecision' not in vars(obj):
                e = NameError(obj.__name__ + ' 모듈 이름 사전에 이름 MakeDecision이 등재되어 있지 않아요. 의사 결정 함수에 대한 함수 정의를 잘 적어 두어야 해요.')
                raise e
            
            if (type(obj.stats) != list or len(obj.stats) != 4 or
                type(obj.stats[0]) != str or type(obj.stats[1]) != int or type(obj.stats[2]) != int or type(obj.stats[3]) != int or
                obj.stats[1] < 0 or obj.stats[2] < 0 or obj.stats[3] < 0 or 
                obj.stats[1] + obj.stats[2] + obj.stats[3] != 30 ):
                e = ValueError(obj.__name__ + ' 모듈의 능력치 정보가 유효하지 않아요. 네 칸짜리 list에 이름과 세 능력치를 각각 담아 두어야 하고, 각 능력치는 0 이상이어야 하고, 세 능력치의 합은 30이어야 해요.')
                raise e
            
            if not callable(obj.Initialize):
                e = ValueError(obj.__name__ + ' 모듈의 Data 초기화용 함수가 유효하지 않아요. 혹시나 MakeDecision = 3 엔터 같은 문장이 적혀 있지는 않은지 확인해 주세요.')
                raise e
            
            if obj.Initialize.__code__.co_argcount != 0:
                e = TypeError(obj.__name__ + ' 모듈의 Data 초기화용 함수가 유효하지 않아요. 인수를 하나도 받지 않도록 구성해 두어야 해요.')
                raise e

            if not callable(obj.MakeDecision):
                e = ValueError(obj.__name__ + ' 모듈의 의사 결정 함수가 유효하지 않아요. 혹시나 MakeDecision = 3 엔터 같은 문장이 적혀 있지는 않은지 확인해 주세요.')
                raise e
            
            if obj.MakeDecision.__code__.co_argcount != 0:
                e = TypeError(obj.__name__ + ' 모듈의 의사 결정 함수가 유효하지 않아요. 인수를 하나도 받지 않도록 구성해 두어야 해요.')
                raise e
            
            # 캐릭터 모듈 붙잡고 프로그램 실행 시작했는지 여부 체크(IDLE에서 모듈을 중복 import하기 때문에 교체 필요)
            if main_module.__file__ == obj.__file__:
                if focal_character == obj:
                    focal_character = main_module
                modules.append(main_module)
            else:
                modules.append(obj)
            
    # 캐릭터 모듈이 하나라도 있어야 됨
    if len(modules) == 0:
        e = ModuleNotFoundError('캐릭터가 하나도 추가되지 않았어요. hw4.settings.py에 적절한 import문을 적어서 게임에 참여할 캐릭터를 지정해 주세요.')
        raise e
    
    # focal_character 값은 None이거나 캐릭터 모듈들 중 하나여야 함
    if 'focal_character' not in globals() or (focal_character != None and focal_character not in modules):
        e = ValueError('hw4_settings.focal_character 값은 None이거나, 캐릭터 모듈들 중 하나를 골라 지정해야 해요.')
        raise e
    
    # print_log_for_all_characters 값은 bool 형식이어야 함
    if 'print_log_for_all_characters' not in globals() or type(print_log_for_all_characters) != bool:
        e = TypeError('hw4_settings.print_log_for_all_characters 값은 bool 형식 True 또는 False로 지정해야 해요.')
        raise e
    
    # export_result 값은 bool 형식이어야 함
    if 'export_result' not in globals() or type(export_result) != bool:
        e = TypeError('hw4_settings.export_result 값은 bool 형식 True 또는 False로 지정해야 해요.')
        raise e
    
    # export_planes 값은 bool 형식이어야 함
    if 'export_planes' not in globals() or type(export_planes) != bool:
        e = TypeError('hw4_settings.export_planes 값은 bool 형식 True 또는 False로 지정해야 해요.')
        raise e
    
    # print_summarized_result 값은 bool 형식이어야 함
    if 'print_summarized_result' not in globals() or type(print_summarized_result) != bool:
        e = TypeError('hw4_settings.print_summarized_result 값은 bool 형식 True 또는 False로 지정해야 해요.')
        raise e

    
verify_settings()


def print_plane_log() :
    for i in Jun.plane_info :
        print('===============================================')
        for j in i :
            for k in j :
                print(k, end=' ')
            print()
        print('===============================================')
        print()
        print()
        input()

if __name__ == '__main__':
    import hw4_core
    hw4_core.run()
    input('종료하려면 엔터 키를 입력하세요>')
    print_plane_log()