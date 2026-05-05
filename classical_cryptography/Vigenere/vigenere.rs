/// Vigenere(维吉尼亚)密码 Rust 实现:
/// 将明文按照密钥分组,实现相同明文字符能加密得到不同的密文字符
pub struct Vigenere {
    key: String,
}

impl Vigenere {
    /// 创建一个新的维吉尼亚密码实例
    /// - key: 密钥字符串（仅字母有效，大小写不敏感）
    pub fn new(key: &str) -> Self {
        assert!(
            key.chars().all(|c| c.is_ascii_alphabetic()),
            "key 必须是纯字母字符串"
        );
        Vigenere {
            key: key.to_lowercase(),
        }
    }

    /// 加密函数
    /// - plaintext: 明文字符串
    /// 返回: 加密后的密文字符串
    pub fn encrypt(&self, plaintext: &str) -> String {
        let key_bytes = self.key.as_bytes();
        let key_len = key_bytes.len();
        let mut key_index = 0;
        let mut ciphertext = String::with_capacity(plaintext.len());

        for &byte in plaintext.as_bytes() {
            match byte {
                // 大写字母 A-Z
                b'A'..=b'Z' => {
                    let k = key_bytes[key_index % key_len] - b'a';
                    let shifted = (byte - b'A') as i32 + k as i32;
                    ciphertext.push((b'A' + (shifted % 26) as u8) as char);
                    key_index += 1;
                }
                // 小写字母 a-z
                b'a'..=b'z' => {
                    let k = key_bytes[key_index % key_len] - b'a';
                    let shifted = (byte - b'a') as i32 + k as i32;
                    ciphertext.push((b'a' + (shifted % 26) as u8) as char);
                    key_index += 1;
                }
                // 非字母字符：直接保留，不消耗密钥位置
                _ => ciphertext.push(byte as char),
            }
        }

        ciphertext
    }

    /// 解密函数
    /// - ciphertext: 密文字符串
    /// 返回: 解密后的明文字符串
    pub fn decrypt(&self, ciphertext: &str) -> String {
        let key_bytes = self.key.as_bytes();
        let key_len = key_bytes.len();
        let mut key_index = 0;
        let mut plaintext = String::with_capacity(ciphertext.len());

        for &byte in ciphertext.as_bytes() {
            match byte {
                // 大写字母 A-Z
                b'A'..=b'Z' => {
                    let k = key_bytes[key_index % key_len] - b'a';
                    let shifted = (byte - b'A') as i32 - k as i32;
                    // 确保非负取模
                    let shifted = ((shifted % 26) + 26) % 26;
                    plaintext.push((b'A' + shifted as u8) as char);
                    key_index += 1;
                }
                // 小写字母 a-z
                b'a'..=b'z' => {
                    let k = key_bytes[key_index % key_len] - b'a';
                    let shifted = (byte - b'a') as i32 - k as i32;
                    let shifted = ((shifted % 26) + 26) % 26;
                    plaintext.push((b'a' + shifted as u8) as char);
                    key_index += 1;
                }
                // 非字母字符：直接保留
                _ => plaintext.push(byte as char),
            }
        }

        plaintext
    }
}

fn main() {
    let key = "hello";
    let plaintext = "hello,what's your name?";

    let vigenere = Vigenere::new(key);

    println!("原文: {}", plaintext);
    println!("密钥: {}", key);

    let ciphertext = vigenere.encrypt(plaintext);
    println!("加密后: {}", ciphertext);

    let decrypted = vigenere.decrypt(&ciphertext);
    println!("解密后: {}", decrypted);
}
