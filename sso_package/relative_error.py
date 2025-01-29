#! /usr/bin/env python

import numpy as np

def relative_error(measured, real):
    """Computes the relative error between the measured and real value

    :param float measured: The measured or computed value
    :param float real: The "real" or reference value

    :returns: Float value for relative error between 2 values
    """
    return np.abs(measured-real)/np.abs(real)