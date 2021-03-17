from typing import Tuple


def dec_to_bin(s1: str) -> str:
    return bin(int(s1))[2:]


def less_than(s1: str, s2: str) -> bool:
    s1 = s1.lstrip('0') or '0'
    s2 = s2.lstrip('0') or '0'

    l1 = len(s1)
    l2 = len(s2)

    if l1 < l2:
        return True
    elif l2 < l1:
        return False

    for x, y in zip(s1, s2):
        if x < y:
            return True
        elif x > y:
            return False

    return False


def is_equal(s1: str, s2: str) -> bool:
    s1 = s1.lstrip('0') or '0'
    s2 = s2.lstrip('0') or '0'
    return s1 == s2


def is_even(s1: str) -> bool:
    return not int(s1[-1]) % 2


def l_add(s1: str, s2: str) -> str:
    l1 = len(s1)
    l2 = len(s2)
    m = max(l1, l2)
    k = int((m - 1) / 9 + 1)
    n = 9 * k
    s1 = s1.zfill(n)
    s2 = s2.zfill(n)
    w = 0
    base = 10 ** 9
    s3 = ''
    for i in range(1, k + 1):
        start = n - 9
        a = int(s1[start:n])
        b = int(s2[start:n])
        c = a + b + w
        if c < base:
            z = c
            w = 0
        else:
            z = c - base
            w = 1
        s = str(z)
        s = s.zfill(9)
        s3 = s + s3
        n -= 9
    if w == 1:
        s3 = '1' + s3
    s3 = s3.lstrip('0')
    return s3 or '0'


def l_sub(s1: str, s2: str) -> str:
    l1 = len(s1)
    l2 = len(s2)
    m = max(l1, l2)
    k = int((m - 1) / 9 + 1)
    n = 9 * k
    s1 = s1.zfill(n)
    s2 = s2.zfill(n)
    w = 0
    base = 10 ** 9
    s3 = ''
    for i in range(1, k + 1):
        start = n - 9
        a = int(s1[start:n])
        b = int(s2[start:n])
        c = a - b - w
        if c >= 0:
            z = c
            w = 0
        else:
            z = c + base
            w = 1
        s = str(z)
        s = s.zfill(9)
        s3 = s + s3
        n -= 9
    s3 = s3.lstrip('0')
    return s3 or '0'


def l_mul(s1: str, s2: str) -> str:
    l1 = len(s1)
    l2 = len(s2)
    m = max(l1, l2)
    k = int((m - 1) / 4 + 1)
    n = 4 * k
    s1 = s1.zfill(n)
    s2 = s2.zfill(n)
    base = 10 ** 4
    st = '0'
    n1 = n
    for j in range(1, k + 1):
        b = int(s2[n1-4:n1])
        n2 = n
        w = 0
        s3 = ''
        for i in range(1, k + 1):
            a = int(s1[n2-4:n2])
            c = a * b + w
            if c < base:
                z = c
                w = 0
            else:
                z = c % base
                w = int(c / base)
            s = str(z)
            s = s.zfill(4)
            s3 = s + s3
            n2 -= 4
        if w != 0:
            s3 = str(w) + s3
        s3 += '0' * (4 * (j - 1))
        st = l_add(st, s3)
        n1 -= 4
    st = st.lstrip('0') or '0'
    return st


def l_divmod(s1: str, s2: str) -> Tuple[str, str]:
    l1 = len(s1)
    l2 = len(s2)
    s3 = ''
    index = l2
    curr_div = s1[:index]
    if less_than(curr_div, s2):
        index += 1
        curr_div = s1[:index]
    old_div = curr_div
    while less_than(s2, curr_div) or is_equal(s2, curr_div):
        i = 0
        while less_than(s2, curr_div) or is_equal(s2, curr_div):
            curr_div = l_sub(curr_div, s2)
            i += 1
        s3 += str(i)
        old_div = curr_div
        if len(s2) == len(old_div):
            curr_div += s1[index: index + 1]
            index += 1
        else:
            curr_div += s1[index: index + l2 - len(old_div)]
            index += l2 - len(old_div)
        s3 += '0' * (len(curr_div) - len(old_div) - 1)
        if less_than(curr_div, s2) and index < l1:
            curr_div += s1[index:index + 1]
            index += 1
            s3 += '0'
    if len(old_div) < len(curr_div):
        s3 += '0'
    curr_div = curr_div.lstrip('0')
    return s3 or '0', curr_div or '0'


def l_pow(s1: str, s2: str):
    if s2 == '0':
        return '1'
    b = dec_to_bin(s2)
    z = s1
    for i in range(1, len(b)):
        z = l_mul(z, z)
        if b[i] == '1':
            z = l_mul(z, s1)
    return z


def l_root(s1: str, s2: str):
    if s1 == '0':
        return s1
    if s2 == '1':
        return s1
    s2_1 = l_sub(s2, '1')
    x = s1
    while True:
        z = x
        # x = ((s2_1 * x) + (s1 / (x ** s2_1))) / s2
        x = l_divmod(l_add(l_mul(s2_1, x), l_divmod(s1, l_pow(x, s2_1))[0]), s2)[0]
        if z == x or less_than(z, x):
            return z
