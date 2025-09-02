
# factorial
try:
    from math import factorial
except ImportError:
    def factorial(n):
        """Returns n factorial"""
        f = 1
        for i in range(2, n + 1):
            f *= i
        return f

# comb
try:
    from math import comb
except ImportError:
    def comb(n, k):
        """
        Return the number of ways to choose k items from n items without
        repetition and without order
        """
        return factorial(n) / (factorial(k) * factorial(n - k))

# perm
try:
    from math import perm
except ImportError:
    def perm(n, k):
        """
        Return the number of ways to choose k items from n items without
        repetition and with order
        """
        return factorial(n) / factorial(n - k)

# isclose
try:
    from math import isclose
except ImportError:
    # https://docs.python.org/3/library/math.html
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        """
        Return True if the values a and b are close to each other and False
        otherwise
        """
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


# isfinite
from math import isinf, isnan
try:
    from math import isfinite
except ImportError:
    def isfinite(x):
        """True if x is neither an infinity nor a NaN, False otherwise"""
        return not isinf(x) and not isnan(x)


if __name__ == '__main__':
    assert factorial(2) == 2
    assert factorial(4) == 24

    assert comb(3, 1) == 3
    assert comb(3, 2) == 3
    assert comb(3, 3) == 1

    assert perm(3, 1) == 3
    assert perm(3, 2) == 6
    assert perm(3, 3) == 6

    assert isclose(10, 10) == True
    assert isclose(0, 1) == False

    assert isfinite(10) == True
    assert isfinite(float('inf')) == False
    assert isfinite(float('nan')) == False
