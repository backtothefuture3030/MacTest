
N,B = map(int, input().split())

def conv(n,base):
    A = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    q, r = divmod(n,base)
    
    return conv(q,base) + A[r] if q else A[r]

print(conv(N,B))


    