#! /usr/bin/env python

import numpy as np

def optimal_step_size(error_bound, phi):
    """Computes the optimal step size for the forward finite difference (FFD) approximation
    of the first derivative.

    :param float error_bound: User-defined error bound, typically prescribed as the machine precision.
    :param float phi: The 2nd-order central difference approximation (phi)

    :returns: Float value for the optimized step size for the FFD approximation
    """
    return 2*np.sqrt(error_bound/np.abs(phi))