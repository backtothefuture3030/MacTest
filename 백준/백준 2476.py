N = int(input())
hops = []
for i in range(N):
    hop = 0 
    a,b,c = map(int,input().split())
    if a==b==c:
        hop += (10000 + a*1000)
    elif a==b:
        hop += (1000 + a*100)
    elif a==c:
        hop += (1000 + a*100)
    elif b==c:
        hop += (1000 + b*100)
    elif a!=b!=c:
        hop += max([a,b,c]) * 100
    hops.append(hop)

print(max(hops))
    
        
        