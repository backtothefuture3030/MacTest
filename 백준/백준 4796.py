
i = 0
while True:
    L, P, V = map(int,input().split())
    i+=1
    if L==0 and P==0 and V==0:
        break
    else:
        if V-P*(V//P)>L:
            case = L*(V//P) + L
        else:
            case = L*(V//P)+(V-P*(V//P))
        print("Case {}: {}".format(i, case))
        