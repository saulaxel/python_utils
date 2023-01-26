"""
Diversas representaciones en cadena adicionales para la clase Fraction, algunas
de las cuales son aptas para Latex

Para la mayoría de los casos, Fraction es más que suficiente
"""
from fractions import Fraction
from functools import wraps
import math
import math_entera


def fraccion_entera(f: Fraction) -> bool:
    return f.denominator == 1


def eleccion_inteligente(funcion, alternativa=lambda ComplexFrac: ComplexFrac.numerator):
    @wraps(funcion)
    def funcion_decorada(ComplexFrac):
        if not fraccion_entera(ComplexFrac):
            return funcion(ComplexFrac)
        else:
            return f'{alternativa(ComplexFrac)}'

    return funcion_decorada


class ComplexFrac:

    def __init__(self, numerator=0, denominator=1):

        if isinstance(numerator, complex):
            self.real = Fraction(numerator.real)
            self.imag = Fraction(numerator.imag)
        elif isinstance(numerator, tuple):
            self.real = Fraction(numerator[0])
            self.imag = Fraction(numerator[1])
        elif isinstance(numerator, ComplexFrac):
            self.real = numerator.real
            self.imag = numerator.imag
        else:
            self.real = Fraction(numerator)
            self.imag = Fraction(0)


        self.dividir_in_place(denominator)


    @property
    def numerador(self):
        if self.imag == 0:
            return self.real.numerator

        if self.real.denominator == self.imag.denominator:
            return self.real.numerator + 1j * self.imag.numerator

        denominador_comun = (self.real + self.imag).denominator

        real = self.real.numerator * denominador_comun / self.real.denominator
        imag = self.imag.numerator * denominador_comun / self.imag.denominator

        return real + imag * 1j


    @property
    def denominator(self):
        if self.imag == 0:
            return self.real.denominator

        if self.real.denominator == self.imag.denominator:
            return self.real

        return (self.real + self.imag).denominator


    @property
    def numerador_real(self):
        return self.real.numerator


    @property
    def denominador_real(self):
        return self.real.denominator


    @property
    def numerador_imag(self):
        return self.imag.numerator


    @property
    def denominador_imag(self):
        return self.imag.denominator


    def multiplicar_in_place(self, other):
        """

        La división de dos números:
        self = sr + si*i
        other = or + oi*i

        (sr + si*i)(or + oi*i) = (sr*or - si*oi) + (sr*oi + si*or)*i

        Por lo tanto:
        self.real = self.real*other.real - self.imag*other.imag
        self.imag = self.real*other.imag + self.imag*other.real
        """
        complex_mul = False

        if isinstance(other, complex):
            o_real = Fraction(other.real)
            o_imag = Fraction(other.imag)
            complex_mul = True
        elif isinstance(other, tuple):
            o_real = Fraction(other[0])
            o_imag = Fraction(other[1])
            complex_mul = True
        elif isinstance(other, ComplexFrac):
            o_real = other.real
            o_imag = other.imag
            complex_mul = True


        if complex_mul:
            real = self.real*o_real - self.imag*o_imag
            imag = self.imag*o_real + self.real*o_imag

            self.real = real
            self.imag = imag

        else:
            self.real *= other
            self.imag *= other


    def dividir_in_place(self, other):
        """

        La división de dos números:
        self = sr + si*i
        other = or + oi*i

        sr + si*i
        ---------
        or + oi*i

        =

        (sr + si*i)(or - oi*i)
        ----------------------
           (or**2 + oi**2)

        =

        (sr*or + si*oi) + (si*or - sr*oi)*i
        -----------------------------------
                  (or**2 + oi**2)

        Por lo tanto:
        self.real = self.real*other.real + self.imag*other.imag / (mag**2)
        self.imag = self.imag*other.real - self.real*other.imag / (mag**2)
        """
        complex_div = False

        if isinstance(other, complex):
            o_real = Fraction(other.real)
            o_imag = Fraction(other.imag)
            complex_div = True
        elif isinstance(other, tuple):
            o_real = Fraction(other[0])
            o_imag = Fraction(other[1])
            complex_div = True
        elif isinstance(other, ComplexFrac):
            o_real = other.real
            o_imag = other.imag
            complex_div = True


        if complex_div:
            o_magnitud_cuad = (o_real ** 2) + (o_imag ** 2)

            real = (self.real*o_real + self.imag*o_imag) / o_magnitud_cuad
            imag = (self.imag*o_real - self.real*o_imag) / o_magnitud_cuad

            self.real = real
            self.imag = imag

        else:
            self.real /= other
            self.imag /= other


    def clonar(self):
        return ComplexFrac((self.real, self.imag))


    @staticmethod
    @eleccion_inteligente
    def fraccion_en_linea(ComplexFrac):
        return f'{ComplexFrac.numerator} / {ComplexFrac.denominator}'


    @staticmethod
    @eleccion_inteligente
    def fraccion_latex_mini(ComplexFrac):
        return f'{{}}^{{{ComplexFrac.numerator}}} / \! {{}}_{{{ComplexFrac.denominator}}}'


    @staticmethod
    @eleccion_inteligente
    def fraccion_latex(ComplexFrac):
        return f'\\ComplexFrac {{{ComplexFrac.numerator}}} {{{ComplexFrac.denominator}}}'


    def __eq__(self, other):
        return (self.real == other.real) and (self.imag == other.imag)


    def __add__(self, other):
        if isinstance(other, ComplexFrac) or isinstance(other, complex):
            return ComplexFrac((self.real + other.real, self.imag + other.imag))
        else:
            return ComplexFrac((self.real + other, self.imag))


    def __radd__(self, other):
        return self.__add__(other)


    def __sub__(self, other):
        return self.__add__(-other)


    def __rsub__(self, other):
        return self.__sub__(other)


    def __mul__(self, other):
        res = self.clonar()
        res.multiplicar_in_place(other)
        return res


    def __rmul__(self, other):
        return self.__mul__(other)


    def __abs__(self):

        # No hay parte imaginaria
        if (self.imag == 0):
            return abs(self.real)


        # Si hay parte imaginaria, se debe sacar el módulo del valor
        abs_cuadrada = (self.real**2) + (self.imag**2)

        try:
            num = math_entera.raiz(abs_cuadrada.numerator)
            den = math_entera.raiz(abs_cuadrada.denominator)

            return ComplexFrac((num, den))

        except ValueError: # No se puede calcular la raíz de forma exacta
            return math.sqrt(abs_cuadrada)


    def modulo(self, primero, segundo):
        if (isinstance(primero, ComplexFrac) and primero.imag != 0) \
                or (isinstance(segundo, ComplexFrac) and segundo.imag != 0):
            raise ValueError('La operación mod requiere operandos enteros')

        val1 = primero.real if isinstance(primero, ComplexFrac) else primero
        val2 = segundo.real if isinstance(segundo, ComplexFrac) else segundo

        return val1 % val2


    def __mod__(self, other):
        return modulo(self, other)


    def __rmod__(self, other):
        return modulo(other, self)


    def __pow__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        ret = ComplexFrac(1)
        if other >= 0:
            for i in range(other):
                ret *= self
        else:
            for i in range(-other):
                ret /= self

        return ret

    def __rpow__(self, other):
        return NotImplemented


    def __truediv__(self, other):
        ret = self.clonar()
        ret.dividir_in_place(other)
        return ret


    def __rtruediv__(self, other):
        if isinstance(other, ComplexFrac):
            num = other
        else:
            num = ComplexFrac(other)


        ret = other.clone()
        ret.dividir_in_place(self)
        return ret


    def __pos__(self):
        return self.clonar()


    def __neg__(self):
        return ComplexFrac((-self.real, -self.imag))


    def __float__(self):
        if self.imag != 0:
            raise ValueError('No se puede convertir un complejo a flotante')

        return float(self.real)


    def __complex__(self):
        return complex(float(self.real), float(self.imag))


    def __str__(self):
        return self.__repr__()


    def __repr__(self):
        real = ComplexFrac.fraccion_en_linea(self.real)

        if self.imag != 0:
            imag = ComplexFrac.fraccion_en_linea(abs(self.imag))

            if self.real != 0:
                first_part = f'{real} ' if self.real != 0 else ''
                sign = '+ ' if self.imag >= 0 else '- '
            else:
                first_part = ''
                sign = '' if self.imag >= 0 else '-'

            return f'{first_part}{sign}{imag} i'

        return real



if __name__ == '__main__':
    f1 = ComplexFrac(1, 2)
    assert str(f1) == '1 / 2'
    assert str(-f1) == '-1 / 2'
    assert float(f1) == 0.5 and complex(f1) == 0.5 + 0j
    assert ComplexFrac.fraccion_latex(f1.real) == r'\ComplexFrac {1} {2}'
    assert ComplexFrac.fraccion_latex_mini(f1.real) == r'{}^{1} / \! {}_{2}'

    f2 = ComplexFrac(2)
    assert str(f2) == '2'
    assert float(f2) == 2.0 and complex(f2) == 2.0 + 0j
    assert ComplexFrac.fraccion_latex(f2.real) == r'2'
    assert ComplexFrac.fraccion_latex_mini(f2.real) == r'2'

    assert f2 == 2
    assert 2 == f2

    assert f1 + f2 == ComplexFrac(5, 2)
    assert f1 - f2 == ComplexFrac(-3, 2)
    assert f1 + 1 == ComplexFrac(3, 2)
    assert f1 - 1 == ComplexFrac(-1, 2)

    assert f1 * f2 == ComplexFrac(1)
    assert f1 / f2 == ComplexFrac(1, 4)
    assert f1 * 3 == ComplexFrac(3, 2)
    assert f1 / 3 == ComplexFrac(1, 6)

    assert f1 ** 2 == ComplexFrac(1, 4) and f1 ** 3 == ComplexFrac(1, 8)
    assert f1 ** (-1) == 2 and f1 ** (-2) == 4

    assert f2 ** 2 == 4 and f2 ** 3 == 8
    assert f2 ** (-1) == ComplexFrac(1, 2) and f2 ** (-2) == ComplexFrac(1, 4)

    f3 = ComplexFrac((1, 2))
    assert f3 == 1 + 2j
    assert str(f3) == "1 + 2 i"
    assert complex(f3) == 1 + 2j

    f4 = ComplexFrac((1, -1), 2)
    assert f4 == .5 -.5j and f4 == ComplexFrac(1 -1j, 2)
    assert str(f4) == "1 / 2 - 1 / 2 i"

    assert f3 + f4 == ComplexFrac((3, 3), 2)
    assert f3 - f4 == ComplexFrac((1, 5), 2)
    assert f3 * f4 == ComplexFrac((3, 1), 2)
    assert f3 / f4 == ComplexFrac((-1, 3))

    f5 = ComplexFrac(1j)
    assert str(f5) == '1 i'
    f6 = ComplexFrac(-1j)
    assert str(f6) == '-1 i'


    f7 = ComplexFrac(1, 1)
    assert f7 == ComplexFrac(f7)
