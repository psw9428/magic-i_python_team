'''
공학도를위한창의적컴퓨팅 과제#4

hw4_core.py

Version 0.5.4

게임의 무대가 되는 다중 평면 세계를 구성하기 위한 파일입니다.

주의:
    이 파일 내용은 절대로 고치면 안 됩니다!
    과제 제출 전에 다양한 테스트를 해 보고 싶다면 hw4_settings.py의 내용물을 확인해 주세요.
    
    굳이 이 파일 내용을 읽지 않아도 과제를 문제 없이 수행할 수 있습니다. 게임 관련 내용이 궁금한 경우 과제 설명서를 체크하거나 강사에게 문의해 주세요.
    - 한국어 주석을 적어 두기는 했는데 강사 본인이 코드 짜면서 참고할 목적으로 적어 두었어요
    - (진짜 주의)원활한 게임 진행을 위해 우리 수업 범위를 초과하는 요소들을 부득이 도입해 두기도 했어요. 괜히 스크롤 내렸다가 마음 아플 수 있으니 그냥 안 보는 것을 추천해요
    - 뭐 늘 그래왔기는 하지만, 여기 적혀 있는 모든 것들을 여러분이 사용할 수 있는 것은 아니에요. 그러니 더더욱 탐독할 필요 없을 듯
'''

def run():
    import time
    import collections # deque 형식을 사용하기 위해 import
    import traceback   # 오류 출력을 위해 import
    import sys         # 모듈 사용 여부 체크를 위해 import

    # hw4_settings.py 붙잡고 F5 눌렀는지 여부 체크
    import __main__
    if __main__.__file__.endswith('hw4_settings.py'):
        hw4_settings = __main__
    else:
        import hw4_settings
    del __main__

    # ---------------------------------------------------------------------------
    # 모듈 사용 여부 체크

    # hw4_settings 모듈은 최소 세 곳에서 사용됨: 이 함수(run()) 안, 시스템 전체 모듈 목록, sys.getrefcount() 내용물 안
    # IDLE의 경우 import 방식이 다르기 때문에 hw4_settings.py 붙잡고 F5 눌렀을 때는 체크 대상에서 제외함
    if hw4_settings.__name__ != '__main__' and sys.getrefcount(hw4_settings) > 3:
        print(sys.getrefcount(hw4_settings))
        print('주의:')
        print("여러분 코드 어딘가에 hw4_settings 모듈에 대한 import문이 적혀 있는 것 같아요. 제출한 코드에 이 import문이 있는 경우 큰 문제가 발생할 수 있으니, 얼른 지워 주세요. (굳이 그거 import하지 않아도 돼요. 본 게임'에서는 항상 과제 설명서에 적어 둔 설정 값들을 사용해서 게임을 진행해요. mode에 따라 서로 다른 Code를 실행하고 싶다면, 그냥 여러분 모듈 이름 사전에다 이름 mode를 직접 등재해 놓고 쓰다가 제출 직전에 0 담도록 고치고 내면 돼요)")
        return
    
    for module in hw4_settings.modules:
        # 각 캐릭터 모듈들은 최소 다섯 곳에서 사용: 이 함수(run()) 안, 시스템 전체 모듈 목록, hw4_settings 모듈 안, hw4_settings.modules,  sys.getrefcount() 내용물 안
        count = sys.getrefcount(module)

        # 주목할 캐릭터로 지정한 경우 1회 추가(미리 빼 둠)
        count -= module == hw4_settings.focal_character
        
        # IDLE의 경우 import 방식이 다르기 때문에 '붙잡고 실행중인 그 모듈은 추가로 두 곳에서 사용하는 것으로 판정됨 -> 그 모듈은 체크하지 않음
        # 어차피 본 게임에서는 core 잡고 실행할 예정이니 예외로 두어도 별 상관 없을 듯
        if module.__name__ != '__main__' and count > 5:
            print('주의: ' + module.__name__ + ' 모듈이 여러 곳에서 사용되고 있어요. 다른 캐릭터 또는 내 캐릭터 자체에 대한 import문을 적으면 안 돼요. 제출한 코드에 그런 import문이 있는 경우 큰 문제가 발생할 수 있으니, 얼른 지워 주세요. (여기서 검사하고 있지는 않지만, 강사가 직접 모든 .py 파일들을 열어서 이상한 내용이 있는지 확인할 예정이니 고인물 친구들은 제 3의 Data 흐름을 유발하지 말고 정갈하게 게임에 참여해 봅시다)')
    
    # ---------------------------------------------------------------------------
    # 내부 Data 준비

    # 캐릭터별 기여도를 집계하기 위한 형식(아직 기여한 적 없다면 0만큼 기여한 것으로 간주)        
    class ContributionInfo(dict):
        def __missing__(self, idx_contributor):
            self[idx_contributor] = 0
            return 0
        
    # 모듈 외부에서의 부적절한 접근을 막기 위한 이름
    isPermissionGranted = True

    # 캐릭터 목록
    characters = list(hw4_settings.modules)
    len_characters = len(characters)

    # 개인 평면 목록
    planes_private = []
    
    # 거점/텔레포터 목록
    pos_bases = [(0, 0)]
    pos_teleporters = []

    # 공유 평면(생성은 나중에 함)
    plane_public = None

    # 캐릭터 정보 목록
    character_infos = []
    pos_characters = [(0, 0)] * len_characters
    idx_focal_character = -1
    last_pos_character_forLog = (0, 0)
    recent_action_characters = [(9, )] * len_characters
    # 숫자 하나만 return하여 의사 결정을 수행하는 행동들 + 이동/요청 게시 행동에 대해 미리 만들어 둔 tuple 목록
    # [10] ~ [13]: 이동 행동을 표현하기 위한 tuple들
    # [14] ~ [16]: 요청 게시 행동을 표현하기 위한 tuple들
    # - 워프 행동을 표현할 때는 항상 새 tuple을 만들어서 사용함
    obj_actions = [(0,), None, (2,), (3,), (4,), (5,), (6,), None, None, (9,),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (8, 0), (8, 1), (8, 2)]

    # 점수 정보 목록
    scores = []

    # 요청 목록
    number_nextRequest = 0
    request_progression_nil = [True, 0, ContributionInfo(), -1]

    requests_active = []
    requests_all = []
    request_progressions = dict()
    request_progressions_perCharacter = [request_progression_nil] * len_characters
    request_progression_forScenario = request_progression_nil


    # 행동 순서 관련
    initiative_order = []
    initiative_maximal_sorted = 0.0
    idx_initiative_order_first = 0

    # 시간 관련
    current_time = 0.0
    end_time = 1e300
    start_realtime = 0.0
    end_realtime = 0.0
    last_time_seconds_forScenario = 0
    
    # Log 출력 관련
    text_actions = ['수집', '이동', '점유', '거점', '텔포', '수납', '인출', '워프', '요청', '대기', '무효', '오류']

    # 개인 평면의 특정 칸에 놓여 있는 자원의 양    
    def getAmountOfResourcesOn(x, y):
        return 5 + ((abs(x) + abs(y)) >> 5)

    # 공유 평면의 특정 칸을 점유하기 위해 필요한 자원량
    def getRequiredResourcesToOccupy(x, y):
        return int(25 * 1.6 ** ((abs(x) + abs(y))/512))

    # 공유 평면의 특정 칸에 거점을 건설하기 위해 필요한 자원량
    def getRequiredResourcesToBuildBaseOn(x, y):
        return int(50 * 6.0 ** ((abs(x) + abs(y))/512))

    # 공유 평면의 특정 칸에 텔레포터를 건설하기 위해 필요한 자원량
    def getRequiredResourcesToBuildTeleporterOn(x, y):
        return int(100 * 1.5 ** ((abs(x) + abs(y))/512))

    # 공유 평면 확장을 위한 함수
    def makeNewPublicChunk(column_chunks, row_chunks):
        result = []

        for y in range(row_chunks * 64, (row_chunks + 1) * 64):
            for x in range(column_chunks * 64, (column_chunks + 1) * 64):
                newCell = [0, collections.deque(),
                           getRequiredResourcesToOccupy(x, y), ContributionInfo(),
                           getRequiredResourcesToBuildBaseOn(x, y), ContributionInfo(),
                           getRequiredResourcesToBuildTeleporterOn(x, y), ContributionInfo(),
                           0, 0, 1.0, 0]
                newCell[11] = newCell[2]
            
                result.append(newCell)

        return result
    
    # 개인 평면 하나를 다루기 위한 형식
    class PrivatePlane:
        # 개인 평면은 64x64 chunk들의 dict로 관리
        # 각 chunk는 64x64 bits(512 Bytes)의 bytearray로 구성되며 특정 비트가 1인 경우 해당 칸의 자원을 수집한 적이 있음을 나타냄
        # 자원을 일부만 수집한 칸들을 별도 dict로 관리(일부만 수집한 칸도 chunk의 해당 비트는 이미 1)
        def __init__(self):
            self.chunks = dict()
            self.cells_partiallyGathered = dict()
        
        def __getitem__(self, pos):
            # 이전에 해당 칸의 자원을 일부만 수집했다면 남은 자원량을 그대로 return
            if pos in self.cells_partiallyGathered:
                return self.cells_partiallyGathered[pos]
            
            pos_chunkwise = (pos[0] // 64, pos[1] // 64)
            
            # 해당 chunk를 생성한 적이 없다면 수집한 적 역시 없을 것이므로 초기 자원량을 계산해 return
            if pos_chunkwise not in self.chunks:
                return getAmountOfResourcesOn(pos[0], pos[1])
            
            # chunk에 기록된 비트 확인. 1인 경우 자원이 없음을 의미하므로 0을 return
            if self.chunks[pos_chunkwise][pos[0] % 64 * 8 + pos[1] % 64 // 8] & (1 << (pos[1] % 8)):
                return 0
            
            # 자원이 모두 남아 있음을 의미하므로 초기 자원량을 계산해 return
            return getAmountOfResourcesOn(pos[0], pos[1])
        
        def __setitem__(self, pos, value):
            # (자원을 아예 수집하지 않은 경우에는 호출하지 않도록 구성해야 함)

            # 이번에 자원을 모두 수집한 경우
            if value == 0:
                # 이전에 해당 칸의 자원을 일부만 수집했다면 남은 자원량 정보 제거
                if pos in self.cells_partiallyGathered:
                    self.cells_partiallyGathered.pop(pos)
                    return
                
                pos_chunkwise = (pos[0] // 64, pos[1] // 64)

                # 해당 chunk를 생성한 적이 없다면 지금 생성
                if pos_chunkwise not in self.chunks:
                    self.chunks[pos_chunkwise] = bytearray(512)
                
                # 해당 칸에 대한 비트를 1로 지정
                self.chunks[pos_chunkwise][pos[0] % 64 * 8 + pos[1] % 64 // 8] |= (1 << (pos[1] % 8))
                return

            # 이번에 해당 칸의 자원을 처음 수집했지만 일부만 수집한 경우
            if pos not in self.cells_partiallyGathered:
                pos_chunkwise = (pos[0] // 64, pos[1] // 64)
                
                # 해당 chunk를 생성한 적이 없다면 지금 생성
                if pos_chunkwise not in self.chunks:
                    self.chunks[pos_chunkwise] = bytearray(512)
                
                # 해당 칸에 대한 비트를 1로 지정
                self.chunks[pos_chunkwise][pos[0] % 64 * 8 + pos[1] % 64 // 8] |= (1 << (pos[1] % 8))
                
            # 남은 자원량 정보 갱신
            self.cells_partiallyGathered[pos] = value
    
    # 공유 평면을 다루기 위한 형식
    class PublicChunks(dict):
        def __missing__(self, pos):
            newChunk = makeNewPublicChunk(pos[0], pos[1])
            self[pos] = newChunk
            return newChunk


    # 캐릭터별 개인 평면 생성
    for _ in characters:
        planes_private.append(PrivatePlane())


    # 공유 평면 생성 + 공유 평면에 중심 주변 chunk 네 개 추가 + (0, 0)을 점유 + (0, 0)에 거점 추가 + (0, 0)에 있는 캐릭터 수 지정
    newChunk = makeNewPublicChunk(0, 0)
    newChunk[0][2] = 0
    newChunk[0][4] = 0
    newChunk[0][8] = len_characters
    newChunk[0][9] = getRequiredResourcesToOccupy(0, 0)
    newChunk[0][10] = 0.75
    
    plane_public = PublicChunks()
    plane_public[-1, -1] = makeNewPublicChunk(-1, -1)
    plane_public[ 0, -1] = makeNewPublicChunk( 0, -1)
    plane_public[-1,  0] = makeNewPublicChunk(-1,  0)
    plane_public[ 0,  0] = newChunk


    # 캐릭터 정보 생성(모듈에서 이름과 능력치 복사한 다음 2차 능력치 지정) + 점수 정보 생성 + 첫 행동 순서 결정
    idx_character = 0
    temp = []
    
    for character in characters:
        if character == hw4_settings.focal_character:
            idx_focal_character = idx_character
            
        newInfo = list(character.stats)

        # 2차 능력치 지정
        # 들 수 있는 자원 최대량
        newInfo.append(newInfo[1])

        # 이동, 워프 기력 소모량 감소 계수
        newInfo.append(newInfo[1] >> 1)

        # 이동, 워프 후딜레이 감소 계수
        newInfo.append(0.9 ** newInfo[2])
        # TODO 계수 조절
        # 점유, 건설 후딜레이 감소 계수
        newInfo.append(0.75 ** newInfo[2])

        # 현재 기력
        newInfo.append(newInfo[3] * 4)
        
        # 기력 최대량
        newInfo.append(newInfo[3] * 4)

        # 기본 기력 회복량 계수
        newInfo.append(newInfo[9] >> 2)

        # 거점 기력 회복량 계수
        newInfo.append(newInfo[9] >> 1)

        # 들고 있는 자원의 총량
        newInfo.append(0)
        
        # 들고 있는 자원들 정보
        newInfo.append(collections.deque())
        
        character_infos.append(newInfo)

        scores.append([0] * 0x42)

        # 민첩 높은 캐릭터, 동일하면 먼저 제출된 캐릭터가 먼저 행동
        temp.append((-newInfo[2], idx_character))
        
        idx_character += 1

    temp.sort()
    for elem in temp:
        initiative_order.append([0.0, elem[1]])

    
    # MakeDecision()에서 각 Data들에 액세스하기 위한 요소들 준비

    def makeNewDataObject():
        class Data:
            '''여러분이 자유롭게 새 이름을 등재해 가며 Data를 담아 둘 수 있게 해 주는 형식이에요.
            data.number = 3 엔터 와 같이 할당문을 적어 가며 사용할 수 있어요.
            - 이렇게 담아 둔 Data는 이번 MakeDecision() 내용물 실행이 끝난 이후에도 계속 남아 있어요 '''
            def __str__(self):
                return '<아무 이름이나 등재해 둘 수 있는 무언가 | 사용 예: data.number = 3 엔터>'
        return Data()
    
    def makeNewInfosObject(idx_character):
        class MyPlane_View:
            def __init__(self):
                '주의: 여러분이 직접 새 MyPlane_View 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 MyPlane_View 형식 값을 만들 수는 없어요.')
                    raise e
                  
            def __len__(self):
                e = TypeError('평면의 칸 수는 한도 끝도 없이 늘어날 수 있어요. 그래서 len(infos.myPlane)을 계산 못 하도록 막아 두었어요.')
                raise e
            
            def __getitem__(self, pos):
                try:
                    return planes_private[idx_character][pos]
                except:
                    e = KeyError('개인 평면을 다루다가 오류가 났어요. 평면의 칸 수는 한도 끝도 없이 늘어날 수 있어서 for문을 사용해서 개인 평면에서 하나씩 꺼내올 수 없도록 막아 두었어요. 만약 내 개인 평면 위 (3, 5)에 있는 자원의 수를 얻고 싶다면 수식 infos.myPlane[3, 5] 를 적으면 돼요.')
                    raise e from None

            def __str__(self):
                return '<개인 평면 정보 | 사용 예: infos.myPlane[3, 5]>'
        
        class PublicCell_View:
            def __init__(self, x, y):
                self.pos = x, y
                pos_chunkwise = (x // 64, y // 64)
                
                if pos_chunkwise in plane_public:
                    cell_public = plane_public[pos_chunkwise][y % 64 * 64 + x % 64]
                    # Data를 읽은 시각
                    self.time_read = current_time
                
                    # 거점에 수납되어 있는 자원의 양
                    self.r_stored = cell_public[0]
                
                    # 점유 완료까지 필요한 자원의 양(0인 경우 점유 완료)
                    self.r_toOccupy = cell_public[2]
                
                    # 거점 건설 완료까지 필요한 자원의 양(0인 경우 건설 완료)
                    self.r_toBuildBase = cell_public[4]
                
                    # 텔레포터 건설 완료까지 필요한 자원의 양(0인 경우 건설 완료)
                    self.r_toBuildTeleporter = cell_public[6]
                
                    # 해당 칸에 캐릭터가 몇 명 있는지
                    self.count_characters = cell_public[8]
                
                    # 해당 칸에서 다른 칸으로 이동/워프할 때의 후딜레이 감소량
                    self.coef_delay_after_move = cell_public[10]
                else:
                    # Data를 읽은 시각
                    self.time_read = current_time
                
                    # 거점에 수납되어 있는 자원의 양
                    self.r_stored = 0
                
                    # 점유 완료까지 필요한 자원의 양(0인 경우 점유 완료)
                    self.r_toOccupy = getRequiredResourcesToOccupy(x, y)
                
                    # 거점 건설 완료까지 필요한 자원의 양(0인 경우 건설 완료)
                    self.r_toBuildBase = getRequiredResourcesToBuildBaseOn(x, y)
                
                    # 텔레포터 건설 완료까지 필요한 자원의 양(0인 경우 건설 완료)
                    self.r_toBuildTeleporter = getRequiredResourcesToBuildTeleporterOn(x, y)
                
                    # 해당 칸에 캐릭터가 몇 명 있는지
                    self.count_characters = 0
                
                    # 해당 칸에서 다른 칸으로 이동/워프할 때의 후딜레이 감소량
                    self.coef_delay_after_move = 1.0

            def __str__(self):
                return f'<{self.time_read:.3f}초 기준 공유 평면 위 {self.pos} 칸 정보 | . 수식 적어 사용>'

        class PublicPlane_View:
            def __init__(self):
                '주의: 여러분이 직접 새 PublicPlane_View 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 PublicPlane_View 형식 값을 만들 수는 없어요.')
                    raise e
                  
            def __len__(self):
                e = TypeError('평면의 칸 수는 한도 끝도 없이 늘어날 수 있어요. 그래서 len(infos.publicPlane)을 계산 못 하도록 막아 두었어요.')
                raise e
           
            def __getitem__(self, pos):
                try:
                    return PublicCell_View(pos[0], pos[1])
                except:
                    e = KeyError('공유 평면을 다루다가 오류가 났어요. 평면의 칸 수는 한도 끝도 없이 늘어날 수 있어서 for문을 사용해서 공유 평면에서 하나씩 꺼내올 수 없도록 막아 두었어요. 만약 공유 평면 위 (3, 5)에 대한 Data를 얻고 싶다면 수식 infos.publicPlane[3, 5] 를 적으면 돼요.')
                    raise e from None
                
            def __str__(self):
                return '<공유 평면 정보 | 사용 예: infos.publicPlane[3, 5]>'

        class Pos_Characters_View:
            def __init__(self):
                '주의: 여러분이 직접 새 Pos_Characters_View 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 Pos_Characters_View 형식 값을 만들 수는 없어요.')
                    raise e
                 
            def __len__(self):
                return len_characters
           
            def __getitem__(self, idx_character):
                return pos_characters[idx_character]
                
            def __str__(self):
                return '<캐릭터들 위치 목록 | for문 적어 사용 추천>'

        class Recent_Action_Characters_View:
            def __init__(self):
                '주의: 여러분이 직접 새 Recent_Action_Characters_View 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 Recent_Action_Characters_View 형식 값을 만들 수는 없어요.')
                    raise e
                
            def __len__(self):
                return len_characters
            
            def __getitem__(self, idx_request):
                return recent_action_characters[idx_request]

            def __str__(self):
                return '<캐릭터들 최근 행동 목록 | for문 적어 사용 추천>'
        
        class Pos_Bases_View:
            def __init__(self):
                '주의: 여러분이 직접 새 Pos_Bases_View 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 Pos_Bases_View 형식 값을 만들 수는 없어요.')
                    raise e
                 
            def __len__(self):
                return len(pos_bases)
           
            def __getitem__(self, idx_base):
                return pos_bases[idx_base]
                
            def __str__(self):
                return '<거점들 위치 목록 | for문 적어 사용 추천>'
        
        class Pos_Teleporters_View:
            def __init__(self):
                '주의: 여러분이 직접 새 Pos_Teleporters_View 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 Pos_Teleporters_View 형식 값을 만들 수는 없어요.')
                    raise e
                 
            def __len__(self):
                return len(pos_teleporters)
           
            def __getitem__(self, idx_teleporter):
                return pos_teleporters[idx_teleporter]
                
            def __str__(self):
                return '<텔레포터들 위치 목록 | for문 적어 사용 추천>'
            
        class Score_View:
            def __init__(self):
                '주의: 여러분이 직접 새 Score_View 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 Score_View 형식 값을 만들 수는 없어요.')
                    raise e
                
            def __len__(self):
                return len(scores[idx_character])
                
            def __getitem__(self, idx_score):
                return scores[idx_character][idx_score]
                
            def __str__(self):
                return '<점수 목록 | [ ] 수식 적어 사용(index별 의미는 설명서 참조)>'

        class Requests_Active_View:
            def __init__(self):
                '주의: 여러분이 직접 새 Requests_Active_View 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 Requests_Active_View 형식 값을 만들 수는 없어요.')
                    raise e
                
            def __len__(self):
                return len(requests_active)
            
            def __getitem__(self, idx_request):
                return requests_active[idx_request]

            def __str__(self):
                return '<유효한 요청 목록 | for문 적어 사용 추천>'
        
        class Requests_All_View:
            def __init__(self):
                '주의: 여러분이 직접 새 Requests_All_View 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 Requests_All_View 형식 값을 만들 수는 없어요.')
                    raise e
                
            def __len__(self):
                return len(requests_all)
            
            def __getitem__(self, idx_request):
                return requests_all[idx_request]

            def __str__(self):
                return '<모든 요청 목록 | for문 적어 사용 추천>'
            

        class Infos:
            def __init__(self):
                '주의: 여러분이 직접 새 Infos 형식 값을 만들 수는 없어요.'
                if not isPermissionGranted:
                    e = PermissionError('여러분이 직접 새 Infos 형식 값을 만들 수는 없어요.')
                    raise e
                character_info = character_infos[idx_character]
                self.idx_me = idx_character
                self.max_r_carrying = character_info[4]
                self.coef_stamina_cost_reduction_after_move = character_info[5]
                self.coef_delay_after_move = character_info[6]
                self.coef_delay_after_work = character_info[7]
                self.coef_stamina_heal = character_info[10]
                self.coef_stamina_heal_on_base = character_info[11]
                self.max_stamina = character_info[9]
                self.end_time = end_time
                self.pos_characters = Pos_Characters_View()
                self.recent_action_characters = Recent_Action_Characters_View()
                self.numberOfCharacters = len_characters
                self.pos_bases = Pos_Bases_View()
                self.pos_teleporters = Pos_Teleporters_View()
                self.myPlane = MyPlane_View()
                self.publicPlane = PublicPlane_View()
                self.myScore = Score_View()
                self.requests_active = Requests_Active_View()
                self.requests_all = Requests_All_View()
                self.myRequest = None

                self.current_time = 0.0
                self.pos_me = (0, 0)
                self.recent_action_me = obj_actions[9]
                self.stamina = 0
                self.r_carrying = 0
            
            def request_isCompleted(self, number_request):
                '''요청 정보 tuple의 0번째 자리에 담긴 요청별 일련번호를 인수로 받는 함수입니다.
                해당 요청이 이미 달성되었는지 여부를 return합니다.'''
                return request_progressions[number_request][0]
                
            def request_getAmountOfResourcesToComplete(self, number_request):
                '''요청 정보 tuple의 0번째 자리에 담긴 요청별 일련번호를 인수로 받는 함수입니다.
                해당 요청에 대해 달성까지 남은 자원량을 return합니다.
                Return값이 0 또는 음수인 경우 해당 요청이 이미 달성되었음을 의미합니다.'''
                return request_progressions[number_request][1]

            def __str__(self):
                return '<각종 정보들이 담긴 무언가 | . 수식 적어 사용>'
            
        return Infos()
            

    # mode별 준비

    # mode별 시작 준비(여기서 바로 실행)
    match hw4_settings.mode:
        case 0:
            # 10000초 후 종료
            end_time = 10000.0
        case 1:
            # (0, 0)에 대한 자원 25개 수집 요청 게시
            newRequest = (number_nextRequest, (0, 0), 0, 25)
            requests_active.append(newRequest)
            requests_all.append(newRequest)
            newRequest_progression = [False, 25, ContributionInfo(), -1]
            request_progressions[number_nextRequest] = newRequest_progression
            request_progression_forScenario = newRequest_progression
            number_nextRequest += 1
        case 3:
            # (4, 4)에 대한 거점 건설 요청 게시
            newRequest = (number_nextRequest, (4, 4), 1, getRequiredResourcesToBuildBaseOn(4, 4))
            requests_active.append(newRequest)
            requests_all.append(newRequest)
            newRequest_progression = [False, getRequiredResourcesToBuildBaseOn(4, 4), ContributionInfo(), -1]
            request_progressions[number_nextRequest] = newRequest_progression
            request_progression_forScenario = newRequest_progression
            number_nextRequest += 1
        case 4:
            # 종료 후 요약 출력을 할 예정이라면 캐릭터별 도착 시각을 기록할 목록 준비
            if hw4_settings.print_summarized_result:
                times_arrived = [-1] * len_characters

            # 중심 칸에 텔레포터 건설
            plane_public[0, 0][0][6] = 0
            pos_teleporters.append((0, 0))
            # 16개의 텔레포터를 x, y 각각 [-256, 255] 범위 내의 임의의 칸에 건설
            import random
            if hw4_settings.seed_forMode4 != None:
                random.seed(hw4_settings.seed_forMode4)
            count = 16
            while count:
                x = random.randint(-256, 255)
                y = random.randint(-256, 255)
                cell_public = plane_public[x // 64, y // 64][y % 64 * 64 + x % 64]

                # 해당 칸에 텔레포터가 이미 건설되어 있다면 다시 고름(총 262144칸 중 16칸을 고르는 것이니 확률은 희박할 듯)
                if cell_public[6] == 0:
                    continue

                cell_public[6] = 0
                pos_teleporters.append((x, y))
                
                count = count - 1

            # x, y 각각 [-256, 255] 범위 내의 각 칸의 점유 기여량을 [0, 100] 범위 내의 임의의 값으로 지정
            for y_chunkwise in range(-4, 4):
                for x_chunkwise in range(-4, 4):
                    chunk_public = plane_public[x_chunkwise, y_chunkwise]
                    for idx_chunk in range(4096):
                        amount_contribution = random.randint(0, 100)
                        cell_public = chunk_public[idx_chunk]
                        cell_public[2] -= amount_contribution
                        cell_public[9] += amount_contribution
                        if cell_public[2] <= 0:
                            cell_public[2] = 0
                            cell_public[10] = 0.75 ** (cell_public[9] / cell_public[11])
            del random
        case -1:
            # 디버그용 모드
            for y in range(-128, 128):
                for x in range(-128, 128):
                    planes_private[0][x, y] = int(getAmountOfResourcesOn(x, y) * ((y + 128) / 255))

            for y_chunkwise in range(-2, 2):
                for x_chunkwise in range(-2, 2):
                    for y_inChunk in range(64):
                        for x_inChunk in range(64):
                            plane_public[x_chunkwise, y_chunkwise][y_inChunk * 64 + x_inChunk][4] = 0
                            plane_public[x_chunkwise, y_chunkwise][y_inChunk * 64 + x_inChunk][6] = 0
            

    # mode별 종료 시점 판단용 Code 지정(자주 실행되므로 각각 함수 정의로 구성)
    match hw4_settings.mode:
        case 0:
            def isGameOver():
                # 10000초 경과시 종료
                return current_time >= end_time
        case 1:
            def isGameOver():
                # 초기 요청 달성시 종료
                return request_progression_forScenario[0]
        case 2:
            def isGameOver():
                # (0, 1)부터 (0, 8)까지의 여덟 칸을 점유하면 종료
                chunk_public = plane_public[0, 0]
                
                for y in range(1, 9):
                    if chunk_public[y * 64][2] > 0:
                        return False
                    
                return True
        case 3:
            def isGameOver():
                # 매 초마다 중심 칸 거점에 자원 1만큼 수납
                nonlocal last_time_seconds_forScenario
                amount = int(current_time) - last_time_seconds_forScenario
                if amount > 0:
                    plane_public[0, 0][0][0] += amount
                
                    # 거점 자원 목록의 마지막 항목에 합산 가능하면 합산
                    queue_base = plane_public[0, 0][0][1]
                    if len(queue_base) > 0 and queue_base[-1][0] == 0:
                        queue_base[-1] = (0, queue_base[-1][1] + amount)
                    else:
                        queue_base.append((0, amount))
                
                    last_time_seconds_forScenario += amount
                
                # 초기 요청 달성시 종료
                return request_progression_forScenario[0]

        case 4:
            def isGameOver():
                # 모든 캐릭터가 (255, -256)에 도착하면 종료
                pos_destination = (255, -256)

                for idx_character in range(len_characters):
                    # 방금 도착한 캐릭터가 있다면 도착 시각을 기록해 둠
                    if times_arrived[idx_character] == -1:
                        if pos_characters[idx_character] == pos_destination:
                            times_arrived[idx_character] = current_time
                        else:
                            return False

                return True
        case 5:
            def isGameOver():
                # (-64, -64)에 대한 완료된 거점 건설 요청과 자원 수집 요청이 있는 경우 종료
                pos_target = (-64, -64)
                flags = 0
                
                for number_request, request_progression in request_progressions.items():
                    if request_progression[0]:
                        request = requests_all[number_request]
                        
                        if request[1] == pos_target:
                            if request[2] == 0:
                                flags |= 0b01
                            elif request[2] == 1:
                                flags |= 0b10
                
                return flags == 0b11
        case -1:
            def isGameOver():
                # 디버그용 모드 - 어떤 캐릭터가 오류를 세 번 이상 발생시켰다면 종료
                for score in scores:
                    if score[0xa] + score[0xb] >= 3:
                        return True
                    
                return False

    # mode별 종료 이후 결과 요약 출력 방법 지정(나중에 한 번 실행할 예정이므로 함수 정의, 하나로 구성)
    if hw4_settings.print_summarized_result:
        def summarize_result():
            # 헤더 출력
            if hw4_settings.mode != 0:
                print(f'{current_time:.3f} 초만에 목표를 달성했습니다!')
                print()
                print(f'시나리오#{hw4_settings.mode} 결과 요약')

            # 요약 표 출력
            match hw4_settings.mode:
                case 1:
                    print('index |       능력치 ||  수집  |  이동  |  수납  |점유건설||수집한 자원량, 요청 달성에 기여한 자원량')
                    
                    for idx_character in range(len_characters):
                        score = scores[idx_character]
                        amount_contribution = request_progression_forScenario[2][idx_character]
                        print(f'{idx_character:5} | [{character_infos[idx_character][1]:2}, {character_infos[idx_character][2]:2}, {character_infos[idx_character][3]:2}] ||',
                              f'{score[0]:6} | {score[1]:6} | {score[5]:6} | {score[2] + score[3] + score[4]:6} ||',
                              f'{score[0x10]:3}, {request_progression_forScenario[2][idx_character]:3}')
                        
                case 2:
                    print('index |       능력치 ||  수집  |  점유  ||수집한 자원량, 점유에 사용한 자원량, 목표 달성에 기여한 자원량, A, B(후술)')

                    amounts_contribution = [0] * len_characters
                    
                    for y in range(0, 9):
                        for idx_character, amount_contribution in plane_public[0, 0][y * 64][3].items():
                            amounts_contribution[idx_character] += amount_contribution

                    for idx_character in range(len_characters):
                        score = scores[idx_character]
                        print(f'{idx_character:5} | [{character_infos[idx_character][1]:2}, {character_infos[idx_character][2]:2}, {character_infos[idx_character][3]:2}] ||',
                              f'{score[0]:6} | {score[2]:6} ||',
                              f'{score[0x10]:3}, {score[0x12]:3}, {amounts_contribution[idx_character]:3}, ( {score[0x2a]:3} / {score[1]:3} ), ( {score[0x2b]:7.3f} : {score[0x21]:7.3f} )')
                    
                    print('A: 점유 완료된 칸에서 이동한 횟수 / 전체 이동 횟수')
                    print('B: 점유 완료된 칸에서 이동하여 절약한 후딜레이 합 : 이동 이후 실제 적용된 후딜레이 합')
                case 3:
                    print('index |       능력치 ||  수집  |  이동  |  점유  |  수납  |  인출  |거점건설||수집량, 점유량, 거점건설량, 요청기여량')
                    for idx_character in range(len_characters):
                        score = scores[idx_character]
                        amount_contribution = request_progression_forScenario[2][idx_character]
                        print(f'{idx_character:5} | [{character_infos[idx_character][1]:2}, {character_infos[idx_character][2]:2}, {character_infos[idx_character][3]:2}] ||',
                              f'{score[0]:6} | {score[1]:6} | {score[2]:6} | {score[5]:6} | {score[6]:6} | {score[3]:6} ||',
                              f'{score[0x10]:3}, {score[0x12]:3}, {score[0x13]:3}, {amount_contribution:3}')
                case 4:
                    print('index |       능력치 || 도착시각 || (이동후딜합 / 횟수), (워프후딜합 / 횟수), A')
                    for idx_character in range(len_characters):
                        score = scores[idx_character]
                        
                        print(f'{idx_character:5} | [{character_infos[idx_character][1]:2}, {character_infos[idx_character][2]:2}, {character_infos[idx_character][3]:2}] ||',
                              f'{times_arrived[idx_character]:8.3f} ||',
                              f'( {score[0x21]:9.3f} / {score[0x1]:3} ), ( {score[0x27]:9.3f} / {score[0x7]:3} ),',
                              f'( {score[0x21] + score[0x27]:7.3f} : {score[0x3e]:7.3f} : {score[0x2b] + score[0x2d]:7.3f} : {score[0x41]:7.3f})')
                        print('A: (이동, 워프에 대해) 실제 적용된 후딜레이 합 : 민첩으로 절약한 후딜레이 합 : 점유로 절약한 후딜레이 합 : 기력 부족으로 증가한 후딜레이 합')
                case _:
                    # TODO 다른 시나리오들에 대한 내용 구성
                    pass
                    
            print()
                
            # 추가 내용 출력
            match hw4_settings.mode:
                case 1:
                    print('도움말')
                    print('- 수집한 자원량과 요청 기여량은 서로 다를 수 있어요. 수집 요청 달성에 기여하려면 요청 대상 칸과 그 주변 두 칸 범위 안에 있는 칸에서 자원을 수집해야 해요.')
                    print()
                case 2:
                    print('도움말')
                    print("- 점유 완료된 칸에서 다른 칸으로 이동, 워프할 때는 점유에 사용된 자원량에 따라 후딜레이 감소 효과를 받을 수 있어요(이 효과는 기력이 없는 채로 행동할 때도 적용돼요). 이번 시나리오의 경우 아마 내 캐릭터 혼자 게임에 참여하고 있기 때문에 초과 점유에 자원을 소모하는 것은 낭비가 될 가능성이 높지만, '본 게임'과 같이 여러 캐릭터들이 같이 참여하는 상황에서는 다른 캐릭터들이 자주 방문하게 될 칸에 대해 초과 점유를 해 두는 것이 전반적인 효율 상승에 도움이 될 수 있어요(초과 점유도 그냥 자원 들고 점유 행동 고르면 수행할 수 있어요). 이 시나리오만 놓고 본다면, 위/아래로 이동할 때 가급적 이전에 점유 완료해 둔 칸을 경유하여 이동하도록 구성해 볼 수 있을 거예요.")
                    print()
                case 4:
                    print('도움말')
                    print('- 이동, 워프 행동의 기본 후딜레이는 딱 1초예요. 따라서 기력 부족으로 후딜레이 페널티를 받지 않는다면 이동, 워프에 대해 실제 적용된 후딜레이 합은 두 행동을 수행한 횟수에다가 두 요인으로 절약한 후딜레이 합을 뺀 값과 같게 돼요.')
                    print('- 민첩성 능력치가 높은 작업자 스타일 캐릭터들은 점유 여부를 상대적으로 덜 고려하고 목적지까지 달리는 게 더 유리할 수 있고, 수집가 캐릭터들은 조금 돌아가더라도 점유된 칸 위주로 밟아 가며 전진하는 게 더 유리할 수 있을 거예요.')
                    print("- 뭐 이 시나리오에서는 주사위 굴려서 텔레포터 위치와 점유 기여량을 마구 지정했지만 '본 게임'에서는 보통은 중심 칸에서 바깥으로 뻗어 나가는 느낌으로 점유 및 건설을 하게 될 테니, 특정 칸에 도달하기 위한 경로를 재는 코드를 너무 무리해서 만들지는 않아도 돼요.")
                    print()
    

        
    # 캐릭터들에게 제공할 Data 준비
    data_for_characters = []
    infos_for_characters = []
    
    for idx_character in range(len_characters):
        data_for_characters.append(makeNewDataObject())
        infos_for_characters.append(makeNewInfosObject(idx_character))

    # Data 설정이 끝났으므로 무단 사용을 막기 위해 막아 둠
    isPermissionGranted = False
    


    # ---------------------------------------------------------------------------
    # 게임 진행

    for idx_character in range(len_characters):
        # Initialize() 호출 직전에 Data 전달
        characters[idx_character].data = data_for_characters[idx_character]
            
        infos = infos_for_characters[idx_character]
        infos.current_time = 0.0
        infos.pos_me = pos_characters[idx_character]
        infos.stamina = character_infos[idx_character][8]
        infos.r_carrying = 0
        characters[idx_character].infos = infos
        
        try:
            characters[idx_character].Initialize()
            character_infos[idx_character][0] = characters[idx_character].stats[0]
        except Exception:
            if hw4_settings.print_error_messages:
                traceback.print_exc()

            if hw4_settings.pause_after_error:
                try:
                    input('게임을 속행하려면 엔터 키를 입력하세요(Ctrl + C를 눌러 게임을 중단할 수 있습니다)>')
                except KeyboardInterrupt:
                    print('게임을 중단했습니다.')
                    return
                
    # Initiative 목록에서 가장 처음 의사 결정을 수행할 캐릭터 선택
    current_time, idx_character = initiative_order[idx_initiative_order_first]

    # mode별 종료 조건을 만족할 때까지 게임 진행
    while not isGameOver():
        # 대상 캐릭터에 대한 Data 미리 준비
        character_info = character_infos[idx_character]
        pos_character = pos_characters[idx_character]
        cell_public = plane_public[pos_character[0] // 64, pos_character[1] // 64][pos_character[1] % 64 * 64 + pos_character[0] % 64]
        score = scores[idx_character]

        # 의사 결정 도중 오류가 발생하지는 않았지만 체크 결과 유효하지 않음이 확인된 경우 str 값 지정
        msgForInvalidDecision = None
        # 유효하지 않은 의사 결정에 대해 (0xa,), 의사 결정 도중 오류 발생에 대해 (0xb,)로 지정
        decision = None
        end_realtime = -1
        score[0xc] += 1

        try:
            # MakeDecision() 호출 직전에 Data 전달
            characters[idx_character].data = data_for_characters[idx_character]
            
            infos = infos_for_characters[idx_character]
            infos.current_time = current_time
            infos.pos_me = pos_character
            infos.recent_action_me = recent_action_characters[idx_character]
            infos.stamina = character_info[8]
            infos.r_carrying = character_info[12]
            characters[idx_character].infos = infos
            
            # MakeDecision() 호출
            start_realtime = time.perf_counter()
            decision = characters[idx_character].MakeDecision()
            end_realtime = time.perf_counter()
            score[0xd] += end_realtime - start_realtime
            
            # 의사 결정 유효성 체크 + 최근 행동 목록 미리 갱신
            try:
                # 숫자 하나만 return한 경우 tuple로 만들어 줌
                if type(decision) == int:
                    decision = (decision, )
                    
                if (type(decision) != tuple and type(decision) != list) or type(decision[0]) != int:
                    msgForInvalidDecision = '의사 결정 결과로 return한 값의 형식이 유효하지 않아요.'
                # 의사 결정의 첫 값은 int 형식이며 [0, 9] 사이의 값이어야 함
                elif decision[0] < 0 or decision[0] > 9:
                    msgForInvalidDecision = '의사 결정 결과로 return한 값이 유효하지 않아요.'
                else:
                    match decision[0]:
                        case 0 | 9:
                            # 수집, 대기 의사 결정은 항상 유효하므로 최근 행동 목록만 갱신
                            recent_action_characters[idx_character] = obj_actions[decision[0]]
                        case 1:
                            # 이동 의사 결정은 값을 두 개 모아 return해야 함
                            if len(decision) < 2:
                                msgForInvalidDecision = '이동 의사 결정에 대한 방향 값을 지정하지 않았어요.'
                            # 이동 의사 결정의 두 번째 값은 int 형식이며 [0, 3] 사이의 값이어야 함
                            elif type(decision[1]) != int or decision[1] < 0 or decision[1] > 3:
                                msgForInvalidDecision = '이동 의사 결정에 대한 방향 값이 유효하지 않아요.'
                            # 최근 행동 목록 갱신
                            else:
                                recent_action_characters[idx_character] = obj_actions[10 + decision[1]]
                        case 3:
                            # 거점 건설 의사 결정은 현재 칸에 해당 시설이 건설되어 있지 않아야 함
                            if cell_public[4] == 0:
                                msgForInvalidDecision = '이미 거점이 있는 칸에서 거점 건설 의사 결정을 했어요.'
                            # 최근 행동 목록 갱신
                            else:
                                recent_action_characters[idx_character] = obj_actions[3]
                        case 4:
                            # 텔레포터 건설 의사 결정은 현재 칸에 해당 시설이 건설되어 있지 않아야 함
                            if cell_public[6] == 0:
                                msgForInvalidDecision = '이미 텔레포터가 있는 칸에서 텔레포터 건설 의사 결정을 했어요.'
                            # 최근 행동 목록 갱신
                            else:
                                recent_action_characters[idx_character] = obj_actions[4]
                        case 5 | 6:
                            # 수납/인출 의사 결정은 현재 칸에 거점이 건설되어 있어야 함
                            if cell_public[4] > 0:
                                if decision[0] == 5:
                                    msgForInvalidDecision = '거점이 없는 칸에서 수납 의사 결정을 했어요.'
                                else:
                                    msgForInvalidDecision = '거점이 없는 칸에서 인출 의사 결정을 했어요.'
                            # 최근 행동 목록 갱신
                            else:
                                recent_action_characters[idx_character] = obj_actions[decision[0]]
                        case 7:
                            # 워프 의사 결정은 값을 세 개 모아 return해야 함
                            if len(decision) < 3:
                                msgForInvalidDecision = '워프 의사 결정에 대한 x, y 좌표 값을 지정하지 않았어요.'
                            # 워프 의사 결정의 두 번째, 세 번째 값은 int 형식이어야 하며 출발지/도착지 칸 모두 이미 텔레포터가 건설되어 있어야 함
                            elif type(decision[1]) != int or type(decision[2]) != int:
                                msgForInvalidDecision = '워프 의사 결정에 대한 x, y 좌표 값은 둘 다 int 형식이어야 해요.'
                            else:
                                pos_destination_chunkwise = (decision[1] // 64, decision[2] // 64)
                        
                                # 도착지 칸이 포함된 chunk를 이전에 생성했는지, 도착지 칸에 텔레포터가 이미 건설되어 있는지, 출발지 칸에 텔레포터가 이미 건설되어 있는지 여부 체크
                                if ( pos_destination_chunkwise not in plane_public or
                                    plane_public[pos_destination_chunkwise][decision[2] % 64 * 64 + decision[1] % 64][6] > 0 ):
                                    msgForInvalidDecision = '워프 의사 결정의 도착지로 지정한 칸에 텔레포터가 없어요.'
                                elif cell_public[6] > 0:
                                    msgForInvalidDecision = '텔레포터가 없는 칸에서 워프 의사 결정을 했어요.'
                                # 최근 행동 목록 갱신
                                else:
                                    recent_action_characters[idx_character] = (decision[0], decision[1], decision[2])
                        case 8:
                            # 요청 게시 의사 결정은 값을 두 개 모아 return해야 함
                            if len(decision) < 2:
                                msgForInvalidDecision = '요청 게시 의사 결정에 대한 요청 종류 값을 지정하지 않았어요.'
                            # 요청 게시 의사 결정의 두 번째 값은 int 형식이어야 하며 [0, 2] 사이의 값이어야 함.
                            elif type(decision[1]) != int or decision[1] < 0 or decision[1] > 2:
                                msgForInvalidDecision = '요청 게시 의사 결정에 대한 요청 종류 값이 유효하지 않아요.'
                            else:
                                # 이 캐릭터가 이전에 게시했지만 아직 달성되지 않은 요청이 있는지 체크
                                if not request_progressions_perCharacter[idx_character][0]:
                                    msgForInvalidDecision = '아직 게시되고 달성되지 않은 요청이 있는데 요청 게시 의사 결정을 했어요.'
                                
                                elif decision[1] == 1:
                                    # 거점 건설 요청을 이미 건설이 끝난 칸에 대해 게시하고 있는지 체크
                                    if cell_public[4] == 0:
                                        msgForInvalidDecision = '이미 거점이 있는 칸에서 거점 건설 요청 게시 의사 결정을 했어요.'
                                    # 해당 칸에 대한 거점 건설 요청이 이미 게시되어 있는지 체크
                                    else:
                                        for request in requests_active:
                                            if request[1] == pos_character and request[2] == 1:
                                                msgForInvalidDecision = '이미 거점 건설 요청이 게시되어 있는 칸에서 거점 건설 요청 게시 의사 결정을 했어요.'
                                                break
                                        
                                elif decision[1] == 2:
                                    # 텔레포터 건설 요청을 이미 건설이 끝난 칸에 대해 게시하고 있는지 체크
                                    if cell_public[6] == 0:
                                        msgForInvalidDecision = '이미 텔레포터가 있는 칸에서 텔레포터 건설 요청 게시 의사 결정을 했어요.'
                                    # 해당 칸에 대한 텔레포터 건설 요청이 이미 게시되어 있는지 체크
                                    else:
                                        for request in requests_active:
                                            if request[1] == pos_character and request[2] == 2:
                                                msgForInvalidDecision = '이미 텔레포터 건설 요청이 게시되어 있는 칸에서 텔레포터 건설 요청 게시 의사 결정을 했어요.'
                                                break
                                
                                # 체크 결과 유효한 경우 최근 행동 목록 갱신
                                if msgForInvalidDecision == None:
                                    recent_action_characters[idx_character] = obj_actions[14 + decision[1]]

            except Exception:
                # 최근 행동 목록 갱신(대기로 간주)
                recent_action_characters[idx_character] = obj_actions[9]
                    
                if hw4_settings.print_error_messages:
                    traceback.print_exc()

                    if msgForInvalidDecision != None:
                        print(f'{character_infos[idx_character][0]}의 의사 결정 유효성 체크 과정에서 오류가 발생했어요.')
                        print('설명:', msgForInvalidDecision)
                        print('...이기는 한데 이 메시지가 출력된 것을 발견했다면 스샷 찍어서 강사에게 보여주세요. 안 나오는 게 정상임')
                    else:
                        print(f'{character_infos[idx_character][0]}의 의사 결정 유효성 체크 과정에서 강사도 예측 못 한 오류가 발생했어요.')
                        print('이 메시지가 출력된 것을 발견했다면 스샷 찍어서 강사에게 보여주세요.')
                        
                    if type(decision) == tuple and len(decision) == 1:
                        print('의사 결정 결과:', decision[0])
                    else:
                        print('의사 결정 결과:', decision)
                    
                if hw4_settings.pause_after_error:
                    try:
                        input('게임을 속행하려면 엔터 키를 입력하세요(Ctrl + C를 눌러 게임을 중단할 수 있습니다)>')
                    except KeyboardInterrupt:
                        print('\n게임을 중단했습니다.')
                        return
                    
                # 유효하지 않은 의사 결정 기록
                decision = (0xa, )
                msgForInvalidDecision = None
                
            if msgForInvalidDecision != None:
                # 최근 행동 목록 갱신(대기로 간주)
                recent_action_characters[idx_character] = obj_actions[9]
                
                if hw4_settings.print_error_messages:
                    print(f'{character_infos[idx_character][0]}의 의사 결정 유효성 체크 과정에서 문제를 발견했어요:')
                    print('설명:', msgForInvalidDecision)
                    if type(decision) == tuple and len(decision) == 1:
                        print('의사 결정 결과:', decision[0])
                    else:
                        print('의사 결정 결과:', decision)
                    
                if hw4_settings.pause_after_error:
                    try:
                        input('게임을 속행하려면 엔터 키를 입력하세요(Ctrl + C를 눌러 게임을 중단할 수 있습니다)>')
                    except KeyboardInterrupt:
                        print('\n게임을 중단했습니다.')
                        return
                
                # 유효하지 않은 의사 결정 기록
                decision = (0xa, )
                
        except Exception:
            if end_realtime == -1:
                end_realtime = time.perf_counter()
                score[0xd] += end_realtime - start_realtime
                
            # 최근 행동 목록 갱신(대기로 간주)
            recent_action_characters[idx_character] = obj_actions[9]

            if hw4_settings.print_error_messages:
                traceback.print_exc()
                print(f'{character_infos[idx_character][0]}의 의사 결정 도중에 오류가 발생했어요.')
                    
            if hw4_settings.pause_after_error:
                try:
                    input('게임을 속행하려면 엔터 키를 입력하세요(Ctrl + C를 눌러 게임을 중단할 수 있습니다)>')
                except KeyboardInterrupt:
                    print('\n게임을 중단했습니다.')
                    return

            # 오류 발생 기록
            decision = (0xb, )

        # 의사 결정 횟수 기록
        score[decision[0]] += 1
        
        # 대기를 제외한 행동 적용
        match decision[0]:
            case 0:
                # 수집
                amount_onCell = planes_private[idx_character][pos_character]
                amount_canGather = character_info[4] - character_info[12]
                if amount_onCell < amount_canGather:
                    amount_canGather = amount_onCell
                    
                if amount_canGather > 0:
                    planes_private[idx_character][pos_character] = amount_onCell - amount_canGather
                    character_info[12] += amount_canGather
                        
                    # 자원 목록의 마지막 항목에 합산 가능하면 합산
                    if len(character_info[13]) > 0 and character_info[13][-1][0] == idx_character:
                        character_info[13][-1] = (idx_character, character_info[13][-1][1] + amount_canGather)
                    else:
                        character_info[13].append((idx_character, amount_canGather))
                        
                    # 현재 칸에 대한 수집 요청이 있는 경우 도움 이력 기록(요청이 여럿 있는 경우 가장 일찍 게시된 것만 적용)
                    for request in requests_active:
                        if request[2] == 0 and abs(request[1][0] - pos_character[0]) + abs(request[1][1] - pos_character[1]) < 3:
                            progression = request_progressions[request[0]]
                            progression[1] -= amount_canGather
                            progression[2][idx_character] += amount_canGather
                                
                            # [0x30] - 수집 요청 달성을 위해 수집한 총 자원량
                            score[0x30] += amount_canGather
                                
                            if progression[1] <= 0:
                                progression[0] = True
                                if progression[3] != -1:
                                    # [0x18] - 자신이 게시했고 달성된 요청 수
                                    scores[progression[3]][0x18] += 1
                                requests_active.remove(request)

                            break

                    # [0x10] - 수집한 총 자원량
                    score[0x10] += amount_canGather
                    
                # 결과 기록
                delay_after_action = 1.0
                if character_info[8] <= 0:
                    # [0x40] - 체력)기력 부족으로 후딜레이가 증가한 횟수
                    score[0x40] += 1
                    # [0x41] - 체력)기력 부족으로 증가한 후딜레이 합
                    score[0x41] += 2.0
                    delay_after_action = 3.0
                        
                stamina_cost = 10
            case 1:
                # 이동
                last_pos_character_forLog = pos_character
                new_x, new_y = pos_character
                cell_public[8] -= 1
                    
                match decision[1]:
                    case 0:
                        new_y -= 1
                    case 1:
                        new_x -= 1
                    case 2:
                        new_x += 1
                    case 3:
                        new_y += 1

                pos_characters[idx_character] = (new_x, new_y)
                cell_destination = plane_public[new_x // 64, new_y // 64][new_y % 64 * 64 + new_x % 64]
                cell_destination[8] += 1
                    
                # [0x11] - 이동 도착지와 중심 사이의 거리의 합(이후 평균 측정할 때 사용)
                score[0x11] += abs(new_x) + abs(new_y)
                    
                # 결과 기록
                delay_after_action = 1.0
                
                # 점유로 인한 후딜레이 감소 적용
                if cell_public[2] == 0:
                    delay_after_action *= cell_public[10]
                    
                    for idx_contributor, amount in cell_public[3].items():
                        if idx_contributor != idx_character:
                            # [0x1d] - 칸 점유에 기여하여 다른 캐릭터의 이동/워프를 도와 얻은 점수(출발지에 대해 적용)
                            scores[idx_contributor][0x1d] += amount
                    
                    # [0x2a] - 점유된 칸에서 이동한 횟수
                    score[0x2a] += 1
                    # [0x2b] - 점유된 칸에서 이동할 때 절약한 후딜레이 합(기력 부족으로 증가한 양은 고려 안 함)
                    score[0x2b] += 1.0 - delay_after_action
                    

                # 기력 부족으로 인한 후딜레이 증가 적용
                if character_info[8] <= 0:
                    # [0x40] - 체력)기력 부족으로 후딜레이가 증가한 횟수
                    score[0x40] += 1
                    # [0x41] - 체력)기력 부족으로 증가한 후딜레이 합
                    score[0x41] += delay_after_action * 3 - delay_after_action
                    
                    delay_after_action *= 3
                    
                # 민첩성 능력치로 인한 후딜레이 감소 적용
                elif character_info[12] == 0:
                    # [0x3c] - 민첩)기력이 충분한 채로 자원을 들지 않고 이동/워프한 횟수
                    score[0x3c] += 1
                    # [0x3d] - 민첩)기력이 충분한 채로 자원을 들지 않고 이동/워프할 때 경과한 후딜레이 합(점유로 인해 감소한 양은 고려 안 함)
                    score[0x3d] += delay_after_action * character_info[6]
                    # [0x3e] - 민첩)기력이 충분한 채로 자원을 들지 않고 이동/워프할 때 절약한 후딜레이 합(점유로 인해 감소한 양은 고려 안 함)
                    score[0x3e] += delay_after_action - delay_after_action * character_info[6]

                    delay_after_action *= character_info[6]

                stamina_cost = character_info[12] - character_info[5]
                if stamina_cost < 1:
                    stamina_cost = 1
                    
                if character_info[12] > 0:
                    # [0x33] - 힘)자원을 들고 이동한 횟수
                    score[0x33] += 1
                    # [0x34] - 힘)이동할 때 들고 있던 자원량 합(이후 평균 측정할 때 사용)
                    score[0x34] += character_info[12]
                    # [0x35] - 힘)이동할 때 추가로 소모한 기력 합
                    score[0x35] += stamina_cost - 1
            case 2:
                # 점유
                amount = character_info[12]
                if amount > 0:
                    # 자신의 점유 참여 기록
                    if cell_public[2] > 0:
                        cell_public[2] -= amount
                        if cell_public[2] < 0:
                            cell_public[2] = 0
                        
                    cell_public[3][idx_character] += amount
                    cell_public[9] += amount
                    
                    # 점유 완료된 칸에 대해 이동, 워프 후딜레이 감소 계수 재계산
                    # (여기 고치면 게임 시작할 때 중심 점에 대해 수동으로 지정하는 부분도 고쳐야 함)
                    if cell_public[2] == 0:
                        cell_public[10] = 0.75 ** (cell_public[9] / cell_public[11])
                        
                    # [0x12] - 점유에 사용한 총 자원량
                    score[0x12] += amount

                    # 자원 생산자의 점유 참여 기록        
                    for idx_gatherer, amount_pile in character_info[13]:
                        cell_public[3][idx_gatherer] += amount_pile
                        # [0x1a] - 자신이 수집했고 점유에 사용된 총 자원량
                        scores[idx_gatherer][0x1a] += amount_pile
                            
                    # 들고 있는 자원 비움
                    character_info[12] = 0
                    character_info[13].clear()
                            
                # 결과 기록
                delay_after_action = 8.0 * character_info[7]
                delay_reduced = 8.0 - delay_after_action

                if character_info[8] <= 0:
                    # [0x40] - 체력)기력 부족으로 후딜레이가 증가한 횟수
                    score[0x40] += 1
                    # [0x41] - 체력)기력 부족으로 증가한 후딜레이 합
                    score[0x41] += 24.0 - delay_after_action
                    delay_after_action = 24.0
                else:
                    # [0x39] - 민첩)기력이 충분한 채로 점유/건설한 횟수
                    score[0x39] += 1
                    # [0x3a] - 민첩)기력이 충분한 채로 점유/건설할 때 경과한 후딜레이 합
                    score[0x3a] += delay_after_action
                    # [0x3b] - 민첩)기력이 충분한 채로 점유/건설할 때 절약한 후딜레이 합
                    score[0x3b] += delay_reduced
                        
                stamina_cost = 10
            case 3 | 4:
                amount = character_info[12]
                if amount > 0:
                    # 자신의 건설 참여 기록
                    if decision[0] == 3:
                        # 거점 건설
                        cell_public[4] -= amount
                        # 건설 완료시 목록에 추가
                        if cell_public[4] <= 0:
                            cell_public[4] = 0
                            pos_bases.append(pos_character)
                                
                        cell_public[5][idx_character] += amount
                        # [0x13] - 거점 건설에 사용한 총 자원량
                        score[0x13] += amount
                           
                        # 자원 생산자의 건설 참여 기록
                        for idx_gatherer, amount_pile in character_info[13]:
                            cell_public[5][idx_gatherer] += amount_pile
                            # [0x1b] - 자신이 수집했고 거점 건설에 사용된 총 자원량
                            scores[idx_gatherer][0x1b] += amount_pile
                    else:
                        # 텔레포터 건설
                        cell_public[6] -= amount
                        # 건설 완료시 목록에 추가
                        if cell_public[6] <= 0:
                            cell_public[6] = 0
                            pos_teleporters.append(pos_character)
                        
                        cell_public[7][idx_character] += amount
                        # [0x14] - 텔레포터 건설에 사용한 총 자원량
                        score[0x14] += amount
                           
                        # 자원 생산자의 건설 참여 기록
                        for idx_gatherer, amount_pile in character_info[13]:
                            cell_public[7][idx_gatherer] += amount_pile
                            # [0x1c] - 자신이 수집했고 텔레포터 건설에 사용된 총 자원량
                            scores[idx_gatherer][0x1c] += amount_pile                           
                        
                    # 현재 칸에 대한 건설 요청이 있는 경우 도움 이력 기록
                    for request in requests_active:
                        if request[1] == pos_character and (decision[0] == 3 and request[2] == 1 or decision[0] == 4 and request[2] == 2):
                            progression = request_progressions[request[0]]
                            progression[1] -= amount
                            progression[2][idx_character] += amount
                            if request[2] == 1:
                                # [0x31] - 거점 건설 요청 달성을 위해 사용한 총 자원량
                                score[0x31] += amount
                            else:
                                # [0x32] - 텔레포터 건설 요청 달성을 위해 사용한 총 자원량
                                score[0x32] += amount
                                    
                            if progression[1] <= 0:
                                progression[0] = True
                                if progression[3] != -1:
                                    # [0x18] - 자신이 게시했고 달성된 요청 수
                                    scores[progression[3]][0x18] += 1
                                requests_active.remove(request)
                            # 어떤 칸에 대한 거점/텔레포터 건설 요청은 각각 최대 하나씩만 존재하므로 더 찾을 필요 없음
                            break
                       
                    # 들고 있는 자원 비움
                    character_info[12] = 0
                    character_info[13].clear()
                        
                # 결과 기록
                delay_after_action = 10.0 * character_info[7]
                delay_reduced = 10.0 - delay_after_action

                if character_info[8] <= 0:
                    # [0x40] - 체력)기력 부족으로 후딜레이가 증가한 횟수
                    score[0x40] += 1
                    # [0x41] - 체력)기력 부족으로 증가한 후딜레이 합
                    score[0x41] += 30.0 - delay_after_action
                    delay_after_action = 30.0
                else:
                    # [0x39] - 민첩)기력이 충분한 채로 점유/건설한 횟수
                    score[0x39] += 1
                    # [0x3a] - 민첩)기력이 충분한 채로 점유/건설할 때 경과한 후딜레이 합
                    score[0x3a] += delay_after_action
                    # [0x3b] - 민첩)기력이 충분한 채로 점유/건설할 때 절약한 후딜레이 합
                    score[0x3b] += delay_reduced
                    
                stamina_cost = 20
            case 5:
                # 수납
                if character_info[12] > 0:
                    cell_public[0] += character_info[12]
                        
                    # 거점의 자원 목록의 뒤에 하나씩 추가
                    queue_base = cell_public[1]
                    for pile in character_info[13]:
                        # 자원 목록의 마지막 항목에 합산 가능하면 합산
                        if len(queue_base) > 0 and pile[0] == queue_base[-1][0]:
                            queue_base[-1] = (pile[0], queue_base[-1][1] + pile[1])
                        else:
                            queue_base.append(pile)
                        
                    # [0x15] - 수납한 총 자원량
                    score[0x15] += character_info[12]
                        
                    # 들고 있는 자원 비움
                    character_info[12] = 0
                    character_info[13].clear()
                        
                    # 자신을 제외한 거점 건설 참여자들에게 도움 점수 제공
                    for idx_contributor, amount in cell_public[5].items():
                        if idx_contributor != idx_character:
                            # [0x1e] - 거점 건설에 기여하여 다른 캐릭터의 수납/인출/대기를 도와 얻은 점수
                            scores[idx_contributor][0x1e] += amount
                    
                # 결과 기록
                delay_after_action = 0.5

                if character_info[8] <= 0:
                    # [0x40] - 체력)기력 부족으로 후딜레이가 증가한 횟수
                    score[0x40] += 1
                    # [0x41] - 체력)기력 부족으로 증가한 후딜레이 합
                    score[0x41] += 1.5 - delay_after_action
                    delay_after_action = 1.5
                    
                stamina_cost = 3
            case 6:
                # 인출
                amount_canGather = character_info[4] - character_info[12]
                if cell_public[0] < amount_canGather:
                    amount_canGather = cell_public[0]
                    
                if amount_canGather > 0:
                    queue_base = cell_public[1]
                        
                    cell_public[0] -= amount_canGather
                    character_info[12] += amount_canGather
                        
                    # 거점의 자원 목록에서 하나씩 가져와 캐릭터의 자원 목록에 더함
                    while amount_canGather > 0:
                        pile_picked = None
                        # 거점 자원 목록의 첫 항목에서 일부만 가져오면 되는 경우 분할
                        if queue_base[0][1] > amount_canGather:
                            queue_base[0] = (queue_base[0][0], queue_base[0][1] - amount_canGather)
                            pile_picked = (queue_base[0][0], amount_canGather)
                        # 첫 항목을 전부 가져와야 하는 경우 가져옴
                        else:
                            pile_picked = queue_base.popleft()
                            
                        # 캐릭터의 자원 목록의 마지막 항목에 합산 가능하면 합산
                        if len(character_info[13]) > 0 and character_info[13][-1][0] == pile_picked[0]:
                            character_info[13][-1] = (pile_picked[0], character_info[13][-1][1] + pile_picked[1])
                        else:
                            character_info[13].append(pile_picked)
                            
                        amount_canGather -= pile_picked[1]
                        
                    # 자신을 제외한 거점 건설 기여자들에게 도움 점수 제공
                    for idx_contributor, amount in cell_public[5].items():
                        if idx_contributor != idx_character:
                            # [0x1e] - 거점 건설에 기여하여 다른 캐릭터의 수납/인출/대기를 도와 얻은 점수
                            scores[idx_contributor][0x1e] += amount         
                                
                    # [0x16] - 인출한 총 자원량
                    score[0x16] += amount_canGather

                # 결과 기록
                delay_after_action = 0.5
                if character_info[8] <= 0:
                    # [0x40] - 체력)기력 부족으로 후딜레이가 증가한 횟수
                    score[0x40] += 1
                    # [0x41] - 체력)기력 부족으로 증가한 후딜레이 합
                    score[0x41] += 1.0
                    delay_after_action = 1.5
                        
                stamina_cost = 5
            case 7:
                # 워프
                last_pos_character_forLog = pos_character
                new_pos = (decision[1], decision[2])

                # 다른 칸으로 워프하는 경우
                if new_pos != pos_character:
                    cell_public[8] -= 1

                    cell_destination = plane_public[new_pos[0] // 64, new_pos[1] // 64][new_pos[1] % 64 * 64 + new_pos[0] % 64]
                        
                    # [0x17] - 워프한 칸 수
                    score[0x17] += abs(new_pos[0] - pos_character[0]) + abs(new_pos[1] - pos_character[1])

                    # 자신을 제외한 양쪽 텔레포터 건설 기여자들에게 도움 점수 제공
                    for idx_contributor, amount in cell_public[7].items():
                        if idx_contributor != idx_character:
                            # [0x1f] - 텔레포터 건설에 기여하여 다른 캐릭터의 워프를 도와 얻은 점수(출발지/도착지 모두에 대해 적용)
                            scores[idx_contributor][0x1f] += amount
                        
                    for idx_contributor, amount in cell_destination[7].items():
                        if idx_contributor != idx_character:
                            # [0x1f] - 텔레포터 건설에 기여하여 다른 캐릭터의 워프를 도와 얻은 점수(출발지/도착지 모두에 대해 적용)
                            scores[idx_contributor][0x1f] += amount

                    pos_characters[idx_character] = new_pos
                    cell_destination[8] -= 1
                            
                # 결과 기록
                delay_after_action = 1.0
                
                # 점유로 인한 후딜레이 감소 적용
                if cell_public[2] == 0:
                    delay_after_action *= cell_public[10]
                    
                    for idx_contributor, amount in cell_public[3].items():
                        if idx_contributor != idx_character:
                            # [0x1d] - 칸 점유에 기여하여 다른 캐릭터의 이동/워프를 도와 얻은 점수(출발지에 대해 적용)
                            scores[idx_contributor][0x1d] += amount
                    
                    # [0x2c] - 점유된 칸에서 워프한 횟수
                    score[0x2c] += 1
                    # [0x2d] - 점유된 칸에서 워프할 때 절약한 후딜레이 합(기력 부족으로 증가한 양은 고려 안 함)
                    score[0x2d] += 1.0 - delay_after_action
                    

                # 기력 부족으로 인한 후딜레이 증가 적용
                if character_info[8] <= 0:
                    # [0x40] - 체력)기력 부족으로 후딜레이가 증가한 횟수
                    score[0x40] += 1
                    # [0x41] - 체력)기력 부족으로 증가한 후딜레이 합
                    score[0x41] += delay_after_action * 3 - delay_after_action
                    
                    delay_after_action *= 3
                    
                # 민첩성 능력치로 인한 후딜레이 감소 적용
                elif character_info[12] == 0:
                    # [0x3c] - 민첩)기력이 충분한 채로 자원을 들지 않고 이동/워프한 횟수
                    score[0x3c] += 1
                    # [0x3d] - 민첩)기력이 충분한 채로 자원을 들지 않고 이동/워프할 때 경과한 후딜레이 합(점유로 인해 감소한 양은 고려 안 함)
                    score[0x3d] += delay_after_action * character_info[6]
                    # [0x3e] - 민첩)기력이 충분한 채로 자원을 들지 않고 이동/워프할 때 절약한 후딜레이 합(점유로 인해 감소한 양은 고려 안 함)
                    score[0x3e] += delay_after_action - delay_after_action * character_info[6]

                    delay_after_action *= character_info[6]

                stamina_cost = character_info[12] - character_info[5]
                if stamina_cost < 1:
                    stamina_cost = 1
                    
                if character_info[12] > 0:
                    # [0x36] - 힘)자원을 들고 워프한 횟수
                    score[0x36] += 1
                    # [0x37] - 힘)워프할 때 들고 있던 자원량 합(이후 평균 측정할 때 사용)
                    score[0x37] += character_info[12]
                    # [0x38] - 힘)워프할 때 추가로 소모한 기력 합
                    score[0x38] += stamina_cost - 1
            case 8:
                # 요청 게시
                amount = 0
                    
                match decision[1]:
                    case 0:
                        # 자원 수집 요청 - 현재 칸 기본 자원량의 10배
                        amount = getAmountOfResourcesOn(pos_character[0], pos_character[1]) * 10
                    case 1:
                        # 거점 건설 요청 - 건설 완료까지 남은 자원량
                        amount = cell_public[4]
                    case 2:
                        # 텔레포터 건설 요청 - 건설 완료까지 남은 자원량
                        amount = cell_public[6]
                    
                newRequest = (number_nextRequest, pos_character, decision[1], amount)
                infos.myRequest = newRequest
                requests_active.append(newRequest)
                requests_all.append(newRequest)
                newRequest_progression = [False, amount, ContributionInfo(), idx_character]
                request_progressions[number_nextRequest] = newRequest_progression
                request_progressions_perCharacter[idx_character] = newRequest_progression
                number_nextRequest += 1
                    
                # 결과 기록
                delay_after_action = 0.5
                if character_info[8] <= 0:
                    # [0x40] - 체력)기력 부족으로 후딜레이가 증가한 횟수
                    score[0x40] += 1
                    # [0x41] - 체력)기력 부족으로 증가한 후딜레이 합
                    score[0x41] += 1.0
                    delay_after_action = 1.5
                        
                stamina_cost = 10

        # 직접 대기 행동을 선택했거나, 유효하지 않은 의사 결정을 수행했거나, 의사 결정 도중 오류를 발생시킨 경우
        if decision[0] >= 9:
            # 대기(실제로 할 일은 없음)            
            
            # 결과 기록
            delay_after_action = 1.0
            
            # 이름이 stamina 'cost'긴 한데 그냥 회복량 담는 용도로 사용
            if cell_public[4] > 0:
                stamina_cost = character_info[10]
            else:
                stamina_cost = character_info[11]
                                                                      
                # 자신을 제외한 거점 건설 기여자들에게 도움 점수 제공
                for idx_contributor, amount in cell_public[5].items():
                    if idx_contributor != idx_character:
                        # [0x1e] - 거점 건설에 기여하여 다른 캐릭터의 수납/인출/대기를 도와 얻은 점수
                        scores[idx_contributor][0x1e] += amount         

                
            if character_info[8] + stamina_cost > character_info[9]:
                stamina_cost = character_info[9] - character_info[8]
            
            character_info[8] += stamina_cost
            
            # [0x19] - 대기를 통해 회복한 총 기력량
            score[0x19] += stamina_cost

            # [0x29] - 대기 행동을 수행한 이후에 실제로 적용받은 후딜레이 합
            score[0x29] += delay_after_action        
                
        # 대기가 아닌 다른 행동에 대한 기력 소모는 여기서 적용
        else:
            character_info[8] -= stamina_cost
            
            # [0x20] ~ [0x28] - 대기를 제외한 각 행동을 수행한 이후에 실제로 적용받은 후딜레이 합
            score[0x20 + decision[0]] += delay_after_action

        # [0x3f] - 체력)행동 종료 시점의 기력 합(이후 평균 측정할 때 사용)
        score[0x3f] += character_info[8] 
        
        # 행동 후딜레이 적용. Initiative 목록 갱신

        next_initiative = initiative_order[idx_initiative_order_first][0] + delay_after_action
        initiative_order[idx_initiative_order_first][0] = next_initiative
        if next_initiative < initiative_maximal_sorted:
            initiative_maximal_sorted = next_initiative

        idx_initiative_order_first += 1
        idx_initiative_order_first %= len_characters
        if initiative_order[idx_initiative_order_first][0] > initiative_maximal_sorted:
            initiative_order.sort()
            idx_initiative_order_first = 0
            initiative_maximal_sorted = initiative_order[-1][0]

        # log 출력
        if idx_character == idx_focal_character or hw4_settings.print_log_for_all_characters:
            print(f'{current_time:9.3f} | {character_info[0]} | {text_actions[decision[0]]} | ', end='')
            if decision[0] == 1 or decision[0] == 7:
                print(f'{last_pos_character_forLog} -> {pos_characters[idx_character]}')
            else:
                print(f'{pos_characters[idx_character]}')
        
        # Initiative 목록에서 다음에 의사 결정을 수행할 캐릭터 선택
        current_time, idx_character = initiative_order[idx_initiative_order_first]
        
    # 게임 종료 이후 결과 기록
    print('게임 종료!')
    
    if hw4_settings.export_result:
        f = open('result.csv', 'w')
                
        f.write('Index,이름,0_수집_횟수,1_이동_횟수,2_점유_횟수,3_거점_건설_횟수,4_텔레포터_건설_횟수,5_수납_횟수,6_인출_횟수,7_워프_횟수,8_요청_게시_횟수,9_대기_횟수,' +
                '10_유효하지_않은_의사_결정_횟수,11_오류_발생_횟수,12_총_의사_결정_횟수,13_총_의사_결정_시간_초,14_여백,15_여백,' +
                '16_수집_자원량,17_이동_거리합,18_점유_자원량,19_거점_자원량,20_텔포_자원량,21_수납_자원량,22_인출_자원량,23_워프_칸수,24_요청_달성횟수,25_대기_회복량,' +
                '26_수집-점유_자원량,27_수집-거점_자원량,28_수집-텔포_자원량,29_점유_도움,30_거점_도움,31_텔포_도움,' +
                '32_수집_후딜레이,33_이동_후딜레이,34_점유_후딜레이,35_거점_건설_후딜레이,36_텔레포터_건설_후딜레이,37_수납_후딜레이,38_인출_후딜레이,39_워프_후딜레이,40_요청_게시_후딜레이,41_대기_후딜레이,' +
                '42_초과점유_이동_횟수,43_초과점유_이동_절약_후딜레이,44_초과점유_워프_후딜레이,45_초과점유_워프_절약_후딜레이,46_여백,47_여백,' +
                '48_수집요청_자원량,49_거점요청_자원량,50_텔포요청_자원량,' +
                '51_자원들고이동_횟수,52_자원들고이동_자원량,53_자원들고워프_소모기력,54_자원들고워프_횟수,55_자원들고워프_자원량,56_자원들고워프_소모기력,' +
                '57_기력충분작업_횟수,58_기력충분작업_경과_후딜레이,59_기력충분작업_절약_후딜레이,60_기력충분이동_횟수,61_기력충분이동_경과_후딜레이,62_기력충분이동_절약_후딜레이,' +
                '63_기력합,64_기력부족_횟수,65_기력부족_후딜레이,\n')

        for idx_character in range(len_characters):
            score = scores[idx_character]
                    
            f.write(f'{idx_character},"' + character_infos[idx_character][0].replace('"', '\\"') + '",')

            for column in score:
                f.write(f'{column},')
            f.write('\n')
                    
        f.close()

    if hw4_settings.export_planes:
        # 평면 그림 크기 계산(공유 평면 기준)
        x_start_chunkwise = 0
        x_end_chunkwise = 0
        y_start_chunkwise = 0
        y_end_chunkwise = 0
        for pos_chunkwise in plane_public.keys():
            x, y = pos_chunkwise
            if x < x_start_chunkwise:
                x_start_chunkwise = x
            if x > x_end_chunkwise:
                x_end_chunkwise = x
            if y < y_start_chunkwise:
                y_start_chunkwise = y
            if y > y_end_chunkwise:
                y_end_chunkwise = y
        x_end_chunkwise += 1
        y_end_chunkwise += 1
                
        width_bitmap = (x_end_chunkwise - x_start_chunkwise) * 64
        height_bitmap = (y_end_chunkwise - y_start_chunkwise) * 64
        size_bitmap = width_bitmap * height_bitmap * 4
        size_file = 122 + size_bitmap
                
        # BMP 파일 출력 준비
        header = bytearray(122)
        header[0] = ord('B')
        header[1] = ord('M')
        header[2] = size_file & 0xff
        header[3] = (size_file & 0xff00) >> 8
        header[4] = (size_file & 0xff0000) >> 16
        header[5] = (size_file & 0xff000000) >> 24
        header[10] = 122
        header[14] = 108
        header[18] = width_bitmap & 0xff
        header[19] = (width_bitmap & 0xff00) >> 8
        header[20] = (width_bitmap & 0xff0000) >> 16
        header[21] = (width_bitmap & 0xff000000) >> 24
        header[22] = height_bitmap & 0xff
        header[23] = (height_bitmap & 0xff00) >> 8
        header[24] = (height_bitmap & 0xff0000) >> 16
        header[25] = (height_bitmap & 0xff000000) >> 24
        header[26] = 1
        header[28] = 32
        header[30] = 3
        header[34] = size_bitmap & 0xff
        header[35] = (size_bitmap & 0xff00) >> 8
        header[36] = (size_bitmap & 0xff0000) >> 16
        header[37] = (size_bitmap & 0xff000000) >> 24
        header[38] = 0x23
        header[39] = 0x2e
        header[42] = 0x23
        header[43] = 0x2e
        header[56] = 0xff
        header[59] = 0xff
        header[62] = 0xff
        header[69] = 0xff
        header[70] = ord(' ')
        header[71] = ord('n')
        header[72] = ord('i')
        header[73] = ord('W')

        # 공유 평면 출력 - chunk 단위로 다루므로 기본 투명에 특이사항 있는 칸을 채색
        bitmap = bytearray(size_bitmap)
        for pos_chunkwise, chunk in plane_public.items():
            x_base = (pos_chunkwise[0] - x_start_chunkwise) * 64
            # y축은 반전 필요
            y_base = (y_end_chunkwise - pos_chunkwise[1]) * 64 - 1
            x_offset = 0
            y_offset = 0
            offset = (y_base * width_bitmap + x_base) * 4
                    
            for cell in chunk:
                # B - 점유 완료시 0xff, 중심 칸은 항상 0
                # G - 텔레포터 건설 완료시 0xff, 중심 칸은 항상 0
                # R - 거점 건설 완료시 0xff, 중심 칸은 항상 0
                # A - 중심 칸만 0xff(완전 불투명), 거점/텔레포터/점유 중 하나라도 완료시 0x80
                        
                if cell[2] == 0:
                    bitmap[offset + 2] = 0xff
                    bitmap[offset + 3] = 0x80
                        
                if cell[4] == 0:
                    bitmap[offset + 1] = 0xff
                    bitmap[offset + 3] = 0x80
                        
                if cell[6] == 0:
                    bitmap[offset] = 0xff
                    bitmap[offset + 3] = 0x80
                        
                x_offset += 1
                offset += 4
                if x_offset == 64:
                    x_offset = 0
                    y_offset -= 1
                    offset = ((y_base + y_offset) * width_bitmap + x_base + x_offset) * 4
                        
        # 중심 칸은 검은색 100%
        offset = ((y_end_chunkwise * 64 - 1) * width_bitmap - x_start_chunkwise * 64) * 4
        bitmap[offset] = 0
        bitmap[offset + 1] = 0
        bitmap[offset + 2] = 0
        bitmap[offset + 3] = 0xff
                
        f = open('publicPlane.bmp', 'wb')
        f.write(header)
        f.write(bitmap)
        f.close()
                
        # 개인 평면들 출력 - 공유 평면 bitmap과 동일한 범위에 대해, 모든 픽셀에 대해 채색
        for idx_character in range(len_characters):
            plane_private = planes_private[idx_character]
                    
            x_start = x_start_chunkwise * 64
            x_end = x_end_chunkwise * 64
            x = x_start
            # y축은 반전 필요
            y = y_end_chunkwise * 64 - 1
                    
            for offset in range(0, (width_bitmap * height_bitmap) * 4, 4):
                max_resources = getAmountOfResourcesOn(x, y)
                current_resources = plane_private[x, y]
                        
                # 중간 정도 회색, 밝기는 최대 자원량에 따라 가변(5단계. 0x78 ~ 0x88)
                color = 0x78 + (max_resources % 5) * 0x04
                bitmap[offset] = color
                bitmap[offset + 1] = color
                bitmap[offset + 2] = color
                # 투명도는 최대 자원량 대비 남은 자원량에 비례(모두 수집했다면 완전 투명)
                bitmap[offset + 3] = int(current_resources / max_resources * 0xff)
                x += 1
                if x == x_end:
                    y -= 1
                    x = x_start
                                      
            f = open(f'privatePlane#{idx_character}.bmp', 'wb')
            f.write(header)
            f.write(bitmap)
            f.close()
    

    # mode별 결과 요약 출력
    if hw4_settings.print_summarized_result:
        summarize_result()



if __name__ == '__main__':
    run()
    input('종료하려면 엔터 키를 입력하세요>')
