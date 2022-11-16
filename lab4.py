import random
from math import gcd


def jacobi(a, n):
    if a == 0:
        if n == 1:
            return 1
        else:
            return 0
    elif a == -1:
        if n % 2 == 0:
            return 1
        else:
            return -1
    elif a == 1:
        return 1
    elif a == 2:
        if n % 8 == 1 or n % 8 == 7:
            return 1
        elif n % 8 == 3 or n % 8 == 5:
            return -1
    elif a >= n:
        return jacobi(a % n, n)
    elif a % 2 == 0:
        return jacobi(2, n) * jacobi(a // 2, n)
    else:
        if a % 4 == 3 and n % 4 == 3:
            return -1 * jacobi(n, a)
        else:
            return jacobi(n, a)


def SS(num, confidence):
    for i in range(confidence):
        a = random.randint(1, num - 1)
        if gcd(a, num) > 1:
            return False
        if not jacobi(a, num) % num == pow(a, (num - 1) // 2, num):
            return False
    return True


def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1

    while (1):
        g = random.randint(2, p - 1)
        if not (pow(g, (p - 1) // p1, p) == 1):
            if not pow(g, (p - 1) // p2, p) == 1:
                return g


def find_prime(numBits, confidence):
    while (1):
        p = random.randint(2 ** (numBits - 2), 2 ** (numBits - 1))

        while (not SS(p, confidence)):
            p = random.randint(2 ** (numBits - 2), 2 ** (numBits - 1))
            while (p % 2 == 0):
                p = random.randint(2 ** (numBits - 2), 2 ** (numBits - 1))

        p = p * 2 + 1
        if SS(p, confidence):
            return p


def generate_keys(confidence=32):
    p = find_prime(256, confidence)
    g = pow(find_primitive_root(p), 2, p)
    x = random.randint(2, p - 1)
    y = pow(g, x, p)

    publicKey = {'p': p, 'g': g, 'y': y}
    privateKey = {'p': p, 'x': x}

    return privateKey, publicKey


def encrypt(key, plainText):
    z = bytearray(plainText, 'utf-8')

    cipher_pairs = []
    for i in z:
        k = random.randint(2, key['p'] - 1)
        a = pow(key['g'], k, key['p'])
        b = (i * pow(key['y'], k, key['p'])) % key['p']
        cipher_pairs.append([a, b])

    encryptedStr = ""
    for pair in cipher_pairs:
        encryptedStr += str(pair[0]) + ' ' + str(pair[1]) + ' '
    return encryptedStr


def decrypt(key, cipher):
    plaintext = []
    cipherArray = cipher.split()
    if len(cipherArray) % 2 != 0:
        return
    for i in range(0, len(cipherArray), 2):
        a = int(cipherArray[i])
        b = int(cipherArray[i + 1])

        s = pow(a, key['x'], key['p'])
        plain = (b * pow(s, key['p'] - 2, key['p'])) % key['p']
        plaintext.append(plain)

    decryptedText = bytearray(plaintext).decode('utf-8')

    return decryptedText


if __name__ == "__main__":
    priv, pub = generate_keys()
    text = "qwerty12345678ytrewq"
    enc_text = encrypt(pub, text)
    dec_text = decrypt(priv, enc_text)
    print("enc text : ", enc_text)
    print("dec text: ", dec_text)