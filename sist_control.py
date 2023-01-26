import numpy as np

def escalon(t, t0):
    return (t - t0 >= 0)


def indice_del_cero(t, tolerancia):
    for i, val in enumerate(t):
        if abs(val) <= tolerancia:
            return i

    raise LookupError('Cero no encontrado en t')


def integrar(f, t, tolerancia=1e-3):
    """
    Calcula la integral de 0 a t, asumiendo que cada valor de f está separado
    por el mismo intervalo de tiempo delta
    """
    delta = t[1] - t[0]  # Se requieren al menos dos punto

    t0 = indice_del_cero(t, tolerancia=tolerancia)

    integral = np.zeros(f.shape, dtype=f.dtype)

    valores = list(enumerate(f))

    if t0 + 1 < len(t):
        valores_positivos = valores[t0 + 1:]

        for x, f_x in valores_positivos:
            integral[x] = integral[x - 1] + f_x

    if t0 > 0:
        valores_negativos = reversed(valores[0:t0])

        for x, f_x in valores_negativos:
            integral[x] = integral[x + 1] - f_x


    integral *= delta
    return integral


def derivar(f, t):
    delta = t[1] - t[0]

    derivada = np.zeros(f.shape, dtype=f.dtype)

    for i in range(len(f) - 1):
        derivada[i] = f[i + 1] - f[i]

    derivada[-1] = derivada[-2] # Rellenamos porque no tenemos información

    derivada /= delta

    return derivada


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(-4, 4, 81) # Se añade 1 para que x contenga cero
    y = x * x
    integral_y = integrar(y, x)

    plt.figure()

    plt.subplot(121)
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')

    plt.subplot(122)
    plt.plot(x, integral_y)
    plt.xlabel('x')
    plt.ylabel('integral y')

    plt.show()

