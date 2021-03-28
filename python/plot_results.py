#!/usr/bin/env python

'''Plot results from an alpha/beta sweep.'''

import csv
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import math

def read_csv(filename):
    '''Read the specified CSV file and return an array of columns.'''
    with open(filename, 'r') as csvfile:
        rows = [r for r in csv.reader(csvfile)]
        return [
            [float(rows[row][col]) for row in range(0, len(rows))]
            for col in range(0, len(rows[0]))
        ]

def compare_sweep(alpha, beta, theory, experimental, label):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('alpha (degrees)')
    ax.set_ylabel('beta (degrees)')
    ax.set_zlabel(label)
    ax.legend([
        ax.scatter3D(alpha, beta, theory),
        ax.scatter3D(alpha, beta, experimental),
    ], [
        'theory',
        'experimental',
    ])
    plt.show()
    # If you want to save it instead, comment out the above line and
    # un-comment this one....
    # plt.savefig(label + '.png', dpi=600)
           
########################################################################
# Define column indexes in the original CSV file

COL_ALPHA = 0
COL_BETA  = 1
COL_Q     = 2  # Scanivalve ch 0, tunnel q
COL_C     = 3  # Scanivalve ch 1, (C)enter hole
COL_B     = 4  # Scanivalve ch 2, (B)ottom hole
COL_U     = 5  # Scanivalve ch 3, (U)pper hole
COL_D     = 6  # Scanivalve ch 4, (D)own hole
COL_L     = 7  # Scanivalve ch 5, (L)eft hole
COL_R     = 8  # Scanivalve ch 6, (R)ight hole

########################################################################
# Read the file and assign each column to a variable

file_name = input('Enter name of CSV file containing data: ')
columns = read_csv(file_name)

col_alpha = columns[COL_ALPHA]
col_beta  = columns[COL_BETA]
col_q     = columns[COL_Q]
col_c     = columns[COL_C]
col_b     = columns[COL_B]
col_u     = columns[COL_U]
col_d     = columns[COL_D]
col_l     = columns[COL_L]
col_r     = columns[COL_R]

########################################################################
# Convert experimental values to pressure coefficients

def limit(x):
    '''Limit values because random numbers are random.'''
    return min(max(x, -10.0), 10.0)

def coeff(d):
    return [
        limit(d[i] / col_q[i])
        for i in range(0, len(col_q))
    ]

col_c_coeff = coeff(col_c)
col_b_coeff = coeff(col_b)
col_u_coeff = coeff(col_u)
col_d_coeff = coeff(col_d)
col_l_coeff = coeff(col_l)
col_r_coeff = coeff(col_r)

########################################################################
# Compute theoretical values

def c_theory_fn(alpha, beta):
    '''Return pressure coefficient for center hole.'''
    # Totally fake formula!
    # TODO: Use proper formula
    return math.cos(math.radians(alpha) * 10) + math.sin(math.radians(beta) * 10)

col_c_theory = [
    c_theory_fn(col_alpha[i], col_beta[i])
    for i in range(0, len(col_alpha))
]

# TODO: Add theory for other holes

########################################################################
# Plot experimental curves

compare_sweep(col_alpha, col_beta, col_c_theory, col_c_coeff, 'Center hole')

# TODO: Add plots for other holes
