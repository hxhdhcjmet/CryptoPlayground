#include <stdio.h>
#include <string.h>
#include <ctype.h>

/*
Vigenere(维吉尼亚)密码 C 语言实现:
将明文按照密钥分组,实现相同明文字符能加密得到不同的密文字符
*/

/**
 * 加密函数
 * @param c       输出密文字符串（需预先分配足够空间）
 * @param m       输入明文字符串
 * @param key     密钥字符串（仅字母有效，大小写不敏感）
 */
void vigenere_encrypt(char *c, const char *m, const char *key) {
    size_t key_len = strlen(key);
    size_t key_index = 0;

    for (size_t i = 0; m[i] != '\0'; i++) {
        if (isalpha((unsigned char)m[i])) {
            // 获取密钥字符（统一转为小写）
            char k = tolower((unsigned char)key[key_index % key_len]);
            // 确保密钥字符是字母
            if (!isalpha((unsigned char)k)) {
                k = 'a';
            }

            // 判断大小写基准
            char base = isupper((unsigned char)m[i]) ? 'A' : 'a';

            // 加密: c = base + (p - base + k - 'a') % 26
            c[i] = (char)(base + (m[i] - base + (tolower((unsigned char)k) - 'a')) % 26);

            key_index++;
        } else {
            c[i] = m[i];
        }
    }
    c[strlen(m)] = '\0';
}

/**
 * 解密函数
 * @param m       输出明文字符串（需预先分配足够空间）
 * @param c       输入密文字符串
 * @param key     密钥字符串（仅字母有效，大小写不敏感）
 */
void vigenere_decrypt(char *m, const char *c, const char *key) {
    size_t key_len = strlen(key);
    size_t key_index = 0;

    for (size_t i = 0; c[i] != '\0'; i++) {
        if (isalpha((unsigned char)c[i])) {
            // 获取密钥字符（统一转为小写）
            char k = tolower((unsigned char)key[key_index % key_len]);
            if (!isalpha((unsigned char)k)) {
                k = 'a';
            }

            // 判断大小写基准
            char base = isupper((unsigned char)c[i]) ? 'A' : 'a';

            // 解密: p = base + (c - base - (k - 'a') + 26) % 26
            int shift = (c[i] - base) - (tolower((unsigned char)k) - 'a');
            shift = (shift % 26 + 26) % 26;  // 确保非负
            m[i] = (char)(base + shift);

            key_index++;
        } else {
            m[i] = c[i];
        }
    }
    m[strlen(c)] = '\0';
}

int main() {
    const char *key = "helloo";
    const char *plaintext = "hello,what's your name?";

    size_t len = strlen(plaintext);
    char ciphertext[len + 1];
    char decrypted[len + 1];

    printf("原文: %s\n", plaintext);
    printf("密钥: %s\n", key);

    vigenere_encrypt(ciphertext, plaintext, key);
    printf("加密后: %s\n", ciphertext);

    vigenere_decrypt(decrypted, ciphertext, key);
    printf("解密后: %s\n", decrypted);

    return 0;
}
