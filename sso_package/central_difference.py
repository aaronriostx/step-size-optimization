#! /usr/bin/env python

def central_difference(func, x, hs):
    """Performs the central finite difference (CFD) operation on a single-variable function
    to approximate the 2nd-order derivative.

    This function takes in a single-variable function at a given evaluation point (x) and step size (hs)

    :param function func: The user-defined single variable function (i.e f(x))
    :param float x: The evaluation point for the FFD operation
    :param float hs: The step size for the CFD operation to approximate the 2nd-order derivative

    :returns: Float value for CFD 2nd-order derivative (phi) at evaluation point, x
    """
    
    # Compute Phi
    phi = (func(x+hs) - 2*func(x) + func(x-hs))/hs**2
    
    return phi