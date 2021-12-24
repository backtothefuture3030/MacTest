
chess = []

for i in range(8):
    chess.append(list(map(str,list(input()))))

count = 0  # 체스 말의 개수


for i in range(8):
    for j in range(8):
        if (i+j) % 2 == 0 :
            if chess[i][j] == 'F':
                count+=1

print(count)