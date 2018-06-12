#!/usr/bin/python3
''' Function library for MC programs 
    (implements Metropolis algorithm)
'''
#import************************************************************************
import math
import random as rnd
import copy
from multiprocessing import Pool 
import sys

#constants*********************************************************************
dx = 1.5                  # const for shifting momenta
b = 0.5                   # dimensionless initial temperature
D = 3                     # dimension of the program
N_MC = 200000             # MC steps
E_max = 50                # maximal possible E
n = 10                    # number of point in Feinman integral

#variables*********************************************************************
debug = 0
human = 1
x_0 = []                  # old coordinates
x = []                    # current coordinates
E_0 = 0                   # old energy
E_1 = 0                   # current energy
es_k = 0                  # estimator of kinetic energy
es_p = 0                  # estimator of potential energy
E_mean = 0                # mean kinetic energy
f = open('debug.log','w')
g = open('tragectory_deb.log', 'w')

#functions*********************************************************************

# input data (for Volf, Vertex and Fourier method)
def consoleInput():
    b = 0.5
    human = 1
    debug = 0
    if len(sys.argv) == 2:
        b = float(sys.argv[1])
        human = 0
    elif len(sys.argv) == 3:
        b = float(sys.argv[1])
        human = int(sys.argv[2])
    elif len(sys.argv) > 3:
        b = float(sys.argv[1])
        human = int(sys.argv[2]) 
        debug = int(sys.argv[3])
    return b, human, debug

# check if we should approve configuration
def metroCheck(E_1,E_0,E_max):

    if E_1 > E_max:
        return False
    else: 
        dE = E_1 - E_0 
        if dE <= 0:
            return True    
        else: 
            w = math.exp(-1 * dE)
            xi = rnd.uniform(0,1)
            if xi <= w:
                return True
            else:
                return False

# making new configuration
def metroFlip(x, x_0):

    k = rnd.randint(0,len(x) - 1)
    for i in range(len(x[k])):
        xi = rnd.uniform(0,1)
        x[k][i] = x_0[k][i] + (xi - 0.5) * dx
    pass

# count potential and kinetical energy
def countEkEp(x, b):

    Ek = 0
    Ep = 0
    for i in range(len(x)):
        for j in range(len(x[i])):
            Ep += x[i][j] ** 2
            if i < n - 1: 
                Ek += (x[i][j] - x[i+1][j]) ** 2
            else:
                Ek += (x[i][j] - x[0][j]) ** 2
    return Ek, Ep

# potential energy estimator
countEsP = lambda Ep: Ep / n


# kinetical energy estimator
countEsK = lambda Ek, b: (D * n / (2 * b))  -  Ek * n / (b ** 2)

# initalization of model function
def init(x):

    for i in range(n):
        x_i = []
        for j in range(D):
            x_i.append(0)
        x.append(x_i)
    pass

# calculating full energy
countE = lambda Ep, Ek, b: (n/b) * Ek + (b/n) * Ep

# calculating theoretical value of energy of quantum oscillator
def calcETheor(D, b_curr):
    E_theor = ( D / 2 ) * math.cosh( b_curr / 2 ) / math.sinh( b_curr / 2 )
    return E_theor
    
# initialization of system function
def MC_init(x, x_0, b):
    init(x_0)
    init(x)
    Ek, Ep = countEkEp(x_0, b)
    E_0 = countE(Ep, Ek, b)
    if debug:
        print(x,x_0,b)
        print("E_0 = ",E_0)
    return Ek, Ep, E_0

# console output function
def Exit(human, E_mean, E_theor, b, Type='Metro'):

    if Type == 'Metro':
        if human:
            print("E_mean = ", E_mean)
            print("E_theor = ", E_theor)
        else:
            print(b,' ',E_mean, ' ', E_theor)
    pass
    
def CloseIO():
    f.close()    
    g.close()
    pass

#functions for Izing model simulations*****************************************

# getting next index in a lattice with periodic boundary conditions    
def nextInd(i,di):
    if i == di - 1:
        i1 = 0
    else:
        i1 = i + 1
    return i1

# getting previous index in a lattice with periodic boundary conditions
def prevInd(i,di):
    if i == 0:
        i1 = di - 1
    else:
        i1 = i - 1
    return i1

# random spin generating
def ran():
    xi = rnd.uniform(0,1) - 0.5
    if xi > 0:
        return 1
    else:
        return -1

def initIZ(x, d1, d2, d3):
    for i in range(d1):
        xi = []
        for j in range(d2):
            xij = []
            for k in range(d3):
                xij.append(ran())
            xi.append(xij)
        x.append(xi)
    pass

# subroutine for calculating energy)
def countEijk(s,i,j,k,d1,d2,d3,H,J,isSingle=1):
    Eijk = 0
    if isSingle:
        
        Eijk =  -1 * J * (s[i][j][k] * s[i][j][nextInd(k,d3)] + 
        s[i][j][k] * s[i][nextInd(j,d2)][k] + 
        s[i][j][k] * s[nextInd(i,d1)][j][k])
    else: 
        Eijk =  -1 * J * (s[i][j][k] * s[i][j][nextInd(k,d3)] + 
        s[i][j][k] * s[i][nextInd(j,d2)][k] + 
        s[i][j][k] * s[nextInd(i,d1)][j][k] +
        s[i][j][prevInd(k,d3)] * s[i][j][k] + 
        s[i][prevInd(j,d2)][k] * s[i][j][k] + 
        s[prevInd(i,d1)][j][k] * s[i][j][k])

    Eijk += -1 * H * s[i][j][k] ** 2
    return Eijk

# calculating energy
def countEIZ(s,d1,d2,d3,H,J):
    E = 0
    for i in range(len(s)):
        for j in range(len(s[i])):
            for k in range(len(s[i][j])):
                E += countEijk(s,i,j,k,d1,d2,d3,H,J)
    return E

# changing our system (Izing model)
def metroFlipIZ(s, d1, d2, d3):
    xi_i = rnd.randint(0,d1 - 1)
    xi_j = rnd.randint(0,d2 - 1)
    xi_k = rnd.randint(0,d3 - 1)
    s[xi_i][xi_j][xi_k] *= -1 
    pass

calcFluct = lambda x, x2: x2 - (x ** 2)

# calculating magnetization
def meanM(s):
    S = 0
    if 1: 
        for i in range(len(s)):
            for j in range(len(s[i])):
                for k in range(len(s[i][j])):
                    S += s[i][j][k] 
    S2 = S ** 2
    S = math.fabs(S)
    return S, S2
