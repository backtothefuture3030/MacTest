'''
n = int(input())

num = ('1'*n)
ten = 0
count = 0 
hop = 0 

for i in num:
    ten+=int(i)*(2**count)
    count+=1
    
for j in range(1,ten+1):
    hop+=j  
print(int(str(bin(hop))[2:]))
'''
'''
import sys
k = int(sys.stdin.readline())
print(int("1"*k+"0"*(k-1)))
'''
k = int(input())
t = 2**k - 1
res = t*(t+1)//2
print(bin(res)[2:])
    
