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
    return min(max(x, -1.0), 1.0)

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

# This is the core formula that computes the pressure at a given point
# on a sphere as a function of angular offset from the stagnation point.
# The result is a ratio of the stagnation pressure _q_. The angle is
# given in radians.

def sphere_coeff_polar(angle):
    def cos_sq(x):
        y = math.cos(x)
        return y * y
    return 1.0 - 9.0 / 4.0 * cos_sq(math.radians(angle)- math.pi / 2.0)

# This formula takes two angles, alpha and beta, and computes the
# pressure coefficient at the given point using the distance formula.

def sphere_coeff_cartesian(alpha, beta):
    return sphere_coeff_polar(
        math.sqrt(alpha * alpha + beta * beta))

col_c_theory = [
    sphere_coeff_cartesian(col_alpha[i], col_beta[i])
    for i in range(0, len(col_alpha))
]

col_b_theory = [
    sphere_coeff_cartesian(col_alpha[i] - 90, col_beta[i])
    for i in range(0, len(col_alpha))
]

col_u_theory = [
    sphere_coeff_cartesian(col_alpha[i] + 45, col_beta[i])
    for i in range(0, len(col_alpha))
]

col_d_theory = [
    sphere_coeff_cartesian(col_alpha[i] - 45, col_beta[i])
    for i in range(0, len(col_alpha))
]

col_l_theory = [
    sphere_coeff_cartesian(col_alpha[i], col_beta[i] + 45)
    for i in range(0, len(col_alpha))
]

col_r_theory = [
    sphere_coeff_cartesian(col_alpha[i], col_beta[i] - 45)
    for i in range(0, len(col_alpha))
]

########################################################################
# Plot experimental curves

compare_sweep(col_alpha, col_beta, col_c_theory, col_c_coeff, 'Center hole')
compare_sweep(col_alpha, col_beta, col_b_theory, col_b_coeff, 'Bottom hole')
compare_sweep(col_alpha, col_beta, col_u_theory, col_u_coeff, 'Upper hole')
compare_sweep(col_alpha, col_beta, col_d_theory, col_d_coeff, 'Down hole')
compare_sweep(col_alpha, col_beta, col_l_theory, col_l_coeff, 'Left hole')
compare_sweep(col_alpha, col_beta, col_r_theory, col_r_coeff, 'Right hole')

# TODO: Add plots for other holes
