class Elliptic_Curve:
    def __init__(self, a: int, b: int, p: int):
        self.a = a
        self.b = b
        self.p = p
        # 检查判别式
        if (4 * a**3 + 27 * b**2) % p == 0:
            raise ValueError("非法参数:判别式不能为0(曲线存在奇点)")

    def is_inCurve(self, Q: tuple) -> bool:
        if Q is None: return True
        x, y = Q
        return (y**2 - (x**3 + self.a * x + self.b)) % self.p == 0

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

    def add(self, P, Q):
        # 1. 处理无穷远点
        if P is None: return Q
        if Q is None: return P
        
        x1, y1 = P
        x2, y2 = Q

        # 2. 处理 P = -Q 的情况
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        # 3. 计算斜率 l (lambda)
        if P == Q:
            # 点倍运算，分母是 2y1
            if y1 == 0: return None
            num = (3 * x1**2 + self.a) % self.p
            den = self._mod_inverse(2 * y1, self.p)
        else:
            # 点加运算，分母是 x2 - x1
            num = (y2 - y1) % self.p
            den = self._mod_inverse(x2 - x1, self.p)
        
        l = (num * den) % self.p

        # 4. 计算结果点 R
        x3 = (l**2 - x1 - x2) % self.p
        y3 = (l * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def ktimes(self, k, P):
        """快速幂算法 (Double-and-Add)"""
        if not self.is_inCurve(P):
            raise ValueError(f"点{P}不在曲线上")
        
        res = None # 初始化为无穷远点
        temp = P
        
        while k > 0:
            if k & 1: # 如果k是奇数
                res = self.add(res, temp)
            temp = self.add(temp, temp) # 倍乘
            k >>= 1 # 右移一位
        return res

if __name__ == "__main__":
    # 参数
    EC = Elliptic_Curve(0, 2, 163) 
    P = (2, 70)

    # 第一题目
    print("="*50,"题目一","="*50)
    target = (78,86)
    print(f"点{target}是否在曲线上? : {EC.is_inCurve(target)}")
    
    # print("="*100)
    # 搜索x
    print("="*50,"题目二","="*50)
    for x in range(1, 200):
        now_point = EC.ktimes(x,P)
        print(f"{x}P = {now_point}")
        if now_point == target:
            print(f"找到 x = {x}")
            break
    # print("="*100)

    # 题目三
    print("="*50,"题目三","="*50)
    print(f"标量乘结果:100P = {EC.ktimes(100,P)}")