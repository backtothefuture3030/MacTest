
sticks = []
high_list = []
for i in range(int(input())):
    sticks.append(input(int()))

high_list.append(sticks[-1])
seq = []

for j in range(len(sticks)-2,0,-1):
    if sticks[j] >= sticks[j-1] :
        high_list.append(sticks[j])
    else:
        high_list.append(sticks[j-1])
for q in list(set(high_list)):
    for k in range(len(sticks)-1,-1,-1):
        if sticks[k]==q: 
            seq.append(k+1)
            break
seq.sort(reverse=True)


print(len(set(high_list)))
print(seq)

