# RC4流密码
import random 


# 将种子密钥k划分为L个字节循环填充到T中
class RC4:
    def __init__(self,k:bytes) -> None:
        """
        k为密钥
        """
        if not isinstance(k,bytes):
            raise TypeError("密钥必须为字节类型")
        
        self.k_len = len(k)
        if self.k_len < 128:
            raise ValueError("安全密钥长度至少128")
         

        self.j = 0
        self.k = k
        self.init_s = self._update()

        

    def _update(self):
        # 状态更新,初始化
        S = list(range(256))
        for i in range(256):
            self.j = (self.j + S[i] + self.k[i % self.k_len] ) % 256
            S[i],S[self.j] = S[self.j],S[i]
        return S


    def _generate_k(self):
        """
        生成密钥流,现在不使用种子密钥,而是通过更新状态S,生成每个字节k[i]
        """
        S = self.init_s.copy()
        self.a,self.b = 0,0
        while True:
            # 这里用生成器生成密钥
            self.a = (self.a + 1) % 256
            self.b = (self.b + S[self.a]) % 256
            S[self.a],S[self.b] = S[self.b],S[self.a]
            
            yield (S[self.a] + S[self.b]) % 256 # 输出密钥
    
    def encrypt(self,m:bytes)->bytes:
        # 加密算法
        if not isinstance(m,bytes):
            raise TypeError("只能加密字节类型明文")
        
        key_stream = self._generate_k()
        result = bytes([b ^ next(key_stream) for b in m])
        return result
    
    def decrypt(self,c:bytes)->bytes:
        # 解密算法
        if not isinstance(c,bytes):
            raise TypeError("只能解密字节类型密文")
        key_stream = self._generate_k()
        result = bytes([b ^ next(key_stream) for b in c])
        return result
    


if __name__ == "__main__":
    print("开始测试...")
    m = "hello,what's u name".encode()
    k = random.randbytes(128)
    rc4 = RC4(k)
    c = rc4.encrypt(m)
    print(f"明文:{m}")
    print(f"加密后结果:{c}")
    print("开始解密...")
    print(f"解密结果:{rc4.decrypt(c)}")


    



        
