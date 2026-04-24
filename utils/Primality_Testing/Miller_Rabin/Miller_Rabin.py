""" 实现Miller-Rabin算法
具体步骤如下:
1.将n-1表示为n-1 = 2^* m
2.随机选取a,满足1<a<n-1
3.计算b = a^m mod n
4.如果b = 1 mod n,输出n为素数
5.执行循环
    for i in range(l):
        if b = -1 mod n:
            return True
        b = b**2
    return False
6.循环结束则输出n为合数
"""

import random
import time

def Miller_Rabin(n:int,k = 5)->bool:
    n_1 = n - 1
    # 获取n-1 = 2^l * m
    l = 0
    while n_1 % 2 == 0:
        l+=1
        n_1 //= 2
    m = n_1

    # 先随机选取整数a,满足 1 < a < n-1
    # 这里如果遍历a in (1,n-1)就浪费时间了
    # 因为是随机算法,又不能只测一个,因此这里测试k个
    k = min(k,n)
    for _ in range(k):
        a = random.randint(2,n)
        b = pow(a,m,n) # python中pow内置实现了快速幂,比b = (a**m) % n更高效
        if b == 1:
            return True 
        else:
            for _ in range(l-1):
                if b == n-1:
                    return True
                b = pow(b,2,n)
            return False
        
def generate_random_int(bits):
    # 产生bits位随机数
    n = random.getrandbits(bits)
    n |= (1<<(bits-1))
    n |= 1
    return n


def test(bits,rounds = 10):
    # 测试函数,bit指代位数(2048,4096),rounds表示运行轮数,在此基础上算平均值
    print("="*20,f"Start to test {bits}-bit data(rounds:{rounds})...","="*20)
    total = 0
    for _ in range(rounds):
        n = generate_random_int(bits)
        start = time.time()
        result = Miller_Rabin(n,k = 10) # 数大,选取的n的个数也增大点
        end = time.time()

        print(f"{bits}-bit:{end-start:.6f}s,result = {result}")
        
        total += end-start
    print(f"Average run time:{total/rounds:.6f}")
if __name__ == "__main__":
    test(2048)
    test(4096)