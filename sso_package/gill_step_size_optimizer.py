#! /usr/bin/env python

import numpy as np

def optimize_step_size(func, evaluation_point, error_bound, conditional_error_bounds, max_iters=50, print_info=False):
    """Runs the algorithm to determine optimal step size for first derivative of a function 

    User-defined function is used and evaluated at the evaluation point. The algorithm
    uses passed in conditional error bounds and error bound parameters to minimize the total error
    on the finite difference calculation.
    
    :param function func: Analytical function that takes in single evaluation point
    :param float evaluation_point: Evaluation point passed into the function
    :param float error_bound: User-defined error bound
    :param tuple conditional_error_bounds: Lower and upper limit to threshold the conditional error, i.e. (0.001, 0.1)
    :param int max_iters: Maximum iterations of the optimization loop (Default: 50)
    :param boolean print_info: Prints the conditional error and optimized step size (Default: False)

    :returns: optimized step size for the finite difference calculation
    """
    # Evaluation point
    x1 = evaluation_point
    
    # Bounds for the conditional error
    lower_bound = conditional_error_bounds[0]
    upper_bound = conditional_error_bounds[1]
     
    # Compute initial step size
    hs_initial = compute_initial_hs(func, x1, error_bound)
    
    # Compute initial phi
    phi = central_difference(func, x1, hs_initial)
    
    # Compute  initial conditional error
    cond_error = conditional_error(error_bound, hs_initial, phi)

    # Initialize iterations to prevent infinite looping
    iter = 0
    
    # Setup conditional loop
    while cond_error < lower_bound or cond_error > upper_bound:
        
        # Update hs and phi if conditional error is out of bounds
        if cond_error > upper_bound:
            hs = hs_initial*10
            phi = central_difference(func, x1, hs)
        
        elif cond_error < lower_bound:
            hs = hs_initial/10
            phi = central_difference(func, x1, hs)
        
        # Compute conditional error with updated values
        cond_error = conditional_error(error_bound, hs, phi)

        # Check number of iterations
        iter += 1
        if iter >= max_iters:
            break
        
    # Return the optimal step size
    h_optimal = optimal_step_size(error_bound, phi)
    
    # Print information to console
    if print_info == True:
        print(f'iteration: {iter}')
        print(f'conditional error: {cond_error}')
        print(f'optimized step size: {h_optimal}')
    
    return h_optimal