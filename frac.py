"""
Diversas representaciones en cadena adicionales para la clase Fraction, algunas
de las cuales son aptas para Latex

Para la mayoría de los casos, Fraction es más que suficiente
"""
from fractions import Fraction
from functools import wraps


def eleccion_inteligente(funcion, alternativa=lambda frac: frac.numerator):
    def funcion_decorada(self):
        if not self.es_entero():
            return funcion(self)
        else:
            return f'{alternativa(self)}'

    return funcion_decorada


def castear_a_frac_operacion_unaria(fun):
    @wraps(fun)
    def fun2(self):
        res = fun(self)
        return Frac(res)

    return fun2


def castear_a_frac_operacion_binaria(fun):
    @wraps(fun)
    def fun2(self, other):
        res = fun(self, other)
        return Frac(res)

    return fun2


def castear_divmod(fun):
    @wraps(fun)
    def fun2(self, other):
        res = fun(self, other)
        return (res[0], Frac(res[1]))
    return fun2


class Frac(Fraction):

    def es_entero(self):
        return self.denominator == 1


    @eleccion_inteligente
    def fraccion_en_linea(self):
        return f'{self.numerator} / {self.denominator}'


    @eleccion_inteligente
    def fraccion_latex_mini(self):
        return f'{{}}^{{{self.numerator}}} / \! {{}}_{{{self.denominator}}}'


    @eleccion_inteligente
    def fraccion_latex(self):
        return f'\\frac {{{self.numerator}}} {{{self.denominator}}}'


    def __str__(self):
        return self.fraccion_en_linea()


    def __repr__(self):
        return self.fraccion_en_linea()



# Proxy para que las operaciones matemáticas regresen fracciones
def actualizar_operadores():
    # Al usar operadores de Frac(), por ejemplo, para sumar dos objetos
    # Frac(1, 2) + Frac(1, 3), el resultado es de tipo Fraction, que es la clase
    # padre. Se van a actualizar todos los operadores con un decorador que añada
    # una conversión a la clase derivada para que la suma, resta, etc., de dos
    # objetos tipo Frac resulte también en un objeto tipo Frac

    def recorrer_y_actualizar(lista_operaciones, decorador):
        for op in lista_operaciones:
            metodo = getattr(Frac, op)
            metodo_nuevo = decorador(metodo)
            setattr(Frac, op, metodo_nuevo)


    operaciones_unarias = [
        '__pos__',
        '__neg__',
    ]
    recorrer_y_actualizar(operaciones_unarias, castear_a_frac_operacion_unaria)

    operaciones_binarias = [
        '__add__',
        '__radd__',
        '__sub__',
        '__rsub__',
        '__mul__',
        '__rmul__',
        '__abs__',
        '__mod__',
        '__rmod__',
        '__pow__',
        '__rpow__',
        '__truediv__',
        '__rtruediv__',
    ]

    recorrer_y_actualizar(operaciones_binarias, castear_a_frac_operacion_binaria)

    operaciones_divmod = [
        '__divmod__',
        '__rdivmod__',
    ]

    recorrer_y_actualizar(operaciones_divmod, castear_divmod)


actualizar_operadores()


if __name__ == '__main__':
    f1 = Frac(1, 2)
    assert str(f1) == '1 / 2'
    assert repr(float(f1)) == '0.5'
    assert f1.fraccion_latex() == r'\frac {1} {2}'
    assert f1.fraccion_latex_mini() == r'{}^{1} / \! {}_{2}'
    print(f'{f1 = } \t {str(f1) = } \t {float(f1) = }')
    print(f'f1.fraccion_latex() = {f1.fraccion_latex()} \t\t f1.fraccion_latex_mini() = {f1.fraccion_latex_mini()}')

    print('\n')

    f2 = Frac(2)
    assert str(f2) == '2'
    assert f2.fraccion_latex() == r'2'
    assert f2.fraccion_latex_mini() == r'2'
    print(f'{f2 = }   \t {str(f2) = }  \t {float(f2) = }')
    print(f'f2.fraccion_latex() = {f2.fraccion_latex()} \t\t\t f2.fraccion_latex_mini() = {f2.fraccion_latex_mini()}')
