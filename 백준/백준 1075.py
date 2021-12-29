N = int(input())
F = int(input())

if str(N-(N%F))[:-2] == str(N)[:-2]:
    a = N-(N%F)
    while True:
        a-=F
        if str(a)[:-2] != str(N)[:-2]:
            a+=F
            break
    print(str(a)[-2:])
else:
    print(str(N+F-(N%F))[-2:])
    



