# magic-i_python_team

    # 수정전
    
    git pull

    git status



    # 수정후

    git add .

    git pull
    
    git commit -m "커밋이름"

    git push




캐릭터 스펙
====

속도 
-----
* 나중에 적팀, 우리팀 모두 속도를 가지고 decreasing order로 배열, 이후 이 순서대로 턴을 재생함.
* 매 턴마다 속도의 우위를 재설정해야함.
   아마도 SortBySpeed() 함수를 따로 정의 하는 것이 좋을 듯

데미지(Damage per turn - DPT)
------
* 한 턴마다 이 캐릭터가 줄 수 있는 기본 대미지
* 80퍼센트로 기본 데미지
* 10퍼센트로 약 1.2배 쎈 데미지
* 10퍼센트로 약 0.6배 약해진 데미지 <br>

크리티컬 히트 확률
-----
* DPT의 2배의 데미지를 주는 확률

방어력
-----
대부분 0일꺼임

명중률
------
공격의 명중 여부

회피
------
공격 회피하는 정도

상태이상 수치
------
명중에 관여하는 상태이상

**(내 명중률 + 상태이상 수치 - 회피율)*100 = 명중 확률**



상태이상
----
 매 팀원의 행동마다 주변 팀원에게 공포 10씩 추가

1. 절망 = 70퍼센트의 확률로 행동을 하지 않음
2. 편집증 = 70퍼센트의 확률로 행동을 받지 않음
3. 정신분열 = 조작 불가.{랜덤 공격(40퍼센트), 턴 넘기기(40퍼센트), 자해(20퍼센트)}

영웅의 등장
-------
1. 구사회생: 기본 데미지가 2배가 되고, 방어력 50으로 FIX. 단 피는 전체체력의 10퍼센트로 조정. 스트레스 수치는 반토막으로 다시 시작
2. 차분한 영혼: 스트레스 수치가 0으로 FIX. 턴마다 모든 아군의 스트레스 수치 5만큼 감소.
3. 회광반조: 4턴 뒤 사망. 하지만 그 턴간 본인 포함 모든 아군 무적. 그동안 스트레스 수치도 중첩 안됨
4. 무의식의 극의: 치트키... DPT가 무한대로 발산함. 평타 하나당 적 하나씩 죽음.

------

A1 A2 B1 B2 B3 A3라 하자...

A는 플레이어, B는 몹

A1 턴에 다음과 같은 순서로 진행

### CHECK
1. 스턴 여부 확인. 스턴이면 스턴을 해제하고 턴은 패스
2. 예약 데미지 확인, 예약 데미지 반영. 만약 체력이 0 이하로 내려갈 시 본인 턴에 사망처리
3. 정신상태 확인. 정신상태에 따른 턴마다 효과 반영

CHECK 이후 TURN 이전에 캐릭터의 스탯을 업데이트하고 반영. 이 내용을 TURN에 사용

### TURN
어떤 선택을 할 지 고르게 함.
1. 2개정도의 스킬 중 하나 선택 -> 스킬의 대상 고를 것(후보군을 표시하면 좋을 듯)
2. 턴 넘기기
3. 후퇴 -> 게임 포기

-------

즉 크게 게임 진행은

### 1. 페이즈 시작
### 2. 속도배열
### 3. 속도 빠른 순서대로
### 4. CHECK
### 5. TURN

즉시 처리 정보는 바로 처리
예약 처리는 미루기

-------

페이즈 끝.. 페이즈 숫자 바꾸며 다시 페이즈 시작.

플레이어 팀 모두 사망 혹은 적팀 모두 사망시에 다음 스테이지로.

스테이지는 총 3개

쉬운 몹 2마리로 1스테이지
다음으로 일반 몹 3마리로 2스테이지
마지막으로 보스몹 1마리로 3스테이지

보스몹까지 죽이면
(희망사항... 각 캐릭터별 힐량, 딜량, 받은 딜량 표시하고 걸린 총 페이즈 개수 표시)


count_enemy가 턴마다 갱신

while(count_enemy != 0)
때마다 페이즈 재생
