"""
Algunas funciones para calcular circuitos
"""
from __future__ import division
from frac import Frac
import sys
from matrices import inversa

giga = Frac('1e9')
mega = Frac('1e6')
kilo = Frac('1e3')
mili = Frac('1e-3')
micro = Frac('1e-6')
nano = Frac('1e-9')

def res_parallel(res1, res2, *more_resistances):
    """
    Calcula la resistencia equivalente de dos o más
    resistencias en paralelo

    1 / resistencia_equiv = 1 / res1 + 1 / res2 + ...
    """
    inverse_res = (1 / res1) + (1 / res2)

    for res in more_resistances:
        inverse_res += (1 / res)

    return 1 / inverse_res


def res_series(res1, res2, *more_resistances):
    """
    Calcula la resistencia equivalente de dos o más
    resistencias en serie

    resistencia_equiv = res1 + res2 + ...
    """
    equivalent_res = res1 + res2

    for res in more_resistances:
        equivalent_res += res

    return equivalent_res


def con_parallel(con1, con2, *more_con):
    return res_series(con1, con2, *more_con)


def con_series(con1, con2, *more_con):
    return res_parallel(con1, con2, *more_con)

def res_estrella_a_delta(resa, resb, resc):
    ya = 1 / resa
    yb = 1 / resb
    yc = 1 / resc
    print(f'{ya = }')
    print(f'{yb = }')
    print(f'{yc = }')

    y_suma = ya + yb + yc
    print(f'{y_suma = }')

    yab = ya * yb / y_suma
    ybc = yb * yc / y_suma
    yca = yc * ya / y_suma
    print(f'{yab = }')
    print(f'{ybc = }')
    print(f'{yca = }')


    zab = 1 / yab
    zbc = 1 / ybc
    zca = 1 / yca
    print(f'{zab = }')
    print(f'{zbc = }')
    print(f'{zca = }')

    return (1 / yab, 1 / ybc, 1 / yca)


def div_voltaje(v, res1, res2):
    """
    ___(res1)__(o)__(res2)___
  + |                       |
   (v)                      |
  - |                       |
    _________________________
    Se calcula el voltaje en el punto (o), dados los valores de v y de las
    resistencias
    """
    return v * res2 / (res1 + res2)


def div_corriente(i, res_buscada, otra_res):
    """
    ____________________________
    |            |             |
  + |            |             |
   (i)         (res1)        (res2)
  - |            |             |
    |        (o)||             |
    |           v|             |
    |            |             |
    _____________|_____________|
    Se calcula la corriente (o) a partir de (i) y los valores de las
    resistencias
    """
    return i * otra_res / (res_buscada + otra_res)


def potencia(i=None, v=None, r=None):
    """
    Calcula la potencia disipada por un elemento lineal e invariante en el
    tiempo
    """
    if i and v:
        return i * v
    if i and r:
        return r * i * i
    if v and r:
        return v * v / r

    raise Exception('Se requieren dos valores de los tres a elegir (corriente, voltaje, resistencia)')

if __name__ == '__main__':
    from frac import Frac

    multiplicadores = (
        giga,
        mega,
        kilo,
        1,
        mili,
        micro,
        nano
    )

    for mul1, mul2 in zip(multiplicadores, multiplicadores[1:]):
        assert mul1 == mul2 * 1000

    assert res_series(Frac(1)*mili, Frac(2)*mili) == Frac(3)*mili
    assert res_series(Frac(1)*kilo, Frac(2)*kilo, Frac(3)*kilo) == Frac(6)*kilo

    assert res_parallel(Frac(1)*giga, Frac(2)*giga) == Frac(2, 3)*giga
    assert res_parallel(Frac(1)*nano, Frac(2)*nano, Frac(3)*nano) == Frac(6, 11)*nano

    assert div_voltaje(v=8, res1=5*mega, res2=3*mega) == 3
    assert div_corriente(i=8, res_buscada=5*micro, otra_res=3*micro) == 3


def metodo_nodos(A, Yk, Vsk, Jsk, echo=False):

    if echo:
        print('Yk', Yk, sep='\n')
        print('Jsk', Jsk, sep='\n')
        print('Vsk', Vsk, sep='\n')
        print('A', A, sep='\n')


    Yn = A * Yk * A.T

    In_predividido_A = Yk*Vsk - Jsk

    In = A * In_predividido_A

    En = inversa(Yn) * In


    Vk = A.T * En


    Jk = Yk*Vk + Jsk - Yk*Vsk

    if echo:
        print('Yn', Yn, sep='\n')
        print('In_predividido_A', In_predividido_A, sep='\n')
        print('In', In, sep='\n')
        print('En', En, sep='\n')
        print('Vk', Vk, sep='\n')
        print('Jk', Jk, sep='\n')

    return Vk, Jk


def metodo_nodos_abreviado(A, Yn, In, echo=False):
    if echo:
        print('A', A, sep='\n')
        print('Yn', Yn, sep='\n')
        print('In', In, sep='\n')


    En = inversa(Yn) * In

    Vk = A.T * En

    if echo:
        print('En', En, sep='\n')
        print('Vk', Vk, sep='\n')
