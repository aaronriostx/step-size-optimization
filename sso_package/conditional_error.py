#! /usr/bin/env python

def conditional_error(error_bound, hs, phi):
    """Computes the conditional error from user-defined error bound, current step size and 
    2nd-order central difference derivative approximation (phi).

    :param float error_bound: User-defined error bound, typically prescribed as the machine precision.
    :param float hs: The step size for the CFD operation to approximate the 2nd-order derivative
    :param float phi: The 2nd-order central difference approximation (phi)

    :returns: Float value for the conditional error to be optimized.
    """
    return (4*error_bound)/(hs**2*np.abs(phi))