num = input()   # 입력값
original = num
num_list = []   # 제곱사이클을 판단하기 위한 리스트
count = 0       # 사이클의 횟수
while True:
    count+=1
    if count>100:
        print("100개 이상")
        break
    elif original in num_list:
        print(count-1)
        break
    if len(num)==1:
        num_list.append(str(int(num)**2))
        num = str(int(num)**2)
    else:
        sum = 0
        for i in range(len(num)):
            sum+=(int(num[i])**2)
        num = str(sum)
        num_list.append(str(sum))


#print(num_list)
