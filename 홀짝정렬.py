a = list(map(int,(input().split())))
even = []
odd = []
for i in a:
    if i%2==0:
        even.append(i)
    elif i%2==1:
        odd.append(i)
even.sort()
even.sort(reverse=True)
odd.sort()
if len(even)==len(odd):
    for j in range(len(a)//2):
        print(odd[j], end= ' ')
        print(even[j], end = ' ')
    print()
else:
    print("홀수와 짝수의 개수가 다르다")
