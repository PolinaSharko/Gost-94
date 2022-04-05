import random as ran
import hashlib
import sympy

W = 257
M = 1 << W
FF = M - 1
W1 = 254
M1 = 1 << W1
FF1 = M1 - 1
K = 512
M2 = 1 << K
FF2 = M2 - 1
K2 = 1024
M3 = 1 << K2
FF3 = M3 - 1

def make_p_q_a():
    t = 128
    ti = [t]
    s = 0
    c = ran.randint(1, pow(2, 16)-1)
    if c % 2 == 0:
        c = c - 1
    while t >= 17:
        t = t//2
        ti.append(t)
        s += 1

    x0 = ran.randint(1, pow(2, 16)-1)
    primes = []
    p_i = 0
    p = 0
    q = 0
    y0 = x0
    y = [y0]
    Y = []
    primes.append(sympy.nextprime(pow(2, ti[s]-1)))
    flag_m = True
    flag_p = True
    flag_k = True
    m = s-1
    while flag_m:
        while flag_p:
            if ti[m+1] % 16 != 0:
                r = (ti[m+1]//16) + 1
            else:
                r = ti[m+1]//16
            Y.append(y[0]*pow(2, 0))
            d = 0
            while d < r:
                y.append((y[d]*19381+c) % pow(2, 16))
                d += 1
                if d < r:
                    Y.append(y[len(y)-1])
            y[0] = y[d]
            if len(y) > 1:
                y = [y[0]]
            N = pow(2, ti[m]-1)//primes[p_i]+pow(2, ti[m]-1, Y[len(Y)-1])//(primes[p_i]*pow(2, 16*r))
            if N % 2 == 1:
                N += 1
            k = 0
            while flag_k:
                p_tmp = primes[p_i]*(N+k)+1
                if p_tmp > pow(2, ti[m]):
                    break
                else:
                    flag_p = False
                if pow(2, primes[p_i]*(N+k), p_tmp) == 1 and pow(2, N+k, p_tmp) != 1:
                    flag_k = False
                    m = m - 1
                else:
                    k = k + 2

        primes.append(p_tmp)
        p_i += 1
        flag_p = True
        flag_k = True
        if FF1 <= p_tmp <= FF2:
            q = p_tmp
        if FF2 <= p_tmp <= FF3:
            p = p_tmp
            break
    return p, q


class Signature(object):

    def __init__(self):
        self.p, self.q = make_p_q_a()
        # Формирование простых чисел
        self.p = 0xebc7dbb31a491de3a9a5f11c7eb4bf89c569b174136e04d6cb0aff8259e277a2fd21d9f2953bbd75db9421617476050a93a16d9fece2e6ddd0466260b9455751
        self.q = 0x87fe3310585c76579461ebfde23b32e27a9f201e7345ea83cf67557e8461fc9d
        print(hex(self.p))
        print(hex(self.q))
        a = ran.randint(1, self.p - 1)
        while pow(a, ((self.p - 1) // self.q), self.p) == 1:
            a = ran.randint(1, self.p - 1)
        self.a = pow(a, ((self.p - 1) // self.q), self.p)
        self.x = ran.randint(1, self.q)
        # Секретный ключ

        a1 = hashlib.sha1(b'signature')
        a2 = a1.hexdigest()
        m = int(a2, 16)
        # Хеш-функция сообщения

        print(hex(m))

        k = ran.randint(0, self.q)
        self.y = pow(self.a, self.x, self.p)
        # Открытый ключ

        r = (pow(self.a, k, self.p)) % self.q
        # Формирование ЭЦП
        while r % self.q == 0:
            k = ran.randint(0, self.q)
            r = (pow(self.a, k, self.p)) % self.q
        s = (k*m+self.x*r) % self.q
        print(hex(s))
        # ЭЦП для исходного сообщения

        w = pow(m, self.q-2, self.q)
        # Процедура проверки подписи
        u1 = (w*s) % self.q
        u2 = (self.q-r)*w % self.q
        v = ((pow(self.a, u1, self.p)*pow(self.y, u2, self.p)) % self.p) % self.q
        d = 0x8043837d829feed2c51d5298e492f3e1d971a31d817e68ab1b0859b4d506f704cb22044b5ec474699d0c790f56c3dd1a04937e6a3e4bfe7fd32cf52880a0edd161c7
        dd = 0x80af72df98b5edd3338958f5f09f9cebafa83abb77a915d3a7747bf8a2d308e547b
        print(sympy.isprime(self.p))
        print(sympy.isprime(self.q))
        print(hex(r))
        print(r == v)


Signature = Signature()
