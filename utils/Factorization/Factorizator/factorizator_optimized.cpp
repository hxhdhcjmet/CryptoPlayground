#include <NTL/ZZ.h>
#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <chrono>
#include <string>

using namespace std;
using namespace NTL;

// GCD 实现
ZZ gcdZZ(ZZ a, ZZ b) {
    while (b != 0) {
        ZZ t = a % b;
        a = b;
        b = t;
    }
    return abs(a);
}

// 十六进制转 ZZ
ZZ hex_to_ZZ(string s) {
    if (s.size() >= 2 && s[0] == '0' && (s[1] == 'x' || s[1] == 'X'))
        s = s.substr(2);
    ZZ x(0);
    for (char c : s) {
        x *= 16;
        if ('0' <= c && c <= '9') x += (c - '0');
        else if ('a' <= c && c <= 'f') x += (c - 'a' + 10);
        else if ('A' <= c && c <= 'F') x += (c - 'A' + 10);
    }
    return x;
}

// Miller-Rabin 素性检验
bool miller_rabin(const ZZ& n, int rounds = 10) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;

    ZZ d = n - 1;
    long s = 0;
    while (d % 2 == 0) {
        d /= 2;
        s++;
    }

    static const long bases[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29};
    for (int i = 0; i < rounds; i++) {
        ZZ a = conv<ZZ>(bases[i % 10]);
        if (a >= n - 1) a = 2 + (RandomBnd(n - 4)); 

        ZZ x = PowerMod(a, d, n);
        if (x == 1 || x == n - 1) continue;

        bool composite = true;
        for (long r = 1; r < s; r++) {
            x = MulMod(x, x, n);
            if (x == n - 1) {
                composite = false;
                break;
            }
        }
        if (composite) return false;
    }
    return true;
}

// 试除法
void trial_division(ZZ& n, vector<ZZ>& fac) {
    static const long small_primes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (long p : small_primes) {
        ZZ P(p);
        while (n > 1 && n % P == 0) {
            fac.push_back(P);
            n /= P;
        }
    }
}

// Pollard's Rho (Brent + 累计GCD)
ZZ pollard_rho_brent(const ZZ& n) {
    if (n % 2 == 0) return ZZ(2);
    if (miller_rabin(n)) return n;

    while (true) {
        ZZ y = RandomBnd(n - 1) + 1;
        ZZ c = RandomBnd(n - 1) + 1;
        long m = 128; // 这里的 m 应该是一个固定的 long 型步长
        ZZ g(1), r(1), q(1);
        ZZ x, ys;

        while (g == 1) {
            x = y;
            for (long i = 0; i < r; i++)
                y = (MulMod(y, y, n) + c) % n;

            long k = 0;
            while (k < r && g == 1) {
                ys = y;
                long batch = min(m, conv<long>(r) - k);
                for (long i = 0; i < batch; i++) {
                    y = (MulMod(y, y, n) + c) % n;
                    q = MulMod(q, abs(x - y), n);
                }
                g = gcdZZ(q, n);
                k += batch;
            }
            r *= 2;
        }

        if (g == n) {
            do {
                ys = (MulMod(ys, ys, n) + c) % n;
                g = gcdZZ(abs(x - ys), n);
            } while (g == 1);
        }

        if (g != n) return g;
    }
}

// 迭代分解器
vector<ZZ> factorize(ZZ n) {
    vector<ZZ> factors;
    trial_division(n, factors);
    if (n == 1) return factors;

    vector<ZZ> stack;
    stack.push_back(n);

    while (!stack.empty()) {
        ZZ curr = stack.back();
        stack.pop_back();

        if (miller_rabin(curr)) {
            factors.push_back(curr);
            continue;
        }

        ZZ d = pollard_rho_brent(curr);
        stack.push_back(d);
        stack.push_back(curr / d);
    }
    sort(factors.begin(), factors.end());
    return factors;
}
// 辅助函数：将 ZZ 转为 16 进制字符串
string ZZ_to_hex(ZZ n) {
    if (n == 0) return "0";
    string hex_str = "";
    string chars = "0123456789ABCDEF";
    ZZ temp = n;
    while (temp > 0) {
        long rem = conv<long>(temp % 16);
        hex_str += chars[rem];
        temp /= 16;
    }
    reverse(hex_str.begin(), hex_str.end());
    return hex_str;
}

int main() {
    string s = "22F4AE6C291EC7B8A534F0D9B13C020D26";
    ZZ n = hex_to_ZZ(s);

    auto start = chrono::high_resolution_clock::now();
    vector<ZZ> facs = factorize(n);
    auto end = chrono::high_resolution_clock::now();

    map<ZZ, int> counts;
    for (auto& f : facs) counts[f]++;

    cout << "n = 0x" << s << endl; // 保持输入的十六进制显示
    cout << "Factorization: ";
    for (auto it = counts.begin(); it != counts.end(); ++it) {
        if (it != counts.begin()) cout << " * ";
        // 调用转换函数输出十六进制
        cout << "0x" << ZZ_to_hex(it->first); 
        if (it->second > 1) cout << "^" << it->second;
    }
    cout << "\nTime: " << chrono::duration<double>(end - start).count() << "s" << endl;

    return 0;
}

// int main() {
//     string s = "22F4AE6C291EC7B8A534F0D9B13C020D26";
//     ZZ n = hex_to_ZZ(s);

//     auto start = chrono::high_resolution_clock::now();
//     vector<ZZ> facs = factorize(n);
//     auto end = chrono::high_resolution_clock::now();

//     map<ZZ, int> counts;
//     for (auto& f : facs) counts[f]++;

//     cout << "n = " << n << endl;
//     cout << "Factorization: ";
//     for (auto it = counts.begin(); it != counts.end(); ++it) {
//         if (it != counts.begin()) cout << " * ";
//         cout << it->first << (it->second > 1 ? "^" + to_string(it->second) : "");
//     }
//     cout << "\nTime: " << chrono::duration<double>(end - start).count() << "s" << endl;

//     return 0;
// }