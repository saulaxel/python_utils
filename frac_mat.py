import numpy as np
from frac import Frac
from tabulate import tabulate
from functools import wraps


class FracMat:
    def __init__(self, *M):
        self.M = np.array([[Frac(col) for col in line] for line in M])


    @staticmethod
    def diagonal(vec):
        largo = len(vec)

        ret = np.array(
            [[(vec[n] if m == n else 0)
              for m in range(largo)]
             for n in range(largo)
        ])

        return FracMat(*ret)

    @property
    def shape(self):
        return self.M.shape

    def __getitem__(self, *args, **kwargs):
        return self.M.__getitem__(*args, **kwargs)


    def __setitem__(self, *args, **kwargs):
        self.M.__setitem__(*args, **kwargs)


    def __eq__(self, other):
        return self.M == other.M


    def __mul__(self, other):
        M1 = self.M
        lines1, cols1 = M1.shape

        if isinstance(other, FracMat):
            M2 = other.M
            lines2, cols2 = M2.shape

            assert cols1 == lines2

            res = np.zeros((lines1, cols2), dtype='object')

            for l in np.arange(lines1):
                for c in np.arange(cols2):

                    res[l][c] = Frac(0)

                    for k in np.arange(cols1):
                        res[l][c] += M1[l, k] * M2[k, c]

            return FracMat(*res)
        elif isinstance(other, Frac) or isinstance(other, int):
            res = np.zeros((lines1, cols1), dtype='object')

            for l in np.arange(lines1):
                for c in np.arange(cols1):
                    res[l, c] = M1[l, c] * other

            return FracMat(*res)
        else:
            raise ValueError('Not implemented')


    def __add__(self, other):
        M1 = self.M
        M2 = other.M
        lines1, cols1 = M1.shape
        lines2, cols2 = M2.shape

        assert lines1 == lines2 and cols1 == cols2

        res = np.zeros((lines1, cols1), dtype='object')

        for l in np.arange(lines1):
            for c in np.arange(cols2):

                res[l][c] = M1[l, c] + M2[l, c]

        return FracMat(*res)


    def __sub__(self, other):
        return self.__add__(-other)


    def __neg__(self):
        M = self.M
        lines, cols = M.shape
        res = np.zeros((lines, cols), dtype='object')

        for l in np.arange(lines):
            for c in np.arange(cols):
                res[l, c] = -M[l, c]

        return FracMat(*res)


    @property
    def T(self):
        lines, cols = self.M.shape
        t = [[self.M[line, col] for line in np.arange(lines)] for col in np.arange(cols)]
        return FracMat(*t)


    def __repr__(self):
        """
        ╒      ╕
        │ 1  2 │
        │ 3  4 │
        ╘      ╛
        """

        num_columns = self.M.shape[1]
        max_col_len = [0] * num_columns
        content_list = []

        for line in self.M:
            column_list = []
            for i, col in enumerate(line):
                col_string = str(col)
                if len(col_string) > max_col_len[i]:
                    max_col_len[i] = len(col_string)

                column_list.append(col_string)

            content_list.append(column_list)


        spaces_between_cols = 5
        str_sbc = ' ' * spaces_between_cols


        content_len = sum(max_col_len) + (num_columns - 1) * spaces_between_cols + 2
        space = ' ' * content_len
        first = f'╒{space}╕'

        middle_list = []
        for column_list in content_list:
            line = []
            for col, col_length in zip(column_list, max_col_len):
                col_padded = col.rjust(col_length)
                line.append(col_padded)

            middle_list.append(f'│ {str_sbc.join(line)} │')

        middle =  '\n'.join(middle_list)
        last = f'╘{space}╛'

        full_matrix = f'{first}\n{middle}\n{last}'

        return full_matrix



operators_to_override = (
    '__truediv__',
)

for name in operators_to_override:

    @wraps(getattr(np.ndarray, name))
    def method(self, *args, _method_name=name, **kwargs):

        original_method = getattr(self.M, _method_name)

        ret = original_method(*args, **kwargs)

        if ret is not None:

            return FracMat(*ret)


    setattr(FracMat, name, method)



if __name__ == '__main__':
    M = FracMat(
        [1, "2/5", -123],
        [30, -75, 12]
    )
    Mt = FracMat(
        [1, 30],
        ["2/5", -75],
        [-123, 12],
    )
    assert M.shape == (2, 3)
    assert np.all(M.T == Mt)
