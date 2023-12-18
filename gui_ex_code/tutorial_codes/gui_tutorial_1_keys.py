'''
1. 키 입력을 다루는 방법 소개

- F5를 눌러 창을 띄운 다음 아무 키나 누르면
  interactive에 '어떤 키'를 방금 눌렀는지 / 떼었는지 알려줄 거예요
'''

import gui_core as gui


w = gui.Window('Escape 키를 누르면 종료해요', 400, 300, 1/60, True)


def initialize(timestamp):
    w.data.number = w.newOval(150, 100, 100, 100, '')

    w.data.colors_skill = ['black', 'blue', 'green', 'red']

    # initialize()에서는 키 입력을 받을 수 없어요.
    # 그렇기는 하지만, 원한다면 update()에서 어떤 키(들)을 사용할 것인지를 미리 준비해둘 수 있어요

    # Escape 키를 '종료' 키로 지정
    w.data.key_quit = 'Escape'

    # q, w, e, r 키를 '스킬 사용' 키로 지정
    w.data.keys_use_skill = ['q', 'w', 'e', 'r']
    


def update(timestamp):
    # w.keys '사전'에는 사용자가 각 키를 누르고 있는지 아닌지 여부가 담겨 있어요
    if w.keys[w.data.key_quit]:
        w.stop()
        return


    idx_skill = 0

    while idx_skill < len(w.data.keys_use_skill):
        key = w.data.keys_use_skill[idx_skill]
        color = w.data.colors_skill[idx_skill]
        
        if w.keys[key]:
            w.setTitle('키 입력 판정: ' + key + ' 키 누름')
            w.recolorObject(w.data.number, color)

            # 'break문'은 이 문장이 포함되어 있는 while문/for문의 실행을 중단해요.
            # - Code 흐름 측면에서 return문과 유사하게 동작하지만,
            #   return문과 달리 break문에는 Data 흐름과 관련한 효과는 없어요
            #   (그래서 그런지 키워드 break 적고 그냥 엔터 치면 break문 작성이 끝나요)
            break

        idx_skill = idx_skill + 1
    else:
        # 만약 break문을 실행함으로써 while문 전체 실행을 중단했다면,
        # 'while문의 else부분 내용물'에 해당하는 이 아래 문장들은 실행되지 않을 거예요
        # -> if문의 경우처럼 while부분 조건식 계산 결과값이 False에 준할 때만 실행돼요
        w.setTitle('Escape 키를 누르면 종료해요')
        w.recolorObject(w.data.number, '')
        


w.initialize = initialize
w.update = update

w.start()
