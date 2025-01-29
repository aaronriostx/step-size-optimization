#! /usr/bin/env python

def forward_difference(func, x, h):
    """Performs the forward finite difference (FFD) operation on a single-variable function.

    This function takes in a single-variable function at a given evaluation point (x) and step size (h)

    :param function func: The user-defined single variable function (i.e f(x))
    :param float x: The evaluation point for the FFD operation
    :parm float h: The step size for the FFD operation

    :returns: Float value for FFD derivative at evaluation point, x
    """
    return (func(x+h) - func(x))/h