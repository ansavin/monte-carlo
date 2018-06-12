#!/usr/bin/python3
''' Program for calculating quantum
    3d oscillator mean energy using
    the Forier method
'''
#import************************************************************************
from multiprocessing import Pool, Process
import os
import math
import random as rnd
import copy
import numpy as np
import sys
from MCfunctions import *

#variables*********************************************************************
N_k = 20 # count of fourier coeffs

#redefining variables**********************************************************
n = N_k # redefining for using old func

#functions*********************************************************************

# initiaqlization function
def initFourier(x):

	for i in range(N_k):
		x_i = []
		for j in range(D):
			x_i.append(0.01)
		x.append(x_i)
	pass

# count sums for estimators
def countFourierEkEp(x):

	Ek = 0
	Ep_1 = 0
	Ep_2 = 0
	x1 = 0
	for k in range(1,len(x)):
		for i in range(len(x[k])):
			Ek += (k ** 2) * (x[k][i] ** 2)
			Ep_1 += x[k][i] ** 2
			if k % 2:
				#print(k)
				Ep_2 += x[0][i] * x[k][i] / k
	for i in range(len(x[0])):
		x1 += x[0][i] ** 2
	Ek *= (math.pi ** 2) / (2 * b) 
	Ep_2 *= 4 * b / math.pi 
	Ep_2 += (b * Ep_1 / 2) + (b * x1)
	return Ek, Ep_2

# Fourier kinetical energy estimator
def countFourierEsK(Ek):
	return D * N_k / (2 * b) -  Ek / b

# Fourier potential energy estimator
def countFourierEsP(Ep):
	return Ep / b

# calculating full energy (for Fourier method)
countFourierE = lambda Ek, Ep: Ek + Ep

def MCFourierInit(x, x_0, b):
	initFourier(x_0)
	initFourier(x)
	Ek, Ep = countFourierEkEp(x_0)
	E_0 = countFourierE(Ep, Ek)
	if debug:
		print(x,x_0,b)
		print("E_0 = ",E_0)
	return Ek, Ep, E_0

#main part*********************************************************************

b, human, debug = consoleInput()

if human:
	print('**********************')
	print('* modelling quantum  *')
	print('* oscillator using   *')
	print('* the Forier method  *')
	print('**********************')
	print('N_MC= ', N_MC, 'b = ', b, 'n = ', n)

Ek, Ep, E_0 = MCFourierInit(x, x_0, b)

for i in range(N_MC):
        metroFlip(x,x_0)
        Ek, Ep = countFourierEkEp(x)
        E_1 = countFourierE(Ep, Ek)
        condition = metroCheck(E_1,E_0,E_max)
        if debug:
            g.write('i= {0} x= {1} \n x0= {2}{3}\n'.format(i,x,x_0, condition))

        if condition:
            x_0 = copy.deepcopy(x)
            E_0 = E_1
        else:
            Ek, Ep = countFourierEkEp(x_0)
        es_k_i = countFourierEsK(Ek)
        es_p_i = countFourierEsP(Ep)
        es_k += es_k_i
        es_p += es_p_i
        if debug: 
            f.write('{0} {1} {2} {3}\n'.format(i,E_0,es_k_i + es_p_i,condition))
        x = copy.deepcopy(x_0)
        if human:
            sys.stdout.write("{0} % complete\r".format(math.floor(100 * i / N_MC)))

E_mean = (es_k + es_p) / N_MC  
E_theor = calcETheor(D, b)

#output************************************************************************
Exit(human, E_mean, E_theor, b, Type='Metro')
CloseIO()
