import numpy as np
import random as rd
import secrets as sc

# 宏定义素数二进制位数
BIT_LENGTH = 128

# 宏定义ascii偏移量
OFFSET = 31


def fast_mul(a, b, n):
    """
    快速乘法
    :param a: 乘数a
    :param b: 乘数b
    :param n: 模数
    :return: a * b % n
    """
    res = 0
    while b:
        if b & 1:
            res = (res + a) % n
        a = (a + a) % n
        b >>= 1
    return res


def fast_pow(a, b, n):
    """
    快速幂
    :param a: 底数
    :param b: 指数
    :param n: 模数
    :return: a ** b % n
    """
    res = 1
    while b:
        if b & 1:
            res = fast_mul(res, a, n)
        a = fast_mul(a, a, n)
        b >>= 1
    return res


def miller_rabin(n):
    """
    Miller Rabin算法
    :param n: 待判断的数
    :return: True or False
    """
    if n % 2 == 0:
        return False

    k = 0
    q = n - 1
    while q % 2 == 0:
        k += 1
        q = (n - 1) // 2 ** k

    a = rd.randint(2, n - 2)
    if fast_pow(a, q, n) == 1 or fast_pow(a, q, n) == n - 1:
        return True

    for j in range(1, k):
        if fast_pow(a, 2 ** j * q, n) == n - 1:
            return True

    return False


def getRandomPrime():
    """
    获取随机素数
    :return: 随机素数
    """
    while True:
        p = sc.randbits(BIT_LENGTH)
        if p % 2 == 0:
            p -= 1
        while p.bit_length() == BIT_LENGTH and not miller_rabin(p):
            p += 2
        if miller_rabin(p):
            return p


def gcd(a, b):
    """
    求最大公约数
    :param a: 数a
    :param b: 数b
    :return: 最大公约数
    """
    if a < b:
        a, b = b, a
    while b != 0:
        a, b = b, a % b
    return a


def getCoprime(n):
    """
    获取与n互质的数
    :param n: 数n
    :return: 与n互质的数
    """
    while True:
        e = sc.randbits(BIT_LENGTH)
        if gcd(e, n) == 1:
            return e


def extended_euclidean(a, b):
    """
    扩展欧几里得算法
    :param a: 数a
    :param b: 数b
    :return: b在mod a下的逆元
    """
    x1, x2, x3 = 1, 0, a
    y1, y2, y3 = 0, 1, b

    while True:
        if y3 == 0:
            return 'None'
        elif y3 == 1:
            return y2 % a
        else:
            Q = x3 // y3
            t1, t2, t3 = x1 - Q * y1, x2 - Q * y2, x3 - Q * y3
            x1, x2, x3 = y1, y2, y3
            y1, y2, y3 = t1, t2, t3


def encryption(key, intPlaintext):
    """
    加密
    :param key: 公钥
    :param intPlaintext: int明文
    :return: 密文
    """
    ciphertext = []
    n, e = key
    for i in intPlaintext:
        ciphertext.append(fast_pow(i, e, n))
    return ciphertext


def decryption(key, ciphertext):
    """
    解密
    :param key: 私钥
    :param ciphertext: 密文
    :return: plaintext明文
    """
    plaintext = []
    n, d = key
    for i in ciphertext:
        plaintext.append(fast_pow(i, d, n))
    return plaintext


def readfile(filename):
    """
    读取文件
    :param filename:
    :return: 文件内容
    """
    file = open(filename, 'r')
    message = file.read()
    file.close()
    return message


def ascii2intPlaintext(ascii):
    """
    将ascii码数组2位一组转换为int数组
    :param ascii: ascii码数组
    :return: int明文数组
    """
    res = []
    for i in range(0, len(ascii) - 1, 2):
        res.append((ascii[i] - OFFSET) * 100 + (ascii[i + 1] - OFFSET))
    if len(ascii) % 2 == 1:
        res.append((ascii[-1] - OFFSET) * 100)
    else:
        res.append((ascii[-1] - OFFSET) * 100 + (ascii[-2] - OFFSET))
    return res


def intPlaintext2ascii(intPlaintext):
    """
    将int明文数组转换为ascii码数组
    :param intPlaintext: int明文数组
    :return: ascii码数组
    """
    res = []
    for i in intPlaintext[:-1]:
        res.append(i // 100 + OFFSET)
        res.append(i % 100 + OFFSET)
    if intPlaintext[-1] % 100 == 0:
        res.append(intPlaintext[-1] // 100 + OFFSET)
    return res


def string2ascii(string):
    """
    将字符串转换为ascii码数组
    :param string: 字符串
    :return: ascii码数组
    """
    ascii = np.frombuffer(string.encode('utf-8'), dtype=np.uint8)
    return ascii


def ascii2string(ascii):
    """
    将ascii码数组转换为字符串
    :param ascii:
    :return:
    """
    string = []
    for i in ascii:
        string.append(chr(i))
    return ''.join(string)


if __name__ == '__main__':
    """
    变量说明：
    p, q: 随机素数
    n: p * q
    euler: 欧拉函数
    e: 与euler互质的数
    d: e在mod euler下的逆元
    publicKey: 公钥
    privateKey: 私钥
    message: 明文
    intPlaintext: int明文
    ciphertext: 密文
    plaintext: 解密后的明文
    """
    print('声明宏定义：')
    print('素数的二进制长度:', BIT_LENGTH)
    print('ascii码偏移量:', OFFSET)

    print('**********************生成随机素数p, q**********************')
    p = getRandomPrime()
    print('p =', p)
    q = getRandomPrime()
    print('q =', q)

    print('**********************求p, q的乘积n**********************')
    n = p * q
    print('n =', n)

    print('**********************求n的欧拉函数值euler**********************')
    euler = (p - 1) * (q - 1)
    print('euler =', euler)

    print('**********************求与euler互质的数e**********************')
    e = getCoprime(euler)
    print('e =', e)

    print('**********************求e在mod euler下的逆元d**********************')
    d = extended_euclidean(euler, e)
    print('d =', d)

    print('**********************求公钥和私钥**********************')
    publicKey = (n, e)
    print('公钥publicKey:', publicKey)
    privateKey = (n, d)
    print('私钥privateKey:', privateKey)

    print('**********************读取明文**********************')
    message = readfile('lab2-Plaintext.txt')
    print('读取到的明文:', message)

    print('**********************将明文转换为ascii码数组**********************')
    message = string2ascii(message)
    print('明文转化出的ascii码数组:', message)

    print('**********************将ascii码数组转换为int明文数组**********************')
    intPlaintext = ascii2intPlaintext(message)
    print('ascii码二合一后的int明文数组:', intPlaintext)

    print('**********************使用公钥进行加密**********************')
    ciphertext = encryption(publicKey, intPlaintext)
    print('加密后的密文:', ciphertext)

    print('**********************将密文写入文件**********************')
    file = open('ciphertext.txt', 'w')
    file.write(str(ciphertext))
    file.close()
    print('密文已写入文件!')

    print('**********************使用私钥进行解密**********************')
    plaintext = decryption(privateKey, ciphertext)
    print('解密得到的int明文数组:', plaintext)

    print('**********************将int明文数组转换为ascii码数组**********************')
    message = intPlaintext2ascii(plaintext)
    print('int明文数组转化为的ascii码数组:', message)

    print('**********************将ascii码数组转换为字符串**********************')
    message = ascii2string(message)
    print('ascii码数组转化得到的明文:', message)

    print('**********************将明文写入文件**********************')
    file = open('plaintext.txt', 'w')
    file.write(message)
    file.close()
    print('明文已写入文件!')
