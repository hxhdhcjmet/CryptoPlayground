"""
试除法实现因子分解
实现简单但效率低下,实际能处理的位数优先
"""
from math import sqrt

SHORT_PRIMES = [2, 3, 5, 7, 11, 13, 17]  # 定义一些小素数
def factorize(n: int) -> list:
    if n <= 1:
        return []

    factors = []
    # 先取出所有2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    queue = [n] if n > 1 else []
    while queue:
        curr = queue.pop()  # 取一个来判断并处理
        if curr <= 1:
            continue
        if curr in SHORT_PRIMES:
            factors.append(curr)
            continue

        is_prime = True  # 判断过了一遍是不是有因子, 有就加入队列, 没有就加入因子
        limit = int(sqrt(curr)) + 1
        for i in range(3, limit, 2):
            if curr % i == 0:
                queue.append(i)
                queue.append(curr // i)
                is_prime = False
                break

        if is_prime:
            factors.append(curr)

    return sorted(factors)



def multply(factors:list):
    n = 1
    for factor in factors:
        n*=factor
    return n

if __name__ == "__main__":
    n = 114514
    factors = factorize(n)
    print(factors)
    print(multply(factors))

