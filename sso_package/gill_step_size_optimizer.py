#! /usr/bin/env python

import argparse
import numpy as np
import pathlib
import sys

import sso_package.initial_hs
import sso_package.central_difference
import sso_package.conditional_error
import sso_package.optimal_step_size

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
    hs_initial = initial_hs(func, x1, error_bound)
    
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
    
    return 0

def get_parser():
    script_name = pathlib.Path(__file__)
    prog = f"python {script_name.name} "
    cli_description = "Optimize the forward finite difference (FFD) step size using Gill's method"
    parser=argparse.ArgumentParser(description=cli_description, prog=prog)

    parser.add_argument('--func', required=True,
        help="A single-variable function used to estimate the FFD approximation")
    parser.add_argument('--evaluation_point', type=float, required=True,
        help="The evaluation point for the FFD approximation")
    parser.add_argument('--error_bound', type=float, required=True,
        help="The user-defined error bound, typically it is the machine precision")
    parser.add_argument('--conditional_error_bounds', type=tuple, required=True,
        help="The user-defined error bound threshold")
    parser.add_argument('--max_iters', type=float, default=50, required=False,
        help="Max iterations to optimize the step size. Default is 50.")
    parser.add_argument('--print_info', type=bool, default=True, required=False,
        help="Print optimzer information to the console")
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args, unknown = parser.parse_known_args()
    sys.exit(optimize_step_size(func=args.func,
                                evaluation_point=args.evaluation_point,
                                error_bound=args.error_bound,
                                conditional_error_bounds=args.conditional_error_bounds,
                                max_iters=args.max_iters,
                                print_info=args.print_info
                                ))