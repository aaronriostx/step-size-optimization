#! /usr/bin/env python

def initial_hs(func, x, error_bound):
    """Computes the initial step size for the 2nd order FD derivative (phi).

    This function takes in the user-defined single variable function,
    evaluation point (x) and error bound and returns an initial step size. 
    Methodology adapted from Gill.

    :param function func: The user-defined single variable function (i.e f(x))
    :param float x: The evaluation point for the 2nd order FD derivative operation
    :parm float error_bound: User-defined error bound, typically prescribed as the machine precision.

    :returns: Initial step size value for the 2nd order FD derivative (phi)
    """
    
    # Evaluate function at evaluation point
    y = func(x)
    
    # Compute hs using double precision evaluation
    hs = 2*(1 + np.abs(x))*np.sqrt(error_bound/(1+np.abs(y)))

    return hs