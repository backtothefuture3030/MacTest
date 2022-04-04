'''
N = int(input())
sosus = []

for i in range(2,N+1):
    q = 0
    for j in range(2,i):
        if i%j==0:
            q+=1
            break
    if q==0:
        sosus.append(i)
        
count = 0
hop = 0

while True:
    hop = 0
    if len(sosus)==0:
        break
    else:
        for i in sosus:
            if hop<N:
                hop+=i
            if hop==N:
                count+=1
                sosus.pop(0)
                break
            if hop>N:
                sosus.pop(0)
                break
        if len(sosus)==1 and sosus[-1] != N:
            break

print(count)
'''

# 에라토스테네스의 체 이용

sosusox = [True for _ in range(4000001)]

for i in range(2, int(4000001 ** 0.5)):
    if sosusox[i]:
        for j in range(i+i, 4000001, i):
            sosusox[j] = False 
sosus = [i for i, j in enumerate(sosusox) if j == True and i >=2 ]

hop = [0] * (len(sosus) + 1)
for i in range(len(sosus)):
    hop[i+1] = hop[i] + sosus[i] 

N = int(input())

answer = 0
start = 0
end = 1

while start < len(hop) and sosus[end-1] <= N:
    if hop[end] - hop[start] == N: 
        answer += 1
        start += 1
    elif hop[end] - hop[start] > N: 
        start += 1
    else:
        if end < len(hop) - 1: 
            end += 1
        else:
            start += 1

print(answer)