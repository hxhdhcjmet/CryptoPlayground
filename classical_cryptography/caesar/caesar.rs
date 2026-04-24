/// 凯撒密码加密函数
/// - plaintext: 明文字符串
/// - key: 加密密钥
/// 返回: 加密后的密文字符串
fn caesar_encrypt(plaintext: &str, key: i32) -> String {
    // 密钥标准化：将密钥转换为 0~25 的正数（兼容任意正负密钥）
    let key = ((key % 26) + 26) % 26;
    // 预分配内存，提升效率
    let mut ciphertext = String::with_capacity(plaintext.len());

    // 遍历明文字节（仅处理 ASCII 字符）
    for &byte in plaintext.as_bytes() {
        match byte {
            // 大写字母 A-Z 循环移位
            b'A'..=b'Z' => {
                let shifted = (byte - b'A') as i32 + key;
                ciphertext.push((b'A' + (shifted % 26) as u8) as char);
            }
            // 小写字母 a-z 循环移位
            b'a'..=b'z' => {
                let shifted = (byte - b'a') as i32 + key;
                ciphertext.push((b'a' + (shifted % 26) as u8) as char);
            }
            // 非字母字符：直接保留，不修改
            _ => ciphertext.push(byte as char),
        }
    }

    ciphertext
}

/// 凯撒密码解密函数
/// 解密 = 反向加密（密钥取负）
fn caesar_decrypt(ciphertext: &str, key: i32) -> String {
    caesar_encrypt(ciphertext, -key)
}

fn main() {
    // 密钥（29 % 26 = 3，等效于密钥 3）
    let key = 29;
    // 明文
    let plaintext = "hhhhhaaaaa";

    // 打印原文
    println!("原文: {}", plaintext);
    // 加密
    let ciphertext = caesar_encrypt(plaintext, key);
    println!("加密后: {}", ciphertext);
    // 解密
    let decrypted_text = caesar_decrypt(&ciphertext, key);
    println!("解密后: {}", decrypted_text);
}