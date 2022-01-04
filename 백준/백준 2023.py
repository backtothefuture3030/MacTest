
'''
N = int(input())

a = int('1'+'0'*(N-1))
b = int('1'+'0'*N)
c = []

for i in range(a,b):
    count = 0
    n = int(i**(1/2)) + 1
    for q in range(2,n):
        if i%q == 0:
            count+=1
    if count == 0 :
        c.append(i)

print(c)
# 소수인 요소만 담기

for t in c:
    counts = 0
    while N!=1:
        r = int(str(t)[:N-1])
        for f in range(2,int(r**(1/2))+1):
            if r%f==0:
                counts+=1
        N-=1
    #if counts == 0:
        #print(w)
'''

# 모든 경우를 사용하기에는 너무 많은 경우가 존재한다, 고로 제곱근까지의 소수만 나눠주어야한다.

def sosu(num):
    for i in range(2, int(int(num)**0.5)+1):
        if int(num) % i == 0 :
            return
    if len(num) == N:
        print(num)
        return
    for p in prime:
        sosu(num+p)
    
N = int(input())
first = ['2','3','5','7']
prime = ['1','3','7','9']
for q in first:
    sosu(q)        
            
            
        
    