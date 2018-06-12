#!/usr/bin/python3
''' Program for modelling
    3d izing model
'''
#import************************************************************************
import math
import random as rnd
import copy
import numpy as np
import sys
from MCfunctions import *

#parameters********************************************************************
N_MC = 100000                    # Redefining number of MC steps to simulate
aver = 5                         # how many experiments to do for averaging
b = 4                            # dimensionless temperature 
b0 = 2                           # left border for t array (min. temperature)
bn = 5                           # right border for t array (max. temperature)
num_b = 10                       # how many experiments for different t to do
bs = [b]                         # array for all t 
d1 = 4                           # X dimension
d2 = 4                           # Y dimension
d3 = 4                           # Z dimension
J = 1                            # Physical const in Izing Hamiltonian
H = 0                            # Value of Magnetic field in Izing Hamiltonian

#functions*********************************************************************

# initialyzing spins
def initIZall(s0):
    initIZ(s0, d1, d2, d3)
    E = countEIZ(s,d1,d2,d3,H,J)    
    E0 = countEIZ(s0,d1,d2,d3,H,J)
    return E, E0

#main part*********************************************************************

# input 
if len(sys.argv) == 2:
    d1 = d2 = d3 = int(sys.argv[1])
    bs = np.linspace(b0, bn, num_b)
    human = 0
    debug = 0
elif len(sys.argv) == 3:
    d1 = d2 = d3 = int(sys.argv[1])
    b = float(sys.argv[2])
    bs = [b]
    debug = 0
    human = 0
elif len(sys.argv) == 4:
    d1 = d2 = d3 = int(sys.argv[1])
    b = float(sys.argv[2])
    bs = [b]
    human = int(sys.argv[3])
    debug = 0
elif len(sys.argv) > 4:
    d1 = d2 = d3 = int(sys.argv[1])
    b = float(sys.argv[2])
    bs = [b]
    human = int(sys.argv[3])
    debug = int(sys.argv[4])

if human:
    print('''
         ****************************
         *    modelling 3d Izing    *
         *    ferromagnetic media   *
         *         model            *
         ****************************
      ''')
for b_i in bs:

    s = []                   # array of spins
    s0 = []                  # array of previous step spins  
    E1 = 0                   # energy of the system
    E0 = 0                   # energy on previous step
    C = 0                    # thermal conductivity
    xi = 0                   # magnetical susceptibility
    M_mean = 0               # mean magnetization
    M2_mean = 0              # mean square magnetization
    E_mean = 0               # mean energy
    E2_mean = 0              # mean square energy

    if human:
        print('///Start modelling with {0} MC steps///'.format(N_MC))
    E, E0 = initIZall(s0)
    s = copy.deepcopy(s0)
    if human:
        print('initial E = {0}'.format(E0))
    if debug:
        print(s0)
    for counter in range(N_MC):
            metroFlipIZ(s,d1,d2,d3)
            E1 = countEIZ(s,d1,d2,d3,H,J)
            condition = metroCheck(E1 / b_i, E0 / b_i, E_max)
            if condition:
                s0 = copy.deepcopy(s)
                E0 = E1
            s = copy.deepcopy(s0)
            E2_mean += E0 ** 2
            E_mean += E0
            M_mean_i, M2_mean_i = meanM(s)
            M_mean += M_mean_i
            M2_mean += M2_mean_i
            if debug:
                print('i = {0} M = {1} M2 = {2}'.format(counter, M_mean, M2_mean))
            if debug:
                g.write('i= {0} x= {1} \n x0= {2}{3}\n'.format(counter,s,s0, condition))
                f.write('{0} {1} {2} {3}\n'.format(counter,E0,E1,condition))
            if human:
                sys.stdout.write("{0} % complete\r".format(math.floor(100 * (counter / N_MC))))

    M_mean /= N_MC
    M2_mean /= N_MC
    E_mean /= N_MC  
    E2_mean /= N_MC  
    C = calcFluct(E_mean, E2_mean) / (b_i ** 2)
    xi = calcFluct(M_mean, M2_mean) / b_i

    #output************************************************************************
    if human:
        print()
        print('E = {0}, C = {1}, S = {2}, M = {3}'.format(E_mean, C, M_mean, xi))
        print('System final configuration:')
        for i in range(len(s)):
            for j in range(len(s[i])):
                for k in range(len(s[i][j])):
                    print('i={0} j={1} k={2} => {3}'.format(i,j,k,s[i][j][k]))
    else: 
        name = 'izing' + str(d1) + '.dat'
        h = open(name,'a')
        h.write("{0} {1} {2} {3} {4}\n".format(b_i, E_mean, C, M_mean, xi))
        h.close()
