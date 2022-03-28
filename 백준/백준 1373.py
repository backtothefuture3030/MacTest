'''
b = input()
sum = 0
a = 0

for i in b:
    a+=1
    sum+=int(i)*2**(len(b)-a)

print(oct(sum)[2:])
'''

print(oct(int(input(),2))[2:])