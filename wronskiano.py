import numpy as np
import sympy as sp

from determinante import determinante


def wronskiano(*funciones, var):
    N = len(funciones)
    matriz = np.zeros(N * N, dtype='object').reshape(N, N)

    for i, fun in enumerate(funciones):
        matriz[i, 0] = fun

        for j in range(1, len(funciones)):
            matriz[i, j] = sp.diff(fun, var, j)

    return determinante(matriz).simplify()


if __name__ == '__main__':
    x = sp.Symbol('x')
    y1 = x**2 + 5*x
    y2 = 3*(x**2) - x

    print(wronskiano(y1, y2, var=x))
