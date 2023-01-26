import math

from math import pi

from trig_grados import gsin, gcos

def complejo_a_polar(num):
    if type(num) == complex:
        magnitud = abs(num)
        angulo = math.atan2(num.imag, num.real) * 180 / pi
        return (magnitud, angulo)
    else:
        return (num, 0)


def polar_a_complejo(magnitud, angulo):
    return magnitud * (gcos(angulo) + 1j * gsin(angulo))


if __name__ == '__main__':
    def almost_equal(a, b, delta=0.001):
        return b - delta <= a <= b + delta

    num1 = 1 + 0j
    num2 = 1
    mag1, ang1 = complejo_a_polar(num1)
    mag2, ang2 = complejo_a_polar(num2)

    num1_ret = polar_a_complejo(mag1, ang1)
    num2_ret = polar_a_complejo(mag2, ang2)

    assert almost_equal(mag1, 1.0) and almost_equal(ang1, 0.0)
    assert almost_equal(mag2, 1.0) and almost_equal(ang2, 0.0)
    assert almost_equal(num1_ret.real, 1.0) and almost_equal(num1_ret.imag, 0.0)
    assert almost_equal(num2_ret.real, 1.0) and almost_equal(num2_ret.imag, 0.0)

    num3 = 0 + 1j
    mag3, ang3 = complejo_a_polar(num3)
    num3_ret = polar_a_complejo(mag3, ang3)
    assert almost_equal(mag3, 1.0) and almost_equal(ang3, 90.0)
    assert almost_equal(num3_ret.real, 0.0) and almost_equal(num3_ret.imag, 1.0)

    num4 = math.sqrt(2) * (1 + 1j)
    mag4, ang4 = complejo_a_polar(num4)
    num4_ret = polar_a_complejo(mag4, ang4)
    assert almost_equal(mag4, 2.0) and almost_equal(ang4, 45.0)
    assert almost_equal(num4_ret.real, math.sqrt(2)) and almost_equal(num4_ret.imag, math.sqrt(2))
