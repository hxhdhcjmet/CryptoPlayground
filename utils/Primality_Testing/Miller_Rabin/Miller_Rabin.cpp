#include <gmpxx.h>
#include <iostream>
#include <chrono>

using namespace std;

// 生成 bits 位随机奇数
mpz_class random_odd(int bits) {
    gmp_randclass rng(gmp_randinit_default);
    rng.seed(time(NULL));

    mpz_class n = rng.get_z_bits(bits);
    mpz_setbit(n.get_mpz_t(), bits - 1); // 保证位数
    mpz_setbit(n.get_mpz_t(), 0);        // 保证奇数
    return n;
}

bool miller_rabin(mpz_class n, int k) {
    if (n < 2) return false;

    mpz_class m = n - 1;
    int l = 0;

    while (m % 2 == 0) {
        m /= 2;
        l++;
    }

    gmp_randclass rng(gmp_randinit_default);
    rng.seed(time(NULL));

    for (int i = 0; i < k; i++) {
        mpz_class a = rng.get_z_range(n - 3) + 2;

        mpz_class b;
        mpz_powm(b.get_mpz_t(), a.get_mpz_t(), m.get_mpz_t(), n.get_mpz_t());

        if (b == 1 || b == n - 1) continue;

        bool flag = false;
        for (int j = 0; j < l - 1; j++) {
            mpz_powm_ui(b.get_mpz_t(), b.get_mpz_t(), 2, n.get_mpz_t());
            if (b == n - 1) {
                flag = true;
                break;
            }
        }

        if (!flag) return false;
    }

    return true;
}

void test(int bits,int rounds = 10) {
    cout<<"Start to test"<<bits<<"-bit data(rounds:"<< rounds <<")..."<<endl;
    chrono::duration<double> total{0};
    for (int i = 0;i < rounds;i++){ 
    mpz_class n = random_odd(bits);

    auto start = chrono::high_resolution_clock::now();
    bool result = miller_rabin(n, 10);
    auto end = chrono::high_resolution_clock::now();

    chrono::duration<double> diff = end - start;
    total += diff;

    cout << bits << "-bit: " << diff.count() << " s, result=" << result << endl;
    }
    cout<<"Average run time:"<<total.count() / rounds<<endl;
}

int main() {
    test(2048);
    test(4096);
    return 0;
}