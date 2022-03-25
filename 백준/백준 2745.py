N, B = input().split()
N = ''.join(reversed(N))
B = int(B)

A = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
sum = 0 

for i in range(len(N)-1,-1,-1):
    result = A.index(N[i]) * (B**i)
    sum+=result
print(sum)

