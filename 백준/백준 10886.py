n = int(input())
cute = 0
uncute = 0
for i in range(n):
    a = input()
    if a=='1':
        cute+=1
    elif a=='0':
        uncute+=1

if cute>uncute:
    print( "Junhee is cute!")
else:
    print( "Junhee is not cute!")
