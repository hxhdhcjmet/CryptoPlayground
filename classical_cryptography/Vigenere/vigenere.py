"""
Vigenere(维吉尼亚)密码:
将明文按照密钥分组,实现相同明文字符能加密得到不同的密文字符
"""

class Vigenere:
    def __init__(self, key: str):
        if not isinstance(key, str) or not key.isalpha():
            raise ValueError("key 必须是纯字母字符串")

        self.key = key.lower()
        self.key_len = len(self.key)

    def encrypt(self, m: str):
        result = []
        key_index = 0  

        for ch in m:
            if ch.isalpha():
                k = self.key[key_index % self.key_len]

                # 判断大小写基准
                base = ord('A') if ch.isupper() else ord('a')

                # 加密
                curr = chr(base + (ord(ch) - base + ord(k) - ord('a')) % 26)

                result.append(curr)
                key_index += 1  
            else:
                result.append(ch)

        return ''.join(result)

    def decrypt(self, c: str):
        result = []
        key_index = 0

        for ch in c:
            if ch.isalpha():
                k = self.key[key_index % self.key_len]

                base = ord('A') if ch.isupper() else ord('a')

                curr = chr(base + (ord(ch) - base - (ord(k) - ord('a'))) % 26)

                result.append(curr)
                key_index += 1
            else:
                result.append(ch)

        return ''.join(result)




if __name__ == "__main__":
    vigenere = Vigenere(key = "hello")
    c = vigenere.encrypt("hello,what's your name?")
    print(c)
    print(vigenere.decrypt(c))

        