from math import gcd
import random


def char_to_ascii(text):
    num_arr = []
    for char in text:
        num_arr.append(ord(char))
    return num_arr


def encrypt(text, e, n):
    ascii_arr = char_to_ascii(text)
    enc_arr = []
    for num in ascii_arr:
        c = (num ** e) % n
        enc_arr.append(c)
    return enc_arr


def decrypt(enc_arr, d, n):
    dec_text = ''
    for num in enc_arr:
        _ascii = (num ** d) % n
        dec_text += chr(_ascii)
    return dec_text


def get_primes(start, stop):
    if start >= stop:
        return []
    primes = [2]
    for n in range(3, stop + 1, 2):
        for p in primes:
            if n % p == 0:
                break
        else:
            primes.append(n)

    while primes and primes[0] < start:
        del primes[0]
    return primes


def keyCreation(length):
    if length < 4:
        raise ValueError('cannot generate a key of length less '
                         'than 4 (got {!r})'.format(length))

    start = 1 << (length // 2 - 1)
    stop = 1 << (length // 2 + 1)
    primes = get_primes(start, stop)

    n_min = 1 << (length - 1)
    n_max = (1 << length) - 1
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_candidates = [q for q in primes
                        if n_min <= p * q <= n_max]
        if q_candidates:
            q = random.choice(q_candidates)
            break

    m = (p - 1) * (q - 1)
    e = 3
    while gcd(e, m) != 1:
        e += 2

    d = 1
    while (e * d) % m != 1:
        d += 1

    print("p:", p, ", q:", q)
    return p * q, e, d


if __name__ == "__main__":
    text = "simmaksim18102001slizh"
    n, e, d = keyCreation(10)
    res = encrypt(text, e, n)
    back = decrypt(res, d, n)
    print("Encryption result : ", res)
    print("Decryption result: ", back)
