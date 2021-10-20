com_numbers = [1,10,11,12,13,2,4]
def straight(com_numbers):
    com_numbers.sort()   # 1,3,4,6,7,8,9
    so = []
    r = 0
    for i in range(len(com_numbers)-1):
        if com_numbers[i+1]-com_numbers[i]==1:
            if i==len(com_numbers)-2:
                so.append(com_numbers[i])
                so.append(com_numbers[i+1])
                r+=1
            else:
                so.append(com_numbers[i])
                r+=1
        else:
            r=0
            so=[]
    if r==4:
        print("straight")
        print(max(so))
        return True
    else:
        del com_numbers[1]
        del com_numbers[1]
        if [1,10,11,12,13]==com_numbers:
            print("high straight")
            return True
            
straight(com_numbers)