#! /usr/bin/env python

import argparse
import pathlib
import sys

import numpy as np
import pandas as pd

import sso_package.my_func as my_func

def initial_hs(func, x, error_bound):
    """Computes the initial step size for the 2nd order FD derivative (phi).

    This function takes in the user-defined single variable function,
    evaluation point (x) and error bound and returns an initial step size. 
    Methodology adapted from Gill.

    :param function func: The user-defined single variable function (i.e f(x))
    :param float x: The evaluation point for the 2nd order FD derivative operation
    :param float error_bound: User-defined error bound, typically prescribed as the machine precision.

    :returns: Initial step size value for the 2nd order FD derivative (phi)
    """
    
    # Evaluate function at evaluation point
    y = func(x)
    
    # Compute hs using double precision evaluation
    hs = 2*(1 + np.abs(x))*np.sqrt(error_bound/(1+np.abs(y)))

    return hs

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

def conditional_error(error_bound, hs, phi):
    """Computes the conditional error from user-defined error bound, current step size and 
    2nd-order central difference derivative approximation (phi).

    :param float error_bound: User-defined error bound, typically prescribed as the machine precision.
    :param float hs: The step size for the CFD operation to approximate the 2nd-order derivative
    :param float phi: The 2nd-order central difference approximation (phi)

    :returns: Float value for the conditional error to be optimized.
    """
    return (4*error_bound)/(hs**2*np.abs(phi))

def optimal_step_size(error_bound, phi):
    """Computes the optimal step size for the forward finite difference (FFD) approximation
    of the first derivative.

    :param float error_bound: User-defined error bound, typically prescribed as the machine precision.
    :param float phi: The 2nd-order central difference approximation (phi)

    :returns: Float value for the optimized step size for the FFD approximation
    """
    return 2*np.sqrt(error_bound/np.abs(phi))

def machine_precision():
    """Extracts machine precision value of the OS. Value used to optimize step size in Gill's method

    :returns: Float value for machine precision (epsilon) 
    """
    epsilon = sys.float_info.epsilon
    return epsilon

def main(evaluation_point, lower_c_bound, upper_c_bound, output_csv_filename, error_bound=None, max_iters=50, print_info=False):
    """Runs the algorithm to determine optimal step size for first derivative of a function 

    User-defined function is used and evaluated at the evaluation point. The algorithm
    uses passed in conditional error bounds and error bound parameters to minimize the total error
    on the finite difference calculation.
    
    :param float evaluation_point: Evaluation point passed into the function
    :param float lower_c_bound: Lower bound to threshold the conditional error
    :param float upper_c_bound: Upper bound to threshold the conditional error
    :param string output_csv_filename: Name of output csv containing algorithm data
    :param float error_bound: Error bound (Default: Machine precision)
    :param int max_iters: Maximum iterations of the optimization loop (Default: 50)
    :param boolean print_info: Prints the conditional error and optimized step size (Default: False)

    :returns: Pandas dataframe containing optimal step size history
    """
    # Set the variable equal to the single-variable function
    func = my_func.my_func

    # Initialize pandas dataframe and arrays to store data
    df = pd.DataFrame()
    iters_array = []
    cond_error_array = []
    hs_array = []
    h_optimal_array = []

    # Evaluation point
    x1 = evaluation_point

    # Get machine precision if no value is passed for error_bound
    if error_bound == None:
        error_bound = machine_precision()
     
    # Compute initial step size
    hs_initial = initial_hs(func, x1, error_bound)
    
    # Compute initial phi
    phi = central_difference(func, x1, hs_initial)
    
    # Compute  initial conditional error
    cond_error_current = conditional_error(error_bound, hs_initial, phi)

    # Compute initial step size based off initial parameters
    h_optimal_initial = optimal_step_size(error_bound, phi)

    # Initialize iterations to prevent infinite looping
    iter = 0

    # Append initialized values to arrays
    iters_array.append(iter)
    cond_error_array.append(cond_error_current)
    hs_array.append(hs_initial)
    h_optimal_array.append(h_optimal_initial)

    # Setup optimization loop
    while cond_error_current < lower_c_bound or cond_error_current > upper_c_bound:
        
        # Update hs and phi if conditional error is out of bounds
        if cond_error_current > upper_c_bound:
            hs = hs_initial*10
            phi = central_difference(func, x1, hs)
        
        elif cond_error_current < lower_c_bound:
            hs = hs_initial/10
            phi = central_difference(func, x1, hs)
        
        # Compute conditional error with updated values
        cond_error_current = conditional_error(error_bound, hs, phi)

        # Compute optimal step size based off current evaluations
        h_optimal_current = optimal_step_size(error_bound, phi)

        # Append initialized values to arrays
        iters_array.append(iter)
        cond_error_array.append(cond_error_current)
        hs_array.append(hs)
        h_optimal_array.append(h_optimal_current)

        # Update number of iterations
        iter += 1
        if iter >= max_iters:
            break
    
    # Print information to console
    if print_info == True:
        print(f'iteration: {iter}')
        print(f'error bound: {error_bound}')
        print(f'conditional error, in range ({lower_c_bound}, {upper_c_bound}): {cond_error_current}')
        print(f'optimized step size: {h_optimal_current}')
    
    # Write data to dataframe 
    df['Iteration'] = iters_array
    df['Cond. Error'] = cond_error_array
    df['2nd-order step size'] = hs_array
    df['1st-order optimal step size'] = h_optimal_array

    # Export to file
    df.to_csv(output_csv_filename)

    return 0

def get_parser():
    script_name = pathlib.Path(__file__)
    prog = f"python {script_name.name} "
    cli_description = "Optimize the forward finite difference (FFD) step size using Gill's method"
    parser=argparse.ArgumentParser(description=cli_description, prog=prog)

    parser.add_argument('--evaluation_point', type=float, required=True,
        help="The evaluation point for the FFD approximation")
    parser.add_argument('--lower_c_bound', type=float, default=0.001,
        help="The lower error bound threshold. Default: 0.001")
    parser.add_argument('--upper_c_bound', type=float, default=0.1,
        help="The upper error bound threshold. Default: 0.1")
    parser.add_argument('--output_csv_filename', type=str, required=False, default="gill_optimizer.csv",
        help="Name of output csv file if given. Default: gill_optimizer.csv")
    parser.add_argument('--error_bound', type=float, required=False,
        help="The user-defined error bound, typically it is the machine precision")
    parser.add_argument('--max_iters', type=float, default=50, required=False,
        help="Max iterations to optimize the step size. Default is 50.")
    parser.add_argument('--print_info', type=bool, default=True, required=False,
        help="Print optimzer information to the console")
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args, unknown = parser.parse_known_args()
    sys.exit(main(evaluation_point=args.evaluation_point,
                                error_bound=args.error_bound,
                                lower_c_bound=args.lower_c_bound,
                                upper_c_bound=args.upper_c_bound,
                                output_csv_filename=args.output_csv_filename,
                                max_iters=args.max_iters,
                                print_info=args.print_info
                                ))