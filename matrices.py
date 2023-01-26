import numpy as np
from frac_mat import FracMat
from frac import Frac


def determinante(matriz):
    if isinstance(matriz, FracMat):
        return determinante(matriz.M)

    if isinstance(matriz, np.matrix):
        arr = matriz.A1.reshape(matriz.shape)
        ret = determinante(arr)
        return ret

    if matriz.shape == (1, 1):
        return matriz[0, 0]
    else:
        det = 0
        signo = 1
        for col in range(matriz.shape[1]):
            submatriz = np.delete(matriz, 0, axis=0)
            submatriz = np.delete(submatriz, col, axis=1)
            det += signo * matriz[0, col] * determinante(submatriz)
            signo = -signo

        return det


def cofactores(matriz):
    if isinstance(matriz, FracMat):
        return FracMat(*cofactores(matriz.M))

    if isinstance(matriz, np.matrix):
        arr = matriz.A1.reshape(matriz.shape)
        ret = cofactores(arr)
        return ret

    result = np.zeros(matriz.shape, dtype='object')
    lines, cols = matriz.shape
    for i in np.arange(lines):
        for j in np.arange(cols):
            aux = np.delete(matriz, i, axis=0)
            Mij = np.delete(aux, j, axis=1)


            sign = (1 if (i + j) % 2 == 0 else -1)
            result[i, j] = determinante(Mij) * sign

    return result



def inversa(matriz):
    det = determinante(matriz)

    cof = cofactores(matriz)

    return cof.T / det


if __name__ == '__main__':
    # Determinante
    matriz = np.matrix([[5]])
    assert determinante(matriz) == 5

    matriz2 = np.matrix([[2, 1], [1, 2]])
    assert determinante(matriz2) == 3

    matriz3 = np.matrix([
            [1, 2, 3],
            [2, 4, 6],
            [3, 6, 9]
        ])

    assert determinante(matriz3) == 0

    matriz5 = np.matrix([[ 5, 2, 1, 4, 6],
                         [ 9, 4, 2, 5, 2],
                         [11, 5, 7, 3, 9],
                         [ 5, 6, 6, 7, 2],
                         [ 7, 5, 9, 3, 3]])

    assert determinante(matriz5) == -2004

    # Inversa
    matriz4 = np.matrix([[2, 1],
                         [7, 4]])

    matriz_4_inversa = np.matrix([[ 4, -1],
                                  [-7,  2]])

    assert np.all(matriz_4_inversa == inversa(matriz4))

    matriz5 = np.matrix([[Frac(1), Frac(2), Frac(3)],
                         [Frac(4), Frac(5), Frac(6)],
                         [Frac(7), Frac(2), Frac(9)]])
    matriz5_inversa = np.matrix([
        [Frac(-11, 12), Frac(1, 3), Frac(1, 12)],
        [Frac(-1, 6), Frac(1, 3), Frac(-1, 6)],
        [Frac(3, 4), Frac(-1, 3), Frac(1, 12)]
    ])
    assert np.all(inversa(matriz5))
