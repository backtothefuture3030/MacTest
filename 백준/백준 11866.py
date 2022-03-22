from collections import deque

N, K = map(int, input().split())

A = deque(list(range(1,N+1)))

i = 0
W = []

while True:
    A.append(A.popleft())
    i+=1
    if i%K==0 and i!=0:
        W.append(A[-1])
        del A[-1]
    if len(W)==N:
        break
    
print('<{}>'.format(', '.join(map(str, W))))
        
        
        
        
    


