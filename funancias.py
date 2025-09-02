from decimal import Decimal, ROUND_HALF_DOWN
uno = Decimal("1")
dias_anio = Decimal("365")

def porcentaje_rendimiento_anual_lineal(monto_inicial, monto_final, dias):
    """ Se supone que la ganancia no se vuelve a re-invertir"""
    porcentaje_un_ciclo = (monto_final - monto_inicial) / monto_inicial
    porcentaje_anio = porcentaje_un_ciclo * (dias_anio / dias)

    return porcentaje_anio

def porcentaje_rendimiento_anual_compuesto(monto_inicial, monto_final, dias):
    """ Suponiendo que la ganancia también se invierte n veces """
    porcentaje_un_ciclo = (monto_final - monto_inicial) / monto_inicial
    porcentaje_anio = (uno + porcentaje_un_ciclo) ** int(dias_anio / dias)
    return porcentaje_anio - uno


def main():
    r1 = porcentaje_rendimiento_anual_lineal(Decimal("100"),
                                             Decimal("110"),
                                             Decimal("365"))
    assert r1 == Decimal("0.1")


    r2 = porcentaje_rendimiento_anual_compuesto(Decimal("100"),
                                                Decimal("110"),
                                                Decimal("180"))

    assert r2 == Decimal("0.21")

    r3 = porcentaje_rendimiento_anual_lineal(Decimal("100"),
                                             Decimal("110"),
                                             Decimal("182"))

    assert r3 > Decimal("0.2") and r3 < Decimal("0.21")


if __name__ == '__main__':
    main()
