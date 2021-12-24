a , b = map(int,input().split())
stage = [list(map(int,input().split())) for _ in range(a)]

on = a*b

left = 0 
for i in range(a):
    for j in range(b):
        if j == 0 :
            left += stage[i][j]
        else:
            if stage[i][j-1] < stage[i][j]:
                left += stage[i][j] - stage[i][j-1]
                
front = 0
for j in range(b):
    for i in range(a):
        if i == 0 :
            front += stage[i][j]
        else:
            if stage[i-1][j] < stage[i][j]:
                front += stage[i][j] - stage[i-1][j]

hop = 2*(on+left+front)
print(hop)

                