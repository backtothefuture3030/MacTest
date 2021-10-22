com_numbers = [1,5,10,11,12,13,9]
def straight(com_numbers):
    com_numbers.sort(reverse=True)   
    so = []
    r = 0
    if com_numbers[0]==13 and com_numbers[1]==12 and com_numbers[2]==11 and com_numbers[3]==10 and com_numbers[4]==9 and com_numbers[6]==1:
        print("Mountain")
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
                print("back straight")
                return True
            else:
                print("straight")
                print(max(so))
                return True        # 랭크를 매겨야한다. 단순한 트루 뿐 아니라 점수까지 더해줘야한다. 
        else:
            del com_numbers[1]
            del com_numbers[1]
            if [1,10,11,12,13]==com_numbers:
                print("Mountain")
                return True
            else:
                print(max(com_numbers))   # 스트레이트가 아님
                return 0
    
    
straight(com_numbers)