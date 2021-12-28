a, b = map(int,input().split())

n = []
m = 1

while True:
    for i in range(1,m+1):
        n.append(m)
    if len(n)>b:
        break
    else:
        m+=1
print(sum(n[a-1:b]))