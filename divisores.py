from math import sqrt, ceil

# Funciones para obtener divisores

def divisores(n):
    yield 1
    for divisor in divisores_no_triviales(n):
        yield divisor
    yield n


def divisores_no_triviales(n):
    limite = n // 2

    for i in range(2, limite + 1):
        if n % i == 0:
            yield i


# Aplicaciones de las funciones

def es_primo(n):
    return list(divisores_no_triviales(n)) == []


def es_par(n):
    try:
        # El abs(n) + 4 es un truco para evitar los casos especiales de -2, 0 y
        # 2. Por supuesto, esta no es una forma coherente de corroborar si un
        # número es par, pero se hace de tal forma no por su prácticidad sino
        # específicamente para aplicar las funciones definidas en este archivo

        if next(divisores_no_triviales(abs(n) + 4)) == 2:
            return True
        return False
    except StopIteration:
        return False


def es_impar(n):
    return not es_par(n)


def maximo_comun_divisor(a, b):
    div_a = set(divisores(a))
    div_b = set(divisores(b))

    divisores_comunes = div_a & div_b
    return max(divisores_comunes)


def minimo_comun_multiplo(a, b):
    mcd = maximo_comun_divisor(a, b)
    return a * b / mcd


if __name__ == '__main__':
    def main():
        # Obtención de divisores
        casos_prueba = (1, 5, 7, 6, 12)
        resultados_no_triviales = (
            [],
            [],
            [],
            [2, 3],
            [2, 3, 4, 6],
            [2, 3, 4, 5, 6, 10, 12, 15, 20, 30]
        )
        resultados_completos = [[1] + res_triv + [caso] for caso, res_triv
                                in zip(casos_prueba, resultados_no_triviales)]


        for num, res_no_triv, res_completa in zip(casos_prueba, resultados_no_triviales, resultados_completos):
            res = list(divisores_no_triviales(num))
            if res != res_no_triv:
                print('para divisores_no_triviales(', num, ') se esperaba', res_no_triv, 'y se obtuvo',
                        res)

            res2 = list(divisores(num))
            if res2 != res_completa:
                print('para divisores(', num, ') se esperaba', res_completa, 'y se obtuvo', res2)

        # Primo, par, impar
        assert all(es_primo(x) for x in (1, 2, 3, 5, 7))
        assert not any(es_primo(x) for x in (4, 6, 8, 9))

        assert all(es_par(x) for x in (-4, -2, 0, 2, 4))
        assert all(es_impar(x) for x in (-3, -1, 1, 3))


        # Máximo común divisor
        assert maximo_comun_divisor(2, 6) == 2
        assert maximo_comun_divisor(1, 7) == 1
        assert maximo_comun_divisor(7, 7) == 7

        # Mínimo común múltiplo
        assert minimo_comun_multiplo(6, 8) == 24
        assert minimo_comun_multiplo(5, 7) == 35
        assert minimo_comun_multiplo(3, 3) == 3

    main()
