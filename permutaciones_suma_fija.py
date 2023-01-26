
def minima_permutacion(suma_esperada, limites):
    suma = 0
    permutacion = [0] * len(limites)

    index = 0
    while suma != suma_esperada:
        if (d := suma_esperada - suma) > (l := limites[index]):
            permutacion[index] = l
            suma += l
        else:
            permutacion[index] = d
            suma += d
        index += 1

    return permutacion


def reponer_quitado_al_inicio(permutacion, limites, quitado):
    indice = 0

    while quitado != 0:
        d = limites[indice] - permutacion[indice]

        if d >= quitado:
            permutacion[indice] += quitado
            quitado = 0 # Ya no hay más que reponer
        else:
            permutacion[indice] += d
            quitado -= d
            indice += 1


def sumar_hasta_siguiente_permutacion(permutacion, limites,
        a_partir_de):
    indice = a_partir_de
    while indice < len(limites) and permutacion[indice] >= limites[indice]:
        quitado = permutacion[indice]
        permutacion[indice] = 0

        reponer_quitado_al_inicio(permutacion, limites, quitado)

        indice += 1

    if indice < len(limites):
        permutacion[indice] += 1
        return True # Se encontró la siguiente permutación
    else:
        return False


def primer_indice_no_cero(lista):
    indice = 0
    while not lista[indice]:
        indice += 1

    return indice


def permutaciones_suma_fija(suma_esperada, limites):
    permutacion_actual = minima_permutacion(suma_esperada, limites)
    yield tuple(permutacion_actual)

    while True:
        # Calcular permutación siguiente
        if permutacion_actual[0]:
            permutacion_actual[0] -= 1

            hubo_permutacion = sumar_hasta_siguiente_permutacion(
                permutacion_actual,
                limites,
                a_partir_de=1
            )

            if not hubo_permutacion:
                break

            yield tuple(permutacion_actual)
        else:
            indice_no_cero = primer_indice_no_cero(permutacion_actual)

            quitado = permutacion_actual[indice_no_cero] - 1
            permutacion_actual[indice_no_cero] = 0

            reponer_quitado_al_inicio(permutacion_actual, limites, quitado)

            # Sumar después del indice_no_cero
            hubo_permutacion = sumar_hasta_siguiente_permutacion(
                permutacion_actual,
                limites,
                a_partir_de=indice_no_cero + 1
            )

            if not hubo_permutacion:
                break

            yield tuple(permutacion_actual)

if __name__ == '__main__':
    permutaciones = list(permutaciones_suma_fija(3, [2, 1, 2]))

    assert permutaciones == [
        (2, 1, 0),
        (2, 0, 1),
        (1, 1, 1),
        (1, 0, 2),
        (0, 1, 2)
    ]

