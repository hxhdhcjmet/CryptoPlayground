"""
Pohlig-Hellman算法
假设阶n可以被有效分解:n = q_1^{c_1}q_2^{c_2}...q_t^{c_t}
log_g X mod n 可以转成方程组
====================
log_g Xmod q_1^{c_1}
log_g Xmod q_2^{c_2}
.
.
.
log_g X Xmod q_t^{c_t}
上述的解用CRT合成最终解即可得到log_g X mod n
上述每一个式子都是求解较小模的离散对数问题,即
a = log_g X mod q^c

令a = a_0 + a_1q + ... + a_{c-1}q^{c-1} mod q^c
所以log_g X mod n = a+q^c  nS
a_0满足等式:X^{n/q} = g^{a_0n /q}
在[0,q-1]范围内搜索a_i,正确a_i满足面式子

X_i = Xg^-{a_0 + a_1q + ... + a_{i-1}q^{i-1}} = X_{i-1}g^{-a_{i-1}q^{i-1}}
再次利用X_i^{n / q_{i+1}} = g^{na_i/q}搜索a_i
"""

from math import ceil,sqrt
class PohligHellman:
    def __init__(self,p:int,a:int,y:int):
        """
        求解 y = a^x mod p
        """
        self.p = p
        self.a = a % p
        self.y = y % p
        self.n = p-1 # 群的阶
    
    # 扩展欧几里得算法求gcd和模逆
    def _extended_gcd(self, a, b):
        old_r, r = a, b
        old_s, s = 1, 0
        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
        return old_r, old_s

    def _mod_inverse(self, n, m):
        gcd, x = self._extended_gcd(n, m)
        if gcd != 1: raise Exception("模逆不存在")
        return x % m
    
    def _get_prime_factors(self, n):
        """
        简单素因子分解
        """
        factors = {}
        d = 2
        temp = n
        while d * d <= temp:
            while temp % d == 0:
                factors[d] = factors.get(d, 0) + 1
                temp //= d
            d += 1
        if temp > 1:
            factors[temp] = factors.get(temp, 0) + 1
        return factors

    def _CRT(self, items):
        """
        CRT合并,迭代参数形式为[(a,m)...]
        """
        N = 1
        for _, m in items: N *= m
        result = 0
        for r, m in items:
            Ni = N // m
            inv = self._mod_inverse(Ni, m)
            result += r * Ni * inv
        return result % N

    def _solve_by_digits(self,q,e):
        # 穷搜求解小的离散对数:mod q^e
        gamma = pow(self.a,self.n//q,self.p)
        x = 0
        a_inv = self._mod_inverse(self.a,self.p) # 求a^{-1} mod p

        for k in range(e):
            # 利用性质(y*a^{-x}^(n / q^{k+1})) = gamma^{a_k}
            power = self.n // (q**(k+1))
            target = pow(self.y * pow(a_inv, x, self.p), power, self.p)

            # 在[0,q-1]内穷搜a_k
            found_ak = None
            for ak in range(q):
                if pow(gamma,ak,self.p) == target:
                    found_ak = ak
                    break
            
            if found_ak is None:return None
            x += found_ak * (q**k)
        return x
    

    def _solve_by_bsgs(self,g_sub,h_sub,sub_order):
        # 小步大步法求解小模下的离散对数问题
        m = ceil(sqrt(sub_order))
        baby_steps  = {}
        curr = 1
        for i in range(m):
            baby_steps[curr] = i
            curr = (curr*g_sub) % self.p
        
        g_inv_m = self._mod_inverse(pow(g_sub,m,self.p),self.p)
        giant_step = h_sub
        for j in range(m):
            if giant_step in baby_steps:
                return j * m + baby_steps[giant_step]
            giant_step = (giant_step * g_inv_m) % self.p
        return None

    
    def solve(self,method = "digit"):
        factors = self._get_prime_factors(self.n) # 对n作因子分解
        crt_items = []


        for q,e in factors.items():
            qe = q**e
            if method == "digit":
                xi = self._solve_by_digits(q,e)
            else:
                # BSGS求解
                gi = pow(self.a,self.n // qe,self.p)
                hi = pow(self.y,self.n // qe,self.p)
                xi = self._solve_by_bsgs(gi,hi,qe)
            crt_items.append((xi,qe))
        
        return self._CRT(crt_items)
    
if __name__ == "__main__":
    # 测试例题
    p1,a1,b1 = 41,6,29
    s1 = PohligHellman(p1,a1,b1)
    print(f"方程{b1} = {a1}^x mod {p1}的解为:")
    print(f"x = log_{a1}^{b1} = {s1.solve()}")

    p2,a2,b2 = 37,2,29
    s2 = PohligHellman(p2,a2,b2)
    print(f"方程{b2} = {a2}^x mod {p2}的解为:")
    print(f"x = log_{a2}^{b2} = {s2.solve(method = 'bsgs')}")



