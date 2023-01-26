

def cortes_tam_fijo(sliceable, tam_corte):
    if not isinstance(tam_corte, int) or tam_corte == 0:
        raise ValueError('tam_corte needs to be integer greater than 0')

    for i in range(0, len(sliceable), tam_corte):
        yield sliceable[i:i + tam_corte]


def sin_duplicados(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


def producto(numeros):
    try:
        from math import prod
        return prod(numeros)
    except:
        from functools import reduce
        from operator import mul
        return reduce(mul, numeros, 1)


if __name__ == '__main__':
    t1 = [1, 5, 2, 1, 9, 1, 5, 10]
    assert list(sin_duplicados(t1)) == [1, 5, 2, 9, 10]

    t2 = [ {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4} ]
    t2_sd = list(sin_duplicados(t2, key=lambda d: (d['x'], d['y'])))
    t2_esperado = [ {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4} ]

    assert t2_sd == t2_esperado

    ####

    assert list(cortes_tam_fijo('abcdef', 3)) == ['abc', 'def']
    assert list(cortes_tam_fijo([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(cortes_tam_fijo((1,), 3)) == [(1,)]
    assert list(cortes_tam_fijo((), 2)) == []

    ####
    assert producto((1, 2, 3, 4)) == 24
    assert producto([]) == 1
    assert producto((-5, 2)) == -10
    assert producto((-5, -2)) == 10
