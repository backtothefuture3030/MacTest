com_numbers = [1,1,2,2,7,7,9]

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
                print("{} One pair".format(com_numbers[i]))
                one = com_numbers[i]
                pair.append(com_numbers[i])
                One_pair = True
                pair.append(com_numbers[i])
            elif count==2:
                print("{} Triple".format(com_numbers[i]))
                triple = com_numbers[i]
                Triple = True
            elif count==3:
                print("{} Four cards".format(com_numbers[i]))
                Four_cards = True
    pair = list(set(pair))
    if Four_cards == True:                                   # 포카드
        pass
    elif One_pair == True and Triple == True:                # 풀하우스
        print("{},{} Full House".format(one,triple))
    elif One_pair == True and len(list(set(pair)))>=2:       # 투페어
        print("{},{} Two Pair".format(pair[-2],pair[-1]))
    return True

pair(com_numbers)

# 투페어가 구현이 되지못함 count 0개 초기화 오류도 수정을 해야함.