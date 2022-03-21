N = int(input())
A = list(map(int, input().split()))
total = 0

if len(A) == N :
    B, C = map(int, input().split())


if len(A) == 1:
    A[0] -= B
    total+=1
    if A[0] != 0:
        if A[0]%C == 0:
            total+= (A[0]//C)
        else:
            total+= (A[0]//C) + 1
else:
    for i in range(0,len(A)):
        A[i] = A[i] - B
    total +=N
    for j in range(0,len(A)):
        if A[j] <= 0:
            pass
        elif A[j] <= C:
            total+=1
        else:
            if A[j]%C == 0:
                total += (A[j]//C)
            else:
                total += (A[j]//C) + 1
            
print(total)
        
    
    