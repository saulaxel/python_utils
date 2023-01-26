from math import sin, cos, tan, asin, acos, atan, atan2, pi


def rad_to_grad(rad):
    return rad * 180 / pi


def grad_to_rad(grad):
    return grad * pi / 180


def grad_trig_function(fun):
    def grad_fun(grad):
        return fun(grad_to_rad(grad))

    return grad_fun


def grad_inv_trig_function(fun):
    def grad_fun(alpha):
        return rad_to_grad(fun(alpha))

    return grad_fun


gsin = grad_trig_function(sin)
gcos = grad_trig_function(cos)
gtan = grad_trig_function(tan)


gasin = grad_inv_trig_function(asin)
gacos = grad_inv_trig_function(acos)
gatan = grad_inv_trig_function(atan)
gatan2 = lambda dy, dx: rad_to_grad(atan2(dy, dx))
