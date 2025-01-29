#! /usr/bin/env python

import numpy as np

def my_func(x):
    try:
        return np.exp(x)/np.sqrt(np.sin(x)**3 + np.cos(x)**3)
    except RuntimeWarning:
        return 0
    except ZeroDivisionError:
        return 0