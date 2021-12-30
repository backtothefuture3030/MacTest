
A,P = map(int,input().split())
D = [A]

count = 0
while True:
    n = 0
    for i in str(D[count]):
        n += int(i)**P 
    count+=1
    D.append(n)
    if len(D) != len(set(D)):
        a = D[-1]
        break
    
D = D[:D.index(a)]
print(len(D))
    
    