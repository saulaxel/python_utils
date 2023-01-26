# Ya existe numpy.poly1d
# https://www.codespeedy.com/find-roots-of-polynomial-in-python/

import numpy as np


class Polinomio:
    def __init__(self, coeficientes):

        coeficientes = np.array(list(reversed(coeficientes)))
        coeficientes = self.__quitar_ceros_irrelevantes(coeficientes)

        self.__coeficientes = coeficientes


    def evaluar(self, x):
        valor_posicion = 1.0
        res = 0.0

        for coeficiente in self.__coeficientes:
            res += valor_posicion * coeficiente
            valor_posicion *= x

        return res


    @property
    def grado(self):
        return len(self.__coeficientes) - 1


    @property
    def coeficientes(self):
        return self.__coeficientes[::-1]


    def parejas_grado_coeficiente(self):
        return reversed(list(enumerate(self.__coeficientes)))


    def __quitar_ceros_irrelevantes(self, coefs):
        index = len(coefs) - 1
        while index > 0 and coefs[index] == 0:
            index -= 1

        return coefs[0:index + 1]


    def __add__(self, otro):

        if not isinstance(otro, Polinomio):
            nuevos_coef = self.__coeficientes.copy()
            nuevos_coef[0] += otro
        else:
            if self.grado >= otro.grado:
                largo = self
                corto = otro
            else:
                largo = otro
                corto = self

            nuevos_coef = largo.__coeficientes.copy()
            nuevos_coef[0:len(corto.__coeficientes)] += corto.__coeficientes

        nuevos_coef = self.__quitar_ceros_irrelevantes(nuevos_coef)

        nuevo = Polinomio([])
        nuevo.__coeficientes = nuevos_coef
        return nuevo


    def __mul__(self, otro):
        if not isinstance(otro, Polinomio):
            otro = Polinomio([otro])

        nuevos_coef = np.convolve(self.__coeficientes, otro.__coeficientes)
        nuevo = Polinomio([])
        nuevo.__coeficientes = nuevos_coef
        return nuevo


    def __divmod__(self, otro):
        coef_self = self.__coeficientes.copy()
        coef_otro = otro.__coeficientes.copy()

        dif_grado = self.grado - otro.grado
        cociente = np.zeros(dif_grado + 1, dtype=coef_self.dtype)
        aux_multiplicacion = cociente.copy()

        pos_self = self.grado
        pos_otro = otro.grado
        pos_resul = dif_grado

        for i in range(dif_grado + 1):
            cociente_individual = coef_self[pos_self] / coef_otro[otro.grado]
            cociente[pos_resul] = cociente_individual
            aux_multiplicacion[pos_resul] = cociente_individual

            coef_self -= np.convolve(coef_otro, aux_multiplicacion)
            assert coef_self[pos_self] == 0

            aux_multiplicacion[pos_resul] = 0

            pos_self -= 1
            pos_otro -= 1
            pos_resul -= 1

        # En coef_self solo debe quedar el residuo, además de varios ceros al
        # inicio
        residuo = self.__quitar_ceros_irrelevantes(coef_self)

        p_cociente = Polinomio([])
        p_residuo = Polinomio([])
        p_cociente.__coeficientes = cociente
        p_residuo.__coeficientes = residuo
        return (p_cociente, p_residuo)


    def __pow__(self, exponente):
        assert type(exponente) == int and exponente >= 1
        mul = self
        for i in range(exponente - 1):
            mul *= self
        return mul


    def __rmul__(self, otro):
        return self.__mul__(self, otro)


    def __radd__(self, otro):
        return self.__add__(otro)


    def __eq__(self, otro):
        if self.__class__ is otro.__class__:
            if self.grado != otro.grado:
                return False
            return np.array_equal(self.__coeficientes, otro.__coeficientes)
        else:
            return NotImplemented


    def __neg__(self):
        nuevos_coef = -self.__coeficientes
        nuevo = Polinomio([])
        nuevo.__coeficientes = nuevos_coef
        return nuevo


    def __sub__(self, other):
        return self.__add__(-other)


    def __rsub__(self, other):
        return self.__add__(-other)


    def __hash__(self, otro):
        return hash((self.__class__, self.__coeficientes))


    def as_string(self, variable):
        string = ""
        primero = True
        for grado, coeficiente in self.parejas_grado_coeficiente():
            if coeficiente == 0:
                continue

            signo = ''
            if coeficiente >= 0 and not primero:
                signo = ' + '
            if coeficiente < 0:
                signo = ' - '

            coeficiente_positivo = abs(coeficiente)

            parte_media = ''
            if coeficiente_positivo != 1 or grado == 0:
                parte_media += f'{coeficiente_positivo} '

            if grado == 0:
                string += f'{signo}{parte_media}'
            elif grado == 1:
                string += f'{signo}{parte_media}{variable}'
            else:
                string += f'{signo}{parte_media}{variable}^{grado}'

            primero = False

        return string.strip() if string else '0'


    def __str__(self):
        return self.as_string(variable='x')


    def __repr__(self):
        return f'Polinomio({self.coeficientes})'


if __name__ == '__main__':
    def prueba():
        p1 = Polinomio([1, 2, 1]) # x² + 2x + 1
        p2 = Polinomio([1, 2, 3, 4, 5]) # x⁴ + 2x³ + 3x² + 4x + 5

        assert p1.evaluar(2) == 9
        assert p1.evaluar(-2) == 1

        suma1 = p1 + p2
        suma2 = p2 + p1
        resta1 = p1 - p2
        resta2 = p2 - p1
        cero = p1 - p1

        assert suma1 == Polinomio([1, 2, 4, 6, 6]) # x^4 + 2x³ + 4x² + 6x + 6
        assert suma2 == Polinomio([1, 2, 4, 6, 6])
        assert resta1 == Polinomio([-1, -2, -2, -2, -4])
        assert resta2 == Polinomio([1, 2, 2, 2, 4])
        assert cero == Polinomio([0])
        assert cero.grado == 0
        assert -p1 == Polinomio([-1, -2, -1])

        assert str(p1) == 'x^2 + 2 x + 1'
        p3 = Polinomio([-3, -2, -1])
        assert str(p3) == '- 3 x^2 - 2 x - 1'
        p4 = Polinomio([2, 0, 0, 1])
        assert str(p4) == '2 x^3 + 1'

        p5 = Polinomio([-1, -1])
        assert str(p5) == '- x - 1'

        p6 = Polinomio([0, 0, 0])
        assert str(p6) == '0'
        assert p6.grado == 0

        p7 = Polinomio([1, 1])
        p7_cuad = p7 ** 2
        p7_cubo = p7 ** 3
        num = p7_cubo
        den = p7

        assert num == Polinomio([1, 3, 3, 1])

        cociente1, residuo1 = divmod(p7_cubo, p7)
        assert cociente1 == p7_cuad and residuo1 == cero
        cociente2, residuo2 = divmod(cociente1, p7)
        assert cociente2 == p7 and residuo2 == cero

        num2 = Polinomio([0.5, 1.])
        den2 = Polinomio([1., 2.])

        cociente3, residuo3 = divmod(num2, den2)
        assert cociente3 == Polinomio([0.5]) and residuo3 == cero

        cociente4, residuo4 = divmod(den2, num2)
        assert cociente4 == Polinomio([2.]) and residuo4 == cero

        p8 = Polinomio([1., -1.])
        p8_cuad = p8 ** 2
        p8_cubo = p8 ** 3
        p9 = Polinomio([7.0, 4.0])

        num3 = p8_cubo + p9
        den3 = p8_cuad

        cociente5, residuo5 = divmod(num3, den3)
        assert cociente5 == p8 and residuo5 == p9


    prueba()
