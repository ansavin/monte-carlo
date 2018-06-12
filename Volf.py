#!/usr/bin/python3
''' Program for modelling
    3d izing model using
    Volf claster method
'''
#import************************************************************************
import math
import random as rnd
import copy
import numpy as np
import sys
from MCfunctions import *

#parameters********************************************************************
s = []
verbose = 0
s0 = []
E1 = 0
E0 = 0
C = 0
aver = 5
M_mean = 0
M2_mean = 0
E_mean = 0
E2_mean = 0
N_steps = 10000
d1 = 4
d2 = 4
d3 = 4
J = 1
H = 0
b = 4
coords = []

#functions*********************************************************************

def getNextCoord(i, i_old, di):
    if not i:
            i_new = prevInd(i_old, di)
    else: 
            i_new = nextInd(i_old, di)
    return i_new
    
def check(i_old, j_old, k_old, i_new, j_new, k_new):
    if not s[i_old][j_old][k_old] == s[i_new][j_new][k_new]:
                    xi = rnd.uniform(0,1)
                    if xi <= (1 - math.exp(-2 * J / b)):
                        s[i_new][j_new][k_new] *= -1 
                        coords.append([i_new, j_new, k_new])
    pass
def step(i_old, j_old, k_old):
    for i in range(2):
        i_new = getNextCoord(i, i_old, d1)
        check(i_old, j_old, k_old, i_new, j_old, k_old)
    for j in range(2):
        j_new = getNextCoord(j, j_old, d2)
        check(i_old, j_old, k_old, i_old, j_new, k_old)
    for k in range(2):
        k_new = getNextCoord(k, k_old, d3)     
        check(i_old, j_old, k_old, i_old, j_old, k_new)
    pass

def zerostep():
    xi_i = rnd.randint(0,d1 - 1)
    xi_j = rnd.randint(0,d2 - 1)
    xi_k = rnd.randint(0,d3 - 1)
    s[xi_i][xi_j][xi_k] *= -1 
    return xi_i, xi_j, xi_k

def nextKnot():
    coord = coords.pop()
    return coord[0], coord[1], coord[2]
    
    
#main part*********************************************************************

# input
b, human, debug = consoleInput()

print('''
         ****************************
         *    modelling 3d Izing    *
         *    ferromagnetic media   *
         *     with Volf method     *
         ****************************
      ''')

initIZ(s,d1,d2,d3)

if verbose:
    print('s0 = ',s)

for counter in range(N_steps):
    i, j, k = zerostep()
    step(i, j, k)
    if verbose:
        print('s` = ',s)
    while coords:
        i, j, k = nextKnot()
        step(i, j, k)
        if verbose:
            print('coords = ',coords) 
    E0 = countEIZ(s,d1,d2,d3,H,J) 
    E2_mean += E0 ** 2
    E_mean += E0
    M_mean_i, M2_mean_i = meanM(s)
    M_mean += M_mean_i
    M2_mean += M2_mean_i
    sys.stdout.write("{0} % complete\r".format(math.floor(100 * (counter / N_steps))))

M_mean /= N_steps
M2_mean /= N_steps
E_mean /= N_steps
E2_mean /= N_steps
C = calcFluct(E_mean, E2_mean) / (b ** 2)
M = calcFluct(M_mean, M2_mean) / b

h = open('Volf.dat','a')
h.write("{0} {1} {2} {3} {4}\n".format(b, E_mean, C, M_mean, M))
h.close()

#output************************************************************************


print()
print('E = {0}, C = {1}, S = {2}, M = {3}'.format(E_mean, C, M_mean, M))
print('final s = ',s)

h = open('volf.dat','a')
h.write("{0} {1} {2} {3} {4}\n".format(b, E_mean, C, M_mean, M))
h.close()
