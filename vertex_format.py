#!/usr/bin/python3

''' Sub-script for averaging values
    and I/O for automatical plotting
'''
f = open('output.txt','r')
g = open('dots.dat','a')

E_mean = 0
counter = 0
for line in f:
    b = float(line.split()[0])
    E = float(line.split()[1])
    E_theor = float(line.split()[2])
    E_mean += E
    counter += 1
E_mean /= counter
g.write('{0} {1} {2}\n'.format(b,E_mean,E_theor))
f.close()
g.close()
