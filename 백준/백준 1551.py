
N, K = map(int,input().split())
nums = list(map(int,input().split(',')))

while K!=0:
    chg = len(nums)
    for i in range(0,len(nums)-1):
        nums.append(nums[i+1] - nums[i])
    nums = nums[chg:]
    K-=1

print(*nums, sep=',')

