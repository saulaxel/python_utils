import sympy as sp
from typing import Any


def sub_euler1(t: sp.Symbol, a, b, c) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """
    t: Substitution variable (a sympy Symbol)
    a, b, c: Coefficients ax^2 + bx + c

    Returns: x_t, dx_dt, sqrt_pol_t
    """
    if a <= 0:
        raise ValueError('The first Euler substitution works for a > 0')

    denom = (b - 2*sp.sqrt(a)*t)
    x_t = (t**2 - c) / denom
    dx_dt = (-2*sp.sqrt(a)*t**2 + 2*b*t - 2*sp.sqrt(a)*c) / denom**2
    sqrt_pol_t = (-sp.sqrt(a)*t**2 + b*t - sp.sqrt(a)*c) / denom
    return x_t, dx_dt, sqrt_pol_t


def sub_euler2(t: sp.Symbol, a, b, c) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """
    t: Substitution variable (A sympy Symbol)
    a, b, c: Coefficients ax^2 + bx + c

    Returns: x_t, dx_dt, sqrt_pol_t
    """
    if c <= 0:
        raise ValueError('The second Euler substitution works for c > 0')

    denom = (t**2 - a)
    x_t = (b - 2*sp.sqrt(c)*t) / denom
    dx_dt = (2*sp.sqrt(c)*t**2 - 2*b*t + 2*a*sp.sqrt(c)) / denom**2
    sqrt_pol_t = (-sp.sqrt(c)*t**2 + b*t - a*sp.sqrt(c)) / denom
    return x_t, dx_dt, sqrt_pol_t


def sub_euler3(t: sp.Symbol, a, r1, r2) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """
    t: Substitution variable (a sympy Symbol)
    a, r1, r2: Coefficients ax^2 + bx + c = a(x - r1)(x - r2)

    Returns: x_t, dx_dt, sqrt_pol_t
    """
    denom = (t**2 - a)
    x_t = (r1*t**2 - a*r2) / denom
    dx_dt = (2*a*t*(r2 - r1)) / denom
    sqrt_pol_t = (a*t*(r1 - r2)) / denom
    return x_t, dx_dt, sqrt_pol_t


def sympy_exp_equals(exp1, exp2):
    print(exp1, '==', exp2)
    return sp.simplify(exp1 - exp2) == 0

def test_this():
    x = sp.Symbol('x')
    t = sp.Symbol('t')

    print('Euler Case 1 Start')
    print('sqrt(4x^2 + 1)')
    x_t, dx_dt, sqrt_pol_t = sub_euler1(t, a=4, b=0, c=1)
    assert sympy_exp_equals(x_t, -(t**2 - 1) / (4*t) )
    assert sympy_exp_equals(dx_dt, -(t**2 + 1) / (4*t**2))
    assert sympy_exp_equals(sqrt_pol_t, (t**2 + 1) / (2*t))

    print('sqrt(x^2 - 1)')
    x_t, dx_dt, sqrt_pol_t = sub_euler1(t, a=1, b=0, c=-1)
    assert sympy_exp_equals(x_t, -(t**2 + 1) / (2*t) )
    assert sympy_exp_equals(dx_dt, -(t**2 - 1) / (2*t**2))
    assert sympy_exp_equals(sqrt_pol_t, (t**2 - 1) / (2*t))

    print('sqrt(x^2 - 3x + 2)')
    x_t, dx_dt, sqrt_pol_t = sub_euler1(t, a=1, b=-3, c=2)
    assert sympy_exp_equals(x_t, -(t**2 - 2) / (2*t + 3) )
    assert sympy_exp_equals(dx_dt, -2 * (t**2 + 3*t + 2) / (2*t + 3)**2 )
    assert sympy_exp_equals(sqrt_pol_t, (t**2 + 3*t + 2) / (2*t + 3))

    print('sqrt(-x^2 - x + 1)')
    try:
        x_t, dx_dt, sqrt_pol_t = sub_euler1(t, a=-1, b=-1, c=1)
    except ValueError:
        print('\'a\' must be positive \\o/')
    print("Euler Case 1 End")

    print()

    print('Euler Case 2 Start')
    print('sqrt(4x^2 + 1)')
    x_t, dx_dt, sqrt_pol_t = sub_euler2(t, a=4, b=0, c=1)
    assert sympy_exp_equals(x_t, (-2*t) / (t**2 - 4) )
    assert sympy_exp_equals(dx_dt, (2*t**2 + 8) / (t**2 - 4)**2 )
    assert sympy_exp_equals(sqrt_pol_t, (-t**2 - 4) / (t**2 - 4) )

    print('sqrt(x^2 - 1)')
    try:
        x_t, dx_dt, sqrt_pol_t = sub_euler1(t, a=1, b=0, c=-1)
    except ValueError:
        print('\'c\' must be positive \\o/')

    print('sqrt(x^2 - 3x + 2)')
    x_t, dx_dt, sqrt_pol_t = sub_euler2(t, a=1, b=-3, c=2)
    s2 = sp.sqrt(2)
    assert sympy_exp_equals(x_t, -(2*s2*t + 3) / (t**2 - 1) )
    assert sympy_exp_equals(dx_dt, 2 * (s2*t**2 + 3*t + s2) / (t**2 - 1)**2 )
    assert sympy_exp_equals(sqrt_pol_t, -(s2*t**2 + 3*t + s2) / (t**2 - 1))

    print('sqrt(-x^2 - x + 1)')
    x_t, dx_dt, sqrt_pol_t = sub_euler2(t, a=-1, b=-1, c=1)
    assert sympy_exp_equals(x_t, - (2*t + 1) / (t**2 + 1) )
    assert sympy_exp_equals(dx_dt, (2*t**2 + 2*t - 2) / (t**2 + 1)**2 )
    assert sympy_exp_equals(sqrt_pol_t, (-t**2 - t + 1) / (t**2 + 1) )

    print('Euler Case 2 End')

    print()
    print("Euler Case 3 Start")

    print('sqrt(x^2 - 1) = sqrt((x - 1)(x + 1))')
    x_t, dx_dt, sqrt_pol_t = sub_euler3(t, a=1, r1=1, r2=-1)
    assert sympy_exp_equals(x_t, (t**2 + 1) / (t**2 - 1) )
    assert sympy_exp_equals(dx_dt, -4*t / (t**2 - 1))
    assert sympy_exp_equals(sqrt_pol_t, 2*t / (t**2 - 1))

    print('sqrt(x^2 - 3x + 2) = sqrt((x - 1)(x - 2))')
    x_t, dx_dt, sqrt_pol_t = sub_euler3(t, a=1, r1=1, r2=2)
    s2 = sp.sqrt(2)
    assert sympy_exp_equals(x_t, (t**2 - 2) / (t**2 - 1) )
    assert sympy_exp_equals(dx_dt, (2*t) / (t**2 - 1) )
    assert sympy_exp_equals(sqrt_pol_t, -(t) / (t**2 - 1))

    print("Euler Case 3 End")

    print()
    print('End of test')


if __name__ == '__main__':
    test_this()
