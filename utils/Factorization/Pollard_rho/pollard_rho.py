"""
pollard rho 算法
寻找x_1 ≠ x_2 mod n,x_1 = x_2 mod p
此时p | x_1 - x_2 
gcd(x-1 -x_2,n) = p
关键在于找碰撞对x_1,x_2=>关键在于构造随机映射函数f:Z_n -> Z_n,这里简单利用多项式实现
"""
import math
import random

def gcd(a,b):
    while b:
        a,b=b,a%b
    return a

def pollar_rho(n:int)->int:
    # f = x^2 + c
    if n % 2 == 0:
        return 2
    
    # 这里死循环或者尝试指定次数次
    for _ in range(1000):
    # while True:
        x_1 = random.randint(1,n)
        x_2 = x_1
        d = 1
        c = random.randint(1,n)

        f = lambda x: (x^2 + c) % n

        while d == 1:
            x_1 = f(x_1)
            x_2 = f(f(x_2))
            d = gcd(abs(x_1 - x_2),n)

            
        if d != n:
            return d
        return -1
        


if __name__ == "__main__":
    n = 11*13*17*19
    print(pollar_rho(n))