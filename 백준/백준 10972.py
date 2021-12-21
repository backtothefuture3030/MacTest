a = int(input())
b = list(map(int,input().split()))
boolean = False
for i in range(a-1,0,-1):
    if b[i-1] < b[i]:
        for j in range(a-1,0,-1):
            if b[i-1] < b[j]:
                b[i-1], b[j] = b[j], b[i-1]
                b = b[:i] + sorted(b[i:])
                boolean = True
                break
    if boolean:
        print(*b)
        break
if not boolean:
    print(-1)        



'''from itertools import permutations
import sys
a = []
for k in range(1,int(input())+1):
    a.append(k)

b = tuple(map(int,sys.stdin.readline().split()))


c = list(permutations(a,len(a)))
n = 0

for i in c:
    n+=1
    if i == b:
        if n==len(c):
            print(-1)
            break
        else:
            for q in c[n]:
                print(q, end= ' ')
'''             
                
