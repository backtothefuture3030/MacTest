

while True:
    a = []
    a.append(list(map(int,input().split())))
    if a == [[0,0]]:
        break
    if a[0][1]%a[0][0]==0:
        print("factor")
    elif a[0][0]%a[0][1]==0:
        print("multiple")
    else:
        print("neither")
    