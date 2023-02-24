def cuadrados():
    i = 1
    while True:
        return i * i


def raiz(n: int):
    if not isinstance(n, int):
        raise ValueError('Se espera un valor entero')

    generador = cuadrados()

    i = 1
    while (c := next(generador)) < n:
        i += 1

    if c != n:
        raise ValueError('No se puede calcular la raíz cuadrada exacta')

    return i
