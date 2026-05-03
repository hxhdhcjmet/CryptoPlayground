"""
shanks算法求解离散对数
X = g^{mj+i},m = floor(sqrt(n)),0<= i,j <= m-1,有以下等式
Xg^{-i} = g^{mj}
这里已知g,X,通过分别遍历i,j in [0,m-1]计算Xg^{-i}和g^{mj},形成列表L_1 = {(j,g^mj)}和L_2 = {(i,Xg^{-i})}
搜索满足Xg^{-i} = g^{mj}的i和j,则
log_g X = mj+i
"""
from math import ceil, sqrt

class Shanks:
    def __init__(self, p: int, a: int, y: int):
        if not (isinstance(p, int) and isinstance(a, int) and isinstance(y, int)):
            raise ValueError("参数必须是整数")
        self.p = p  
        self.a = a % p
        self.y = y % p
        self.m = ceil(sqrt(self.p))

    def _extended_gcd(self, a, b):
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1
        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t
        return old_r, old_s, old_t

    def _mod_inverse(self, n, m):
        gcd, x, y = self._extended_gcd(n, m)
        if gcd != 1:
            raise Exception("模逆不存在")
        return x % m

    def solve(self):
        # 1. 婴儿步 (Baby-step): 存储 y * a^(-i) mod p
        # 使用字典实现 O(1) 查找
        # 边算边查
        baby_steps = {}
        a_inv = self._mod_inverse(self.a, self.p)
        
        current_yai = self.y
        for i in range(self.m):
            baby_steps[current_yai] = i
            current_yai = (current_yai * a_inv) % self.p

        # 2. 大步 (Giant-step): 计算 (a^m)^j mod p 并查找
        a_m = pow(self.a, self.m, self.p)
        current_amj = 1
        for j in range(self.m):
            if current_amj in baby_steps:
                i = baby_steps[current_amj]
                return self.m * j + i
            current_amj = (current_amj * a_m) % self.p
            
        return None

# 测试
if __name__ == "__main__":
    # y = 6^x mod 41, y=29
    s1 = Shanks(41, 6, 29)
    print(f"解为: {s1.solve()}")  # 输出应该为 37

    # y = 2^x mod 37, y=29
    s2 = Shanks(37, 2, 29)
    print(f"解为: {s2.solve()}")  # 输出应该为 24