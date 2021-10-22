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

com_num = []      # 카드들의 첫번째 장 레벨
player_num = []
#print("com : ", end=' ')
#print(com)
print("player : " ,end=' ')
print(player)

random.shuffle(com)   # 일단 컴퓨터가 낼 카드를 랜덤으로 뽑는다
a = int(input("먼저 낼 오픈카드를 선택하세요 : ")) # 사용자가 낼 카드

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
print("------------------------------")
check1 = input("배팅 하시겠습니까? y or n : ")

if check1 == "y":
    player.append(deck[8])
    com.append(deck[9])
    print("------------------------------")
    print("com : {},{},{}".format(com[0],com[-2],com[-1]))                 # 세장씩 오픈카드를 보여준다
    print("player : {},{},{}".format(player[a-1],player[-2],player[-1]))    
    print("------------------------------")
    print("HIDE : {}".format(player))  # 자신의 패를 보여줌
else:
    print("패배 하셨습니다")
    print("com : {}".format(com))
    exit()

check2 = input("배팅 하시겠습니까? y or n : ")

if check2 == "y":
    player.append(deck[10])
    com.append(deck[11])
    print("------------------------------")
    print("com : {},{},{},{}".format(com[0],com[-3],com[-2],com[-1]))                 # 네장씩 오픈카드를 보여준다
    print("player : {},{},{},{}".format(player[a-1],player[-3],player[-2],player[-1]))    
    print("------------------------------")
    print("HIDE : {}".format(player))  # 자신의 패를 보여줌
else:
    print("패배 하셨습니다")
    print("com : {}".format(com))
    exit()

player.append(deck[12])
com.append(deck[13])
print("HIDE : {}".format(player))    # 배팅 전 마지막 카드 확인
print("------------------------------")
check3 = input("베팅 하시겠습니까? y or n : ")
if check3 == "y":
    print("------------------------------")
    print("com : {}".format(com))
    print("player : {}".format(player))
else:
    print("패배 하셨습니다")
    print("com : {}".format(com))
    exit()
 
# 카드의 무늬와 숫자 따로 담기
com_pattern = []                  # 무늬
player_pattern = []
for i in com:
    com_pattern.append(i[0])
for j in player:
    player_pattern.append(j[0])    

com_numbers = []                  # 숫자
player_numbers = []
for q in com:
    com_numbers.append(q[1])
for w in player:
    player_numbers.append(w[1])

com_numbers.sort()
player_numbers.sort()
print(com_numbers)
print(player_numbers)

com_rank = 0
player_rank = 0


# 플러쉬
def flush(com_pattern):
    if com_pattern.count('♠︎')==5:
        print("com : ♠︎ flush")
        return True
    elif com_pattern.count('♦︎')==5:
        print("com : ♦︎ flush")
        return True
    elif com_pattern.count('♥︎')==5:
        print("com : ♥︎ flush")
        return True
    elif com_pattern.count('♣︎')==5:
        print("com : ♣︎ flush")
        return True
    else:
        return False

# 스트레이트
def straight(com_numbers):
    com_numbers.sort(reverse=True)   
    so = []
    r = 0
    if com_numbers[0]==13 and com_numbers[1]==12 and com_numbers[2]==11 and com_numbers[3]==10 and com_numbers[4]==9 and com_numbers[6]==1:
        print("com : Mountain")
        exit()
    else:
        for i in range(len(com_numbers)-1):
            if com_numbers[i+1]-com_numbers[i]==-1:
                if i==len(com_numbers)-2:
                    so.append(com_numbers[i])
                    so.append(com_numbers[i+1])
                    r+=1
                else:
                    so.append(com_numbers[i])
                    r+=1
            elif r>=4:
                so.append(com_numbers[i])
                break
            else:
                r=0
                so=[]
        if r>=4:
            if max(so)==5:
                print("com : back straight")
                return True
            else:
                print("com : {} straight".format(max(so)))
                return True        # 랭크를 매겨야한다. 단순한 트루 뿐 아니라 점수까지 더해줘야한다. 
        else:
            del com_numbers[1]
            del com_numbers[1]
            if [1,10,11,12,13]==com_numbers:
                print("com : Mountain")
                return True
            else:
                #print("com의 최고 하이카드는 {}".format(max(com_numbers)))   # 스트레이트가 아님
                return False


# 페어 
def pair(com_numbers):
    com_numbers.sort()
    count = 0
    pair = []
    One_pair = False
    Triple = False
    Four_cards = False
    for i in range(len(com_numbers)-1):
        count = 0
        if com_numbers[i]==com_numbers[i-1]:
            pass
        else:
            for j in range(i+1,len(com_numbers)):
                if com_numbers[i] == com_numbers[j]:
                    count+=1
            if count==1:
                print("com : {} One pair".format(com_numbers[i]))
                one = com_numbers[i]
                pair.append(com_numbers[i])
                One_pair = True
                pair.append(com_numbers[i])
            elif count==2:
                print("com : {} Triple".format(com_numbers[i]))
                triple = com_numbers[i]
                Triple = True
            elif count==3:
                print("com : {} Four cards".format(com_numbers[i]))
                Four_cards = True
    pair = list(set(pair))
    if Four_cards == True:                                   # 포카드
        pass
    elif One_pair == True and Triple == True:                # 풀하우스
        print("com : {},{} Full House".format(one,triple))
    elif One_pair == True and len(list(set(pair)))>=2:       # 투페어
        print("com : {},{} Two Pair".format(pair[-2],pair[-1]))
    elif One_pair == False and Triple == False and Four_cards == False:
        print("com : {} card".format(max(com_numbers)))




pair(com_numbers)
flush(com_pattern)
straight(com_numbers)


# 포카드, 트리플, 풀하우스, 투페어, 원페어 pair 판단하는 코드
