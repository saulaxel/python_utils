# -*- coding: utf-8 -*-

def es_par(n):
    return n % 2 == 0


def es_impar(n):
    return n % 2 != 0


def es_divisible(a, divisor):
    return a % divisor == 0


def maximo_comun_divisor(*items):
    try:
        from math import gcd
        return gcd(*items)
    except:
        mcd = items[0]

        for num in items[1:]:
            while num != 0:
                res = mcd % num
                mcd = num
                num = res


        return mcd


def minimo_comun_multiplo(*items):
    try:
        from math import lcm
        return lcm(*items)
    except:
        mcm = 1
        for i in items:
            mcm = lcm * i // maximo_comun_divisor(lcm, i)

        return mcm


if __name__ == '__main__':
    pares = (0, 2, -2, 20)

    for par in pares:
        assert es_par(par)


    impares = (-1, 1, 27)

    for par in pares:
        assert es_par(par)


    divisibles = ((4, 2), (-49, 7), (1, 1))
    for a, divisor in divisibles:
        assert es_divisible(a, divisor)


    no_divisibles = ((7, 2), (-5, 2), (5, 7))
    for a, divisor in no_divisibles:
        assert not es_divisible(a, divisor)

    # Máximo común divisor
    assert maximo_comun_divisor(2, 6) == 2
    assert maximo_comun_divisor(1, 7) == 1
    assert maximo_comun_divisor(7, 7) == 7
    assert maximo_comun_divisor(4, 8, 12) == 4

    # Mínimo común múltiplo
    assert minimo_comun_multiplo(6, 8) == 24
    assert minimo_comun_multiplo(5, 7) == 35
    assert minimo_comun_multiplo(3, 3) == 3
    assert minimo_comun_multiplo(3, 4, 5) == 60
