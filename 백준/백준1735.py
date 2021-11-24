import sys
import fractions


'''
a,b = map(int,sys.stdin.readline().split())
c,d = map(int,sys.stdin.readline().split())
e = fractions.Fraction(a,b) + fractions.Fraction(c,d)
e = str(e)
q, w = e.split('/')
print(int(q), end= ' ')
print(int(w))
'''

def gcd(a,b):
    while a%b != 0:
        mod = a%b
        a = b
        b = mod
    return b
a,b = map(int,sys.stdin.readline().split())
c,d = map(int,sys.stdin.readline().split())

g1 = gcd(b,d)
mother = b * d  // g1
son = a * (d//g1) + c * (b//g1)
g2 = gcd(son, mother)
print(son// g2, mother// g2)
        




'''
son = a*d + b*c
mother = b*d
son_list = []
mother_list = []
dauther = []

for i in range(2,son):
    if son % i == 0:
        son_list.append(i)

for j in range(2,mother):
    if mother % j == 0 :
        mother_list.append(j)
        
for q in son_list:
    if q in mother_list:
        dauther.append(q)

if len(dauther)>0:
    w = max(dauther)
    son = son//w 
    mother = mother//w
    print(son, mother)
else:
    print(son,mother)
        
'''      
        
        