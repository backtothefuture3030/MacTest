N , M = map(int, input().split())

if N<=6:
    aprice = []
    for i in range(M):
        a, b = map(int,input().split())
        aprice.append(a)
        aprice.append(b*N)
    print(min(aprice))
else:
    bprice = []
    cprice = []
    dprice = []
    cases = N%6
    for i in range(M):
        a, b = map(int,input().split())
        bprice.append(a*(N//6))
        cprice.append(a)
        cprice.append(b*cases)
        dprice.append(a*(N//6+1))
        dprice.append(b*N)
    if min(bprice)+min(cprice)>= min(dprice):
        print(min(dprice))
    else:
        print(min(bprice)+min(cprice))