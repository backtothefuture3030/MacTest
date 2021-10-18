
score = []
for i in range(5):
    score.append(list(map(int,input().split())))
    
a = score[0]
b = score[1]
c = score[2]
d = score[3]
e = score[4]

list = [sum(a),sum(b),sum(c),sum(d),sum(e)]
print(list.index(max(list))+1,max(list))