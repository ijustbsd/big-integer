from long_math import l_add, l_divmod, l_mul, l_pow, l_sub


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


if __name__ == '__main__':
    x = BigInt(input('Введите первое число (x): '))
    y = BigInt(input('Введите второе число (y): '))
    menu_text = '\n'.join([
        'Выберите действие:',
        '1) x + y',
        '2) x - y',
        '3) x * y',
        '4) x / y',
        '5) x mod y'
    ])
    print(menu_text)
    choice = input()
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
    else:
        print('Выбрано несуществующее значение :(')

    input('Для выхода нажмите Enter...')
