
#include <NTL/ZZ.h>
#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <chrono>
#include <string>

using namespace std;
using namespace NTL;

// =====================================================
// gcd 自实现
// =====================================================
ZZ gcdZZ(ZZ a, ZZ b) {
    while (b != 0) {
        ZZ t = a % b;
        a = b;
        b = t;
    }
    return a;
}

// =====================================================
// 十六进制字符串转 ZZ
// 支持: 0xABCDEF
// =====================================================
ZZ hex_to_ZZ(string s) {

    if (s.size() >= 2 &&
        s[0] == '0' &&
       (s[1] == 'x' || s[1] == 'X'))
        s = s.substr(2);

    ZZ x(0);

    for (char c : s) {

        x *= 16;

        if ('0' <= c && c <= '9')
            x += (c - '0');
        else if ('a' <= c && c <= 'f')
            x += (c - 'a' + 10);
        else if ('A' <= c && c <= 'F')
            x += (c - 'A' + 10);
    }

    return x;
}

// =====================================================
// Miller-Rabin 自实现
// 使用 NTL 的 PowerMod 做模幂
// =====================================================
bool miller_rabin(const ZZ& n, int rounds = 10) {

    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;

    // n-1 = d * 2^s
    ZZ d = n - 1;
    long s = 0;

    while (d % 2 == 0) {
        d /= 2;
        s++;
    }

    long bases[] = {2,3,5,7,11,13,17,19,23,29};

    for (int i = 0; i < rounds; i++) {

        ZZ a = conv<ZZ>(bases[i % 10]);

        if (a >= n - 2)
            a = ZZ(2);

        ZZ x = PowerMod(a, d, n);

        if (x == 1 || x == n - 1)
            continue;

        bool witness = true;

        for (long r = 1; r < s; r++) {

            x = MulMod(x, x, n);

            if (x == n - 1) {
                witness = false;
                break;
            }
        }

        if (witness)
            return false;
    }

    return true;
}

// =====================================================
// 小素数筛
// =====================================================
vector<long> get_primes(long limit = 100000) {

    vector<bool> vis(limit + 1, false);
    vector<long> primes;

    for (long i = 2; i <= limit; i++) {

        if (!vis[i]) {

            primes.push_back(i);

            if (1LL * i * i <= limit) {
                for (long j = i * i; j <= limit; j += i)
                    vis[j] = true;
            }
        }
    }

    return primes;
}

vector<long> SMALL_PRIMES = get_primes();

// =====================================================
// 试除法
// =====================================================
void trial_division(ZZ& n, vector<ZZ>& fac) {

    for (long p : SMALL_PRIMES) {

        ZZ P(p);

        if (P * P > n)
            break;

        while (n % P == 0) {
            fac.push_back(P);
            n /= P;
        }
    }
}

// =====================================================
// Pollard p-1
// =====================================================
ZZ pollard_p1(const ZZ& n, long B1 = 10000) {

    if (n % 2 == 0)
        return ZZ(2);

    ZZ a(2);

    for (long p : SMALL_PRIMES) {

        if (p > B1)
            break;

        long pk = p;

        while (1LL * pk * p <= B1)
            pk *= p;

        a = PowerMod(a, conv<ZZ>(pk), n);
    }

    ZZ d = gcdZZ(a - 1, n);

    if (d > 1 && d < n)
        return d;

    return ZZ(1);
}

// =====================================================
// Pollard Rho
// =====================================================
ZZ pollard_rho(const ZZ& n) {

    if (n % 2 == 0)
        return ZZ(2);

    while (true) {

        ZZ c = RandomBnd(n - 1) + 1;
        ZZ x = RandomBnd(n - 2) + 2;
        ZZ y = x;
        ZZ d(1);

        while (d == 1) {

            x = (MulMod(x, x, n) + c) % n;

            y = (MulMod(y, y, n) + c) % n;
            y = (MulMod(y, y, n) + c) % n;

            d = gcdZZ(abs(x - y), n);
        }

        if (d != n)
            return d;
    }
}

// =====================================================
// 递归分解
// =====================================================
void factor_rec(const ZZ& n, vector<ZZ>& fac) {

    if (n == 1)
        return;

    if (miller_rabin(n)) {
        fac.push_back(n);
        return;
    }

    ZZ d = pollard_p1(n);

    if (d == 1)
        d = pollard_rho(n);

    factor_rec(d, fac);
    factor_rec(n / d, fac);
}

// =====================================================
// 总分解器
// =====================================================
vector<ZZ> factor_all(ZZ n) {

    vector<ZZ> fac;

    trial_division(n, fac);

    if (n > 1)
        factor_rec(n, fac);

    sort(fac.begin(), fac.end());

    return fac;
}

// =====================================================
// 输出
// =====================================================
void print_result(const ZZ& n) {

    auto start = chrono::high_resolution_clock::now();

    vector<ZZ> fac = factor_all(n);

    auto end = chrono::high_resolution_clock::now();

    map<ZZ,int> cnt;

    for (auto &x : fac)
        cnt[x]++;

    cout << "====================================\n";
    cout << "n = " << n << "\n";
    cout << "Prime factorization:\n";

    bool first = true;

    for (auto &kv : cnt) {

        if (!first) cout << " * ";
        first = false;

        cout << kv.first;

        if (kv.second > 1)
            cout << "^" << kv.second;
    }

    cout << "\n";

    double t =
        chrono::duration<double>(end - start).count();

    cout << "Time used: " << t << " sec\n";
    cout << "====================================\n";
}

// =====================================================
// main
// =====================================================
int main() {

    string s = "0x22F4AE6C291EC7B8A534F0D9B13C020D26";

    cout<<"The BIG num is : "<<s<<endl;

    ZZ n;

    if (s.size() >= 2 &&
        s[0] == '0' &&
       (s[1] == 'x' || s[1] == 'X'))
        n = hex_to_ZZ(s);
    else
        n = conv<ZZ>(s.c_str());

    print_result(n);

    return 0;
}

