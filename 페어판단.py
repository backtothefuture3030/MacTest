com_numbers = [1,1,1,3,3,4,7]


def pair(com_numbers):
    com_numbers.sort()
    pairs = []
    count = 0
    for i in range(len(com_numbers)-1):
        count = 0
        for j in range(i+1,len(com_numbers)):
            if com_numbers[i] == com_numbers[j]:
                count+=1
                pairs.append(com_numbers[i])
        if count==1:
            print("{} 1 pair".format(com_numbers[i]))
        elif count==2:
            print("{} triple".format(com_numbers[i]))
        elif count==3:
            print("{} 4 cards".format(com_numbers[i]))
        list(set(pairs))
        while pairs[-1] in com_numbers:
            com_numbers.remove(pairs[-1])
    print(com_numbers)
    print(pairs)
    print(count)

pair(com_numbers)

# 투페어가 구현이 되지못함 count 0개 초기화 오류도 수정을 해야함.