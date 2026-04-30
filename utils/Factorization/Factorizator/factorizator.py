import random
import math
import time
from collections import Counter

# ==========================================================
# High Performance Integer Factorizer (Python)
# Combines:
#   1. Trial Division
#   2. Miller-Rabin primality test
#   3. Pollard p-1
#   4. Pollard Rho
# Recursive full factorization
# ==========================================================


# ----------------------------------------------------------
# gcd
# ----------------------------------------------------------
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)
# Fast modular multiply (Python big int already safe)
# ----------------------------------------------------------
def mul_mod(a, b, mod):
    return (a * b) % mod


# ----------------------------------------------------------
# Miller Rabin primality test
# Deterministic for 64-bit
# Good probabilistic for larger integers
# ----------------------------------------------------------
def is_prime(n: int, rounds=10) -> bool:

    if n < 2:
        return False

    small_primes = [
        2, 3, 5, 7, 11, 13, 17, 19,
        23, 29, 31, 37
    ]

    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    # write n-1 = d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    # deterministic bases for 64-bit
    if n.bit_length() <= 64:
        test_bases = [2, 3, 5, 7, 11, 13, 17]
    else:
        test_bases = [random.randrange(2, n - 2) for _ in range(rounds)]

    for a in test_bases:

        if a % n == 0:
            continue

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        skip = False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                skip = True
                break

        if skip:
            continue

        return False

    return True


# ----------------------------------------------------------
# Prime sieve
# ----------------------------------------------------------
def prime_sieve(limit=100000):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:limit + 1:step] = b"\x00" * (
                ((limit - start) // step) + 1
            )

    return [i for i in range(limit + 1) if sieve[i]]


SMALL_PRIMES = prime_sieve(100000)


# ----------------------------------------------------------
# Trial division
# ----------------------------------------------------------
def trial_division(n: int, factors: list) -> int:

    for p in SMALL_PRIMES:
        if p * p > n:
            break

        while n % p == 0:
            factors.append(p)
            n //= p

    return n


# ----------------------------------------------------------
# Pollard p-1
# ----------------------------------------------------------
def pollard_p1(n: int, B1=10000) -> int:

    if n % 2 == 0:
        return 2

    a = 2

    for p in SMALL_PRIMES:
        if p > B1:
            break

        pk = p
        while pk * p <= B1:
            pk *= p

        a = pow(a, pk, n)

    d = gcd(a - 1, n)

    if 1 < d < n:
        return d

    return 1


# ----------------------------------------------------------
# Pollard Rho
# ----------------------------------------------------------
def pollard_rho(n: int) -> int:

    if n % 2 == 0:
        return 2

    if n % 3 == 0:
        return 3

    while True:

        c = random.randrange(1, n - 1)
        x = random.randrange(2, n - 1)
        y = x
        d = 1

        while d == 1:
            x = (mul_mod(x, x, n) + c) % n
            y = (mul_mod(y, y, n) + c) % n
            y = (mul_mod(y, y, n) + c) % n

            d = gcd(abs(x - y), n)

        if d != n:
            return d


# ----------------------------------------------------------
# Core recursive factorization
# ----------------------------------------------------------
def factor_recursive(n: int, factors: list):

    if n == 1:
        return

    if is_prime(n):
        factors.append(n)
        return

    # first try p-1
    d = pollard_p1(n)

    # fallback to rho
    if d == 1:
        d = pollard_rho(n)

    factor_recursive(d, factors)
    factor_recursive(n // d, factors)


# ----------------------------------------------------------
# Full factorization
# ----------------------------------------------------------
def factor(n: int):

    start = time.perf_counter()

    factors = []

    # trial division first
    n = trial_division(n, factors)

    if n > 1:
        factor_recursive(n, factors)

    factors.sort()

    elapsed = time.perf_counter() - start

    return factors, elapsed


# ----------------------------------------------------------
# Pretty print
# ----------------------------------------------------------
def print_factorization(n: int):

    factors, t = factor(n)

    cnt = Counter(factors)

    parts = []
    for p in sorted(cnt):
        e = cnt[p]
        if e == 1:
            parts.append(str(p))
        else:
            parts.append(f"{p}^{e}")

    print("=" * 60)
    print("n =", n)
    print("Prime Factorization:")
    print(" * ".join(parts))
    print("All factors list:")
    print(factors)
    print(f"Time used: {t:.6f} seconds")
    print("=" * 60)


# ----------------------------------------------------------
# Demo
# ----------------------------------------------------------
if __name__ == "__main__":

    tests = [
        int("22F4AE6C291EC7B8A534F0D9B13C020D26",16)
    ]

    for x in tests:
        print_factorization(x)