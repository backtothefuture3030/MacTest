a, b = input().split()
a = int(a)
b = int(b)
t = 1
z = 1


for i in range(a,a-b,-1):
    t*=i
for j in range(b,0,-1):
    z*=j
    
print(t//z)