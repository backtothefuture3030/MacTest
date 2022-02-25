import itertools
import math

a = []

for i in range(int(input())):
    a.append(list(input()))
 

for j in a:    # 숫자들의 중복없는 순열 
    r = []
    b = []
    hop = 0
    for t in range(1,len(j)+1):
        b+=list(set(list(map(''.join, itertools.permutations(j,t)))))
    count = 0
    for k in b:   # r에다가 b의 구성원을 정수로 바꾸는 과정
        r.append(int(k))
    r = list(set(r))
    for x in r:    # r에 있는 원자들이 소수인지 아닌지를 판단
        count = 0
        if x == 1 or x==0:
            pass
        else:
            for q in range(2,int(math.sqrt(x))+1):
                if x%q==0 and x>=q:
                    count+=1
                    if count>0:
                        break
            if count==0:
                hop+=1

    print(hop)

    