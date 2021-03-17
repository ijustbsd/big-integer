from long_math import (dec_to_bin, is_even, l_add, l_divmod, l_mul, l_pow,
                       l_root, l_sub)


class BigInt:

    def __init__(self, value='0'):
        if not isinstance(value, str):
            t = type(value).__name__
            raise TypeError(f'BigInt() argument must be a string, not "{t}"')

        if value == '-0':
            value = '0'

        self.is_neg = value[0] == '-'
        self.value = value[self.is_neg:]

        if not self.value.isdigit():
            raise TypeError(f'invalid argument for BigInt(): "{value}"')

    def __abs__(self):
        return BigInt(self.value)

    def __bool__(self):
        return self.value != '0'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ('-' if self.is_neg else '') + self.value

    def __len__(self):
        return len(self.value)

    def __eq__(self, other):
        if isinstance(other, int):
            other = BigInt(str(other))
        return self.value == other.value and self.is_neg == other.is_neg

    def __ne__(self, other):
        if isinstance(other, int):
            other = BigInt(str(other))
        return not self == other

    def __lt__(self, other):
        if self.is_neg == other.is_neg:
            self_len = len(self)
            other_len = len(other)
            if self_len == other_len:
                return (self.value < other.value) ^ self.is_neg
            return (self_len < other_len) ^ self.is_neg
        return self.is_neg

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __pos__(self):
        return BigInt(('-' if self.is_neg else '') + self.value)

    def __neg__(self):
        return BigInt(('' if self.is_neg else '-') + self.value)

    def __add__(self, other):
        if self.is_neg == other.is_neg:
            result = l_add(self.value, other.value)
            return BigInt(('-' if self.is_neg else '') + result)
        x, y = sorted((abs(self), abs(other)))
        neg = max((self, other), key=lambda e: abs(e)).is_neg
        return BigInt(('-' if neg else '') + (y - x).value)

    def __sub__(self, other):
        if not self.is_neg and not other.is_neg:
            y, x = sorted((self, other))
            result = l_sub(x.value, y.value)
            return BigInt(('-' if self < other else '') + result)

        if self.is_neg and not other.is_neg:
            return BigInt('-' + (abs(self) + abs(other)).value)

        if not self.is_neg and other.is_neg:
            return BigInt((abs(self) + abs(other)).value)

        if self.is_neg and other.is_neg:
            return self + abs(other)

    def __mul__(self, other):
        result = l_mul(self.value, other.value)
        return BigInt(('-' if self.is_neg != other.is_neg else '') + result)

    def __truediv__(self, other):
        if other.value == '0':
            raise ZeroDivisionError('division by zero')
        result = l_divmod(self.value, other.value)[0]
        return BigInt(('' if self.is_neg == other.is_neg else '-') + result)

    def __mod__(self, other):
        if other.value == '0':
            raise ZeroDivisionError('division by zero')
        mod = l_divmod(self.value, other.value)[1]
        mod = BigInt(mod)

        if mod.value == '0':
            return mod

        return {
            not self.is_neg and not other.is_neg: mod,
            self.is_neg and not other.is_neg: other - mod,
            not self.is_neg and other.is_neg: mod + other,
            self.is_neg and other.is_neg: -mod
        }[True]

    def __pow__(self, other):
        result = l_pow(self.value, other.value)
        if int(other.value[-1]) % 2:
            return BigInt(('-' if self.is_neg else '') + result)
        return BigInt(result)

    @staticmethod
    def root(a, b):
        result = l_root(a.value, b.value)
        return BigInt(result)

    @staticmethod
    def gcd(a, b):
        if a.value == '0':
            return b
        if b.value == '0':
            return a
        a = BigInt(a.value)
        b = BigInt(b.value)
        zero, one = BigInt('0'), BigInt('1')
        r, old_r = a, b
        s, old_s = zero, one
        t, old_t = one, zero
        while r:
            q = old_r / r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
            old_t, t = t, old_t - q * t
        return old_r, old_t, old_s

    @staticmethod
    def bin_gcd(a, b):
        a = BigInt(a.value)
        b = BigInt(b.value)
        zero, one, two = BigInt('0'), BigInt('1'), BigInt('2')
        g = one
        while is_even(a.value) and is_even(b.value):
            a /= two
            b /= two
            g *= two
        x, y = a, b
        A, B, C, D = one, zero, zero, one
        while x:
            while is_even(x.value):
                x /= two
                if is_even(A.value) and is_even(B.value):
                    A /= two
                    B /= two
                else:
                    A = (A + b) / two
                    B = (B - a) / two
            while is_even(y.value):
                y /= two
                if is_even(C.value) and is_even(D.value):
                    C /= two
                    D /= two
                else:
                    C = (C + b) / two
                    D = (D - a) / two
            if x < y:
                y -= x
                C -= A
                D -= B
            else:
                x -= y
                A -= C
                B -= D
        return g * y, C, D

    @staticmethod
    def ring_add(x, y, n):
        r1 = x % n
        r2 = y % n
        z = r1 + r2
        if z >= n:
            z -= n
        return z

    @staticmethod
    def ring_sub(x, y, n):
        r1 = x % n
        r2 = y % n
        z = r1 - r2
        if z < BigInt('0'):
            z += n
        return z

    @staticmethod
    def ring_mul(x, y, n):
        r1 = x % n
        r2 = y % n
        z = r1 * r2
        return z % n

    @staticmethod
    def ring_inv(x, n):
        if x.value == '1':
            return x
        d, v, u = BigInt.gcd(x, n)
        if d != BigInt('1'):
            return None
        zero = BigInt('0')
        while True:
            if u > n:
                u -= n
            if u < zero:
                u += n
            if zero < u < n:
                break
        return u

    @staticmethod
    def ring_pow(x, m, n):
        if m.value == '0':
            return BigInt('1')
        b = dec_to_bin(m.value)
        z = x % n
        for i in range(1, len(b)):
            z = (z * z) % n
            if b[i] == '1':
                z = (z * x) % n
        return z


if __name__ == '__main__':
    menu_text = '\n'.join([
        'Выберите операцию:',
        '1) x + y',
        '2) x - y',
        '3) x * y',
        '4) x / y',
        '5) x mod y',
        '6) x ^ y',
        '7) Корень из X степени Y',
        '8) НОД(x, y)',
        '9) (x + y) mod N',
        '10) (x - y) mod N',
        '11) (x * y) mod N',
        '12) x^(-1) mod N',
        '13) x^y mod N',
    ])
    print(menu_text)
    choice = input('Введите номер операции: ')

    if int(choice) < 1 or int(choice) > 13:
        print('Выбрано несуществующее значение :(')
        input('Для выхода нажмите Enter...')
        exit(0)

    x = BigInt(input('Введите первое число (x): '))
    if choice != '12':
        y = BigInt(input('Введите второе число (y): '))
    if 9 <= int(choice) <= 13:
        n = BigInt(input('Введите модуль (N): '))

    if choice == '1':
        print('x + y =', x + y)
    elif choice == '2':
        print('x - y =', x - y)
    elif choice == '3':
        print('x * y =', x * y)
    elif choice == '4':
        print('x / y =', x / y)
    elif choice == '5':
        print('x mod y =', x % y)
    elif choice == '6':
        print('x ^ y =', x ** y)
    elif choice == '7':
        print('Корень из X степени Y = ', BigInt.root(x, y))
    elif choice == '8':
        print('НОД(x, y), u, v =', *BigInt.gcd(x, y))
    elif choice == '9':
        print('(x + y) mod N =', BigInt.ring_add(x, y, n))
    elif choice == '10':
        print('(x - y) mod N =', BigInt.ring_sub(x, y, n))
    elif choice == '11':
        print('(x * y) mod N =', BigInt.ring_mul(x, y, n))
    elif choice == '12':
        inv = BigInt.ring_inv(x, n)
        if inv is None:
            print(f'Обратный элемент числа {x} по модулю {n} не существует!')
        else:
            print('x^(-1) mod N =', BigInt.ring_inv(x, n))
    elif choice == '13':
        print('x^y mod N =', BigInt.ring_pow(x, y, n))

    input('Для выхода нажмите Enter...')
