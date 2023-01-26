#https://www.baeldung.com/cs/array-generate-all-permutations
# Auxiliares

def es_impar(n):
    return n % 2 != 0


def swap(lista, idx1, idx2):
    lista[idx1], lista[idx2] = lista[idx2], lista[idx1]


def exclude_index(sequence, index):
    return tuple(x for i, x in enumerate(sequence) if i != index)

### Funciones principales

def permutaciones_ordenadas_aux(elements, current_permutation, permutation_list):
    if elements:
        for i, element in enumerate(elements):
            next_permutation = current_permutation + (element,)
            remaining_elements = exclude_index(elements, i)
            permutaciones_ordenadas_aux(remaining_elements, next_permutation, permutation_list)
    else:
        permutation_list.append(current_permutation)



def permutaciones_ordenadas(elements):
    permutation_list = []
    permutaciones_ordenadas_aux(elements, (), permutation_list)
    return permutation_list


def permutaciones(elementos):
    elementos = list(elementos)
    lista_permutaciones = []
    num_elementos = len(elementos)

    lista_permutaciones.append(tuple(elementos))

    p = [i for i in range(num_elementos + 1)]

    index = 1
    while index < num_elementos:
        p[index] -= 1
        if es_impar(index):
            j = p[index]
        else:
            j = 0

        swap(elementos, j, index)
        lista_permutaciones.append(tuple(elementos))

        index = 1
        while p[index] == 0:
            p[index] = index
            index = index + 1

    return lista_permutaciones

if __name__ == '__main__':
    def mismos_elementos(res, esperada):
        res_ordenada = sorted(res)
        esperada_ordenada = sorted(esperada)
        assert res_ordenada == esperada_ordenada

    def main():
        funciones_ordenadas_a_probar = [
                (permutaciones_ordenadas, 'ordenada'),
                (permutaciones, 'no-ordenada'),
        ]

        for fun, tipo in funciones_ordenadas_a_probar:
            t0 = (True,)
            esperada0 = [(True,)]
            res0 = fun(t0)
            assert res0 == esperada0

            t1 = (1, 2)
            esperada1 = [(1, 2), (2, 1)]
            res1 = fun(t1)
            if tipo == 'ordenada':
                assert res1 == esperada1
            else:
                mismos_elementos(res1, esperada1)

            t2 = ('A', 'B', 'C')
            esperada2 = [('A', 'B', 'C'), ('A', 'C', 'B'),
                    ('B', 'A', 'C'), ('B', 'C', 'A'),
                    ('C', 'A', 'B'), ('C', 'B', 'A')]

            res2 = fun(t2)
            if tipo == 'ordenada':
                assert res2 == esperada2
            else:
                mismos_elementos(res2, esperada2)

    main()

