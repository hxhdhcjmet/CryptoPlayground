
use num_bigint::{BigUint, RandBigInt};
use num_traits::{One, Zero};
use rand::thread_rng;
use std::time::Instant;

fn random_odd(bits: usize) -> BigUint {
    let mut rng = thread_rng();
    let mut n = rng.gen_biguint(bits);
    n.set_bit(bits - 1, true);
    n.set_bit(0, true);
    n
}

fn miller_rabin(n: &BigUint, k: u32) -> bool {
    let one = BigUint::one();
    let two = &one + &one;

    let mut m = n - &one;
    let mut l = 0;

    while &m % &two == Zero::zero() {
        m /= &two;
        l += 1;
    }

    let mut rng = thread_rng();

    for _ in 0..k {
        let a = rng.gen_biguint_range(&two, &(n - &two));
        let mut b = a.modpow(&m, n);

        if b == one || b == n - &one {
            continue;
        }

        let mut flag = false;
        for _ in 0..l - 1 {
            b = b.modpow(&two, n);
            if b == n - &one {
                flag = true;
                break;
            }
        }

        if !flag {
            return false;
        }
    }

    true
}

fn test(bits: usize) {
    let n = random_odd(bits);

    let start = Instant::now();
    let result = miller_rabin(&n, 10);
    let duration = start.elapsed();

    println!("{}-bit: {:?}, result={}", bits, duration, result);
}

fn main() {
    test(1024);
    test(2048);
    test(4096);
}