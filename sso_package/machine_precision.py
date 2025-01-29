#! /usr/bin/env python

import sys

def machine_precision():
    """Extracts machine precision value of the OS. Value used to optimize step size in Gill's method

    :returns: Float value for machine precision (epsilon) 
    """
    epsilon = sys.float_info.epsilon
    return epsilon