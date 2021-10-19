import random

deck = []  # 총 포커 덱
com = []   # 컴퓨터가 가지고 있는 카드
player = [] # 플레이어가 가지고 있는 카드

for i in range(1,14):     # 스페이드, 다이아몬드, 하트, 클로버 족보
    deck.append(("♠︎",i))
    deck.append(("♦︎",i))
    deck.append(("♥︎",i))
    deck.append(("♣︎",i))
    
random.shuffle(deck)  # 카드 섞기

for j in range(3):      # 3장씩 카드 받기
    com.append(deck[j])  
for k in range(3,6):
    player.append(deck[k])

com_num = []      # 카드들의 크기
player_num = []
print("com : ", end=' ')
print(com)
print("player : " ,end=' ')
print(player)

random.shuffle(com)   # 일단 컴퓨터가 낼 카드를 랜덤으로 뽑는다
a = int(input()) # 사용자가 낼 카드

if com[0][1]>player[a-1][1]:   # 카드의 족보에 따라 카드를 먼저받거나 후에 받거나. 코딩엔 별 의미가 안보임
    print("com : {}".format(com[0]))
    print("player : {}".format(player[a-1]))
    print("------------------------------")
    com.append(deck[6])
    player.append(deck[7])
    print("com : {},{}".format(com[0],deck[6]))
    print("player : {},{}".format(player[a-1],deck[7]))
else:
    print("com : {}".format(com[0]))
    print("player : {}".format(player[a-1]))
    print("------------------------------")
    player.append(deck[6])
    com.append(deck[7])
    print("com : {},{}".format(com[0],deck[7]))                 # 두장씩 오픈카드를 보여준다
    print("player : {},{}".format(player[a-1],deck[6]))    

print("------------------------------")
print("HIDE : {}".format(player))  # 자신의 패를 보여줌

#def poker_hand():   # 포커 족보 함수



