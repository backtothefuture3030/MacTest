import math
a,b = map(int,input().split())

# 최대 공약수
if a>b:
    num = []
    nums = []
    for i in range(int(math.sqrt(b)),0,-1):
        if b%i==0:
            num.append(b//i)
            num.append(i)
    list(set(num))
    for j in num:
        if a%j==0:
            nums.append(j)
    print(max(nums))
    k = max(nums)
elif a==b:
    print(a)
    k = a
else:
    num = []
    nums = []
    for i in range(int(math.sqrt(a)),0,-1):
        if a%i==0:
            num.append(a//i)
            num.append(i)
    list(set(num))
    for j in num:
        if b%j==0:
            nums.append(j)
    print(max(nums))
    k = max(nums)

# 최소공배수
print(k*(a//k)*(b//k))