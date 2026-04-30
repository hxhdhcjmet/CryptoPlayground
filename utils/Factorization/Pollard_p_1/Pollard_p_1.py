"""
Pollard p-1算法
p为模n的奇素因子,p-1能分解为不同素数幂乘积形式:
p-1 = p_1^t_1 p_2^t_2... = q_1 q_2 ...
对每个q满足q_i <= B,则(p-1)|B!
令a = 2^{B!} mod n
由Fermat小定理有
2^{p-1} = 1 mod p
又(p-1)|B!
所以a = 1 mod p,即p | (a-1)
gcd(p-1,n) = p
"""

import math


def gcd(a,b):
    while b:
        a,b=b,a%b
    return a

def primes_upto(n):
    sieve=[True]*(n+1)
    ps=[]
    for i in range(2,n+1):
        if sieve[i]:
            ps.append(i)
            for j in range(i*i,n+1,i):
                sieve[j]=False
    return ps

def pollard_p1_stage2(n,B1=100,B2=1000,a=2):

    # Stage 1
    for p in primes_upto(B1):
        pk=p
        while pk*p<=B1:
            pk*=p
        a=pow(a,pk,n)

    d=gcd(a-1,n)
    if 1<d<n:
        return d

    # Stage 2
    for q in primes_upto(B2):
        if q<=B1:
            continue

        b=pow(a,q,n)
        d=gcd(b-1,n)

        if 1<d<n:
            return d

    return -1


if __name__=="__main__":
    n=11*12*13
    print(pollard_p1_stage2(n,20,200))

