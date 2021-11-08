
'''
초기에 생각했던 간단한 생각, 반복이 많아지면 시간 초과가 되어버린다 heap stack 을 생각해야한다.

import sys

count = int(sys.stdin.readline())
i = 0
a = []
while count>i:
    a.append(int(sys.stdin.readline()))
    count-=1
    a.sort()
    if len(a)%2==0:
        if a[len(a)//2] > a[len(a)//2-1]:
            print(a[len(a)//2-1])
        else:
            print(a[len(a)//2])
    else:
        print(a[(len(a)-1)//2])

'''


