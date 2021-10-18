import random
a = int(input("count : "))
q = []
for i in range(a):
    N = random.randrange(97,123)
    q.append(chr(N))

print(q)
for w in range(len(q)):
    print(q[w],end='')
print()