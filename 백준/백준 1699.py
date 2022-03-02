
'''
n = int(input())

dp = [0 for i in range(n+1)]

for i in range(1,n+1):
    dp[i] = i
    for j in range(1,i):
        if j**2 > i :
            break
        if dp[i] > dp[i-j**2]+1:
            dp[i] = dp[i-j**2] + 1
            
print(dp[n])
   ''' 


'''

cases = []

n = int(input())
count = 0

while True:
    w=0
    while n!=0:
        n-=((int(n**0.5))**2)
        count+=1
        if n==0:
            cases.append(count)
            break
    if count==2 :
        break
    w+=1
print(cases)
    

'''
'''
cases = []
n = int(input())

count = 0
while n!=0:
    n-=(int(n**0.5))**2
    count+=1
cases.append(count)

print(cases)
'''
'''
n = int(input())
dp = [0]*(n+1)
for i in range(1, n+1):
    dp[i]=i
    for j in range(1, int(i**0.5)+1):
        dp[i] = min(dp[i],dp[i - j*j]+1)
print(dp[n])
'''
import sys
import math
n = int(sys.stdin.readline())

dp = [0]*(n+1)

for i in range(1, n+1):
    dp[i]=i
    for j in range(1, int(math.sqrt(i))+1):
        dp[i] = min(dp[i], dp[i-j*j]+1)
        
print(dp[n])
    
