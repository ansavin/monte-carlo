#!/usr/bin/python3
''' Program for calculating quantum
    3d oscillator mean energy using
    Metropolis algorithm
'''
#import************************************************************************
import math
import random as rnd
import copy
from multiprocessing import Pool 
import sys
from MCfunctions import *

#main part*********************************************************************

b, human, debug = consoleInput()

if human:
	print('**********************')
	print('* modelling quantum  *')
	print('* oscillator         *')
	print('**********************')
	print('N_MC= ', N_MC, 'b = ', b, 'n = ',n)

Ek, Ep, E_0 = MC_init(x, x_0, b)

for i in range(N_MC):
        metroFlip(x,x_0)
        Ek, Ep = countEkEp(x, b)
        E_1 = countE(Ep, Ek, b)
        condition = metroCheck(E_1,E_0,E_max)
        if condition:
            x_0 = copy.deepcopy(x)
            E_0 = E_1
        else:
            Ek, Ep = countEkEp(x_0, b)
        es_k_i = countEsK(Ek, b)
        es_p_i = countEsP(Ep)
        es_k += es_k_i
        es_p += es_p_i
        x = copy.deepcopy(x_0)
        if debug:
            g.write('i= {0} x= {1} \n x0= {2}{3}\n'.format(i,x,x_0, condition))
            f.write('{0} {1} {2} {3}\n'.format(i,E_0,es_k_i + es_p_i,condition))

E_mean += (es_k + es_p) / N_MC  
E_theor = calcETheor(D, b)

#output************************************************************************
Exit(human, E_mean, E_theor, b, Type='Metro')
