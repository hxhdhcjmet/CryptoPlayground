# AES加密算法实现

# 为了实现速度,一般直接计算好各种输入过S盒后的结果,实际计算时直接查表
S = (0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16)

S_INV = (0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D)

def creat_subbytes_table()->tuple:
    # 输入8bit共2^8
    subbytes = {}
    subbytes_inv = {}
    for k in range(2**8):
        # 转8长二进制
        k = f"{k:08b}"
        row = k[:4]
        col = k[4:]
        pos = int(row,2) * 16 + int(col,2)
        subbytes[k] = S[pos]
        subbytes_inv[k] = S_INV[pos]
    
    return subbytes,subbytes_inv

SUBBYTES ,SUBBYTES_INV = creat_subbytes_table() # 提前创建好表格


def xtimes()->dict:
    x2 = {}
    # 在GF(2^8)上做乘2，提前算好，实际aes加密时直接查表
    for x in range(2**8):
        # 左移一位,如果最高位为1则与0x1B做异或
        value = (x << 1) ^ (0x1B if x & 0x80 else 0)
        x2[x] = value & 0xFF  # 保持在8位范围内
    return x2

X2 = xtimes()


# Rcon常量 - AES128需要10个轮常数
RCON = (0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36)

class aes128:
    def __init__(self,k:bytes,m:bytes) -> None:
        if not isinstance(k,bytes):
            raise TypeError("密钥需要为字节类型")
        if not isinstance(m,bytes):
            raise TypeError("明文需要为字节类型")
        key_len = len(k)
        if key_len != 16:  # 128位 = 16字节
            raise ValueError("密钥长度必须为16字节(128位)")
        if len(m) != 16:
            raise ValueError("明文长度必须为16字节(128位)")
        # 明文m,密钥k,明文m假定为一组的128-bit
        self.m = m
        self.matrix_m = self._bytes2matrix() # 转为矩阵
        # 直接使用列优先矩阵
        self.ciphertext = [row[:] for row in self.matrix_m]
        self.k = k
        self.matrix = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]] # Mixcolumns所用矩阵
        self.matrix_inv = [[0x0E,0x0B,0x0D,0x09],[0x09,0x0E,0x0B,0x0D],[0x0D,0x09,0x0E,0x0B],[0x0B,0x0D,0x09,0x0E]]  # Mixcolums逆所用的矩阵
        # 生成所有轮密钥
        self.round_keys = self._generate_key()



    def _bytes2matrix(self, data: bytes = None) -> list:
        # 将16字节转为4*4的矩阵（列优先）
        if data is None:
            data = self.m
        if not isinstance(data, (bytes, bytearray)) or len(data) != 16:
            raise ValueError("输入数据必须为16字节")

        matrix = []
        for row in range(4):
            matrix.append([data[row + 4*col] for col in range(4)])
        return matrix

    def _matrix2bytes(self, matrix: list) -> bytes:
        result = []
        for col in range(4):
            for row in range(4):
                result.append(matrix[row][col])
        return bytes(result)

    def _gf_mul(self, a: int, x: int) -> int:
        if a == 1:
            return x
        if a == 2:
            return X2[x]
        if a == 3:
            return X2[x] ^ x
        if a == 9:
            return X2[X2[X2[x]]] ^ x
        if a == 0x0B:
            return X2[X2[X2[x]]] ^ X2[x] ^ x
        if a == 0x0D:
            return X2[X2[X2[x]]] ^ X2[X2[x]] ^ x
        if a == 0x0E:
            return X2[X2[X2[x]]] ^ X2[X2[x]] ^ X2[x]
        raise ValueError(f"不支持的GF(2^8)系数: {a}")

    def _generate_key(self):
        # 生成所有密钥,共需要11组轮密钥（AES128需要10轮加密+1个初始轮密钥）
        # 每组128bit密钥分为4个密钥字(word)，每个字32位(4字节)
        # 总共需要44个字: w[0]...w[43]
        w = []
        
        # 初始密钥的4个字（列优先）
        for i in range(4):
            w.append([self.k[4*i], self.k[4*i+1], self.k[4*i+2], self.k[4*i+3]])
        
        # 扩展密钥
        for i in range(4, 44):
            temp = w[i-1][:]  # 复制上一个字
            if i % 4 == 0:
                # RotWord: 循环左移1字节
                temp = temp[1:] + temp[:1]
                # SubWord: 对每个字节应用S盒
                temp = [S[b] for b in temp]
                # 异或Rcon
                rcon_index = (i // 4) - 1
                temp[0] ^= RCON[rcon_index]
            
            # w[i] = w[i-4] ^ temp
            w.append([w[i-4][j] ^ temp[j] for j in range(4)])
        
        # 将44个字重组为11个轮密钥(每个轮密钥4x4矩阵，按行组织)
        round_keys = []
        for r in range(11):
            # 每个轮密钥由4个连续的字组成，转为行矩阵
            rk = []
            for row in range(4):
                rk.append([w[r*4 + col][row] for col in range(4)])
            round_keys.append(rk)
        
        return round_keys



    #================================================
    #加密:先与轮密钥相加->| 过S盒->行移位->列混合->轮密钥相加 |*9 -> 过S盒->行移位->轮密钥相加 ->密文
    #================================================
    def _SubBytes(self):
        # 过S盒
        for i in range(4):
            for j in range(4):
                B = self.ciphertext[i][j]
                self.ciphertext[i][j] = S[B]  # 直接用S盒查表更简单

    
    def _ShiftRows(self):
        # 行移位:第i行左移i个位置
        for i in range(4):
            self.ciphertext[i] = self.ciphertext[i][i:] + self.ciphertext[i][:i]

    
    def _MixColumns(self):
        # 列混合,整列与矩阵做乘法,4列进4列出
        for col_idx in range(4):
            curr_col = [self.ciphertext[row][col_idx] for row in range(4)]
            curr_col_result = []

            for row in self.matrix:
                curr_result = [self._gf_mul(a, x) for a, x in zip(row, curr_col)]
                curr = curr_result[0]
                for i in range(1, 4):
                    curr ^= curr_result[i]
                curr_col_result.append(curr)

            for row in range(4):
                self.ciphertext[row][col_idx] = curr_col_result[row]

    def _AddRoundKey(self, round_key):
        # 异或轮密钥
        for i in range(4):
            for j in range(4):
                self.ciphertext[i][j] ^= round_key[i][j]
    
    def encrypt(self):
        """执行完整的AES128加密"""
        self.ciphertext = self._bytes2matrix(self.m)
        # 初始轮密钥加
        self._AddRoundKey(self.round_keys[0])
        
        # 前9轮: SubBytes -> ShiftRows -> MixColumns -> AddRoundKey
        for round_num in range(1, 10):
            self._SubBytes()
            self._ShiftRows()
            self._MixColumns()
            self._AddRoundKey(self.round_keys[round_num])
        
        # 第10轮(最后一轮): SubBytes -> ShiftRows -> AddRoundKey (无MixColumns)
        self._SubBytes()
        self._ShiftRows()
        self._AddRoundKey(self.round_keys[10])
        
        return self._matrix2bytes(self.ciphertext)
    

    #====================解密======================
    #可以将输入的m看作密文,密文同样为128bit,这里使用为
    # aes = aes128(k,input)
    # 单加密:c = aes.encrypt()
    # 单解密:m = aes.decrypt()
    # 解密先异或轮密钥,|行移位的逆->过S盒的逆->轮密钥相加->列混合的逆| * 9 ->|行移位的逆->过S盒的逆->轮密钥相加|->m
    # 等价软硬件实现的提速方法:轮密钥相加->|过S盒的逆->行移位的逆->列混合的逆->等级轮密钥相加|-> * 9 ->|过S盒->行移位的逆->轮密钥相加|->m
    #=============================================
    def _ShiftRowsInv(self):
        for i in range(4):
            self.ciphertext[i] = self.ciphertext[i][-i:] + self.ciphertext[i][:-i]

    def _SubBytesInv(self):
        # 过S盒的逆
        for i in range(4):
            for j in range(4):
                B = self.ciphertext[i][j]
                self.ciphertext[i][j] = S_INV[B]  

    def _MixColumnsInv(self):
        # 列混合的逆
        for col_idx in range(4):
            curr_col = [self.ciphertext[row][col_idx] for row in range(4)]
            curr_col_result = []

            for row in self.matrix_inv:
                curr_result = [self._gf_mul(a, x) for a, x in zip(row, curr_col)]
                curr = curr_result[0]
                for i in range(1, 4):
                    curr ^= curr_result[i]
                curr_col_result.append(curr)

            for row in range(4):
                self.ciphertext[row][col_idx] = curr_col_result[row]
    
    # 轮密钥相加不用重新实现，只需要调换加密钥的顺序
    def decrypt(self):
        self.ciphertext = self._bytes2matrix(self.m)
        self._AddRoundKey(self.round_keys[10])

        for round_num in range(9, 0, -1):
            self._ShiftRowsInv()
            self._SubBytesInv()
            self._AddRoundKey(self.round_keys[round_num])
            self._MixColumnsInv()

        self._ShiftRowsInv()
        self._SubBytesInv()
        self._AddRoundKey(self.round_keys[0])

        return self._matrix2bytes(self.ciphertext)





if __name__ == "__main__":
    # 测试AES128加密
    # 使用NIST标准测试向量
    # 密钥: 2b7e151628aed2a6abf7158809cf4f3c
    # 明文: 3243f6a8885a308d313198a2e0370734
    # 期望密文: 3925841d02dc09fbdc118597196a0b32
    
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    plaintext = bytes.fromhex("3243f6a8885a308d313198a2e0370734")
    expected = bytes.fromhex("3925841d02dc09fbdc118597196a0b32")
    
    print("AES128加密测试")
    print("=" * 50)
    print(f"密钥:     {key.hex()}")
    print(f"明文:     {plaintext.hex()}")
    print(f"期望密文: {expected.hex()}")
    
    # 执行加密
    aes = aes128(key, plaintext)
    ciphertext = aes.encrypt()
    
    print(f"实际密文: {ciphertext.hex()}")
    print("=" * 50)
    
    if ciphertext == expected:
        print("✓ 测试通过! 加密结果正确!")
    else:
        print("✗ 测试失败! 加密结果不匹配!")

    # 解密测试
    decrypted = aes128(key, ciphertext).decrypt()
    print(f"解密结果: {decrypted.hex()}")
    if decrypted == plaintext:
        print("✓ 解密测试通过! 明文恢复正确!")
    else:
        print("✗ 解密测试失败! 明文恢复不正确!")
    
    # 额外测试
    print("\n自定义测试:")
    key2 = b"YELLOW SUBMARINE"  # 16字节密钥
    plaintext2 = b"Hello AES128!!!!"  # 16字节明文
    
    print(f"密钥:     {key2}")
    print(f"明文:     {plaintext2}")
    
    aes2 = aes128(key2, plaintext2)
    ciphertext2 = aes2.encrypt()
    
    print(f"密文(hex): {ciphertext2.hex()}")
    decrypted2 = aes128(key2, ciphertext2).decrypt()
    print(f"解密结果: {decrypted2}")


    print("\n测试二:")
    key3 = b"abcdefghhgfedcba"
    ciphertext3 = b"hello,world,haha"
    aes3 = aes128(key3,ciphertext3)
    m = aes3.encrypt()
    print(f"加密结果:{m.hex()}")
    print(f"解密结果:{aes128(key3,m).decrypt().decode()}")

