n = int(input())

N = [0,1] + [0]*n 
i = 0
while i<n:
    N[i+2] = N[i]+N[i+1]
    i+=1
    
print(N[n])
    