'''
N = int(input())
for i in range(N) :
    A,B = map(int,input().split())
    Alist = []
    Blist = []
    Clist = []
    for j in range(2,int(A**(1/2))+1):
        if A%j == 0:
            if A//j == j:
                Alist.append(j)
            else:
                Alist.append(j)
                Alist.append(A//j)
    for k in range(2,int(B**(1/2))+1):
        if B%k == 0 :
            if B//k == k :
                Blist.append(k)
            else:
                Blist.append(k)
                Blist.append(B//k)
    for q in Alist:
        if q in Blist:
            Clist.append(q)
    print(Alist)
    print(Blist)
    if Clist == []:
        print(A*B)
    else:
        print(A//max(Clist)*B//max(Clist)*max(Clist))
'''

import sys
N = int(sys.stdin.readline())
for i in range(N):
    a,b = map(int,sys.stdin.readline().split())
    aa,bb = a,b
    while a%b!=0:
        a,b = b, a%b
        
    print(aa*bb//b)          
