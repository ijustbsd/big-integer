import math
import unittest
from random import randint

from bigint import BigInt
from long_math import (dec_to_bin, l_add, l_divmod, l_mul, l_pow, l_root,
                       l_sub, less_than)


class TestLongMath(unittest.TestCase):

    MIN = 10 ** 20
    MAX = 10 ** 30
    TESTS_COUNT = 10 ** 5

    def test_add(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            self.assertEqual(str(x + y), l_add(str(x), str(y)))

    def test_sub(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            x, y = sorted([x, y], reverse=True)
            self.assertEqual(str(x - y), l_sub(str(x), str(y)))

    def test_mul(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            self.assertEqual(str(x * y), l_mul(str(x), str(y)))

    def test_divmod(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            self.assertEqual(tuple(map(str, divmod(x, y))), l_divmod(str(x), str(y)))

    def test_pow(self):
        for _ in range(100):
            x = randint(0, 1000)
            y = randint(0, 1000)
            self.assertEqual(str(x ** y), l_pow(str(x), str(y)))

    def test_root(self):
        for _ in range(100):
            x = randint(0, 100)
            y = randint(1, 100)
            self.assertEqual(str(int(x ** (1 / y))), l_root(str(x), str(y)))

    def test_dec_to_bin(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            self.assertEqual(bin(x)[2:], dec_to_bin(x))

    def test_less_than(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            self.assertEqual(x < y, less_than(str(x), str(y)))


class TestBigInt(unittest.TestCase):

    MIN = -10 ** 30
    MAX = 10 ** 30
    TESTS_COUNT = 10 ** 5

    def test_add(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            big_x = BigInt(str(x))
            big_y = BigInt(str(y))
            self.assertEqual(x + y, big_x + big_y)

    def test_sub(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            big_x = BigInt(str(x))
            big_y = BigInt(str(y))
            self.assertEqual(x - y, big_x - big_y)

    def test_mul(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            big_x = BigInt(str(x))
            big_y = BigInt(str(y))
            self.assertEqual(x * y, big_x * big_y)

    def test_div(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            big_x = BigInt(str(x))
            big_y = BigInt(str(y))
            self.assertEqual(int(x / y), big_x / big_y)

    def test_mod(self):
        for _ in range(self.TESTS_COUNT):
            x = randint(self.MIN, self.MAX)
            y = randint(self.MIN, self.MAX)
            big_x = BigInt(str(x))
            big_y = BigInt(str(y))
            self.assertEqual(x % y, big_x % big_y)

    def test_pow(self):
        for _ in range(100):
            x = randint(-100, 100)
            y = randint(0, 100)
            big_x = BigInt(str(x))
            big_y = BigInt(str(y))
            self.assertEqual(x ** y, big_x ** big_y)

    def test_root(self):
        for _ in range(100):
            x = randint(0, 100)
            y = randint(1, 100)
            big_x = BigInt(str(x))
            big_y = BigInt(str(y))
            self.assertEqual(int(x ** (1 / y)), BigInt.root(big_x, big_y))

    def test_gcd(self):
        for _ in range(10000):
            x = randint(0, 10 ** 20)
            y = randint(0, 10 ** 20)
            big_x = BigInt(str(x))
            big_y = BigInt(str(y))
            d, big_u, big_v = BigInt.gcd(big_x, big_y)
            u = int(('-' if big_u.is_neg else '') + big_u.value)
            v = int(('-' if big_v.is_neg else '') + big_v.value)
            self.assertEqual(str(math.gcd(x, y)), d.value)
            self.assertEqual(str(u*x + v*y), d.value)

    def test_ring_add(self):
        values = [
            ('3', '4', '5', '2'),
            ('12345678', '87654321', '123', '15'),
            ('12345678', '0', '987', '282'),
            ('0', '12345678', '987', '282'),
            ('9999999999', '9999999999', '9999999999', '0')
        ]
        for args in values:
            args = list(map(BigInt, args))
            self.assertEqual(BigInt.ring_add(*args[:3]), args[3])

    def test_ring_sub(self):
        values = [
            ('3', '4', '5', '4'),
            ('12345678', '87654321', '123', '75'),
            ('12345678', '0', '987', '282'),
            ('0', '12345678', '987', '705'),
            ('9999999999', '9999999999', '9999999999', '0')
        ]
        for args in values:
            args = list(map(BigInt, args))
            self.assertEqual(BigInt.ring_sub(*args[:3]), args[3])

    def test_ring_mul(self):
        values = [
            ('3', '4', '5', '2'),
            ('12345678', '87654321', '123', '3'),
            ('12345678', '0', '987', '0'),
            ('0', '12345678', '987', '0'),
            ('9999999999', '9999999999', '9999999999', '0')
        ]
        for args in values:
            args = list(map(BigInt, args))
            self.assertEqual(BigInt.ring_mul(*args[:3]), args[3])

    def test_ring_inv(self):
        values = [
            ('873372847093', str(10 ** 12), '94559444997'),
            ('3', '6', None),
        ]
        for *args, x in values:
            args = list(map(BigInt, args))
            if isinstance(x, str):
                x = BigInt(x)
            self.assertEqual(BigInt.ring_inv(*args[:2]), x)

    def test_ring_pow(self):
        values = [
            ('3', '4', '5', '1'),
            ('18', '50', '873372847093', '194798095869'),
            ('12345678', '0', '987', '1'),
            ('0', '12345678', '987', '0'),
            ('999', '999', '999', '0')
        ]
        for args in values:
            args = list(map(BigInt, args))
            self.assertEqual(BigInt.ring_pow(*args[:3]), args[3])


if __name__ == '__main__':
    unittest.main()
