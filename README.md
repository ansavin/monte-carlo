# Introduction

Welcome to Monte-Carlo sample program set. It is created for studying the Monte-Carlo simulations method at all and some Monte-Carlo algoritms like Metropolis algoritm and Wang-Landau algoritm. It contains a set of simple program, which allows to simulate simple physical systems (3D Izing model of ferromagnetic) or calculate Feinman integral via MC method.This set also contains some bash-scripts for doing usefull thing like plotting graph, launching program parallel wia GNU Parallel, etc.

# What is Monte-Carlo method?

MC is famous method for modellng some physical system, doing calculations, etc. It contains many algorithms unified by idea of using random numbers for calculations.
The best idea to understand how it works is try it imagine (or even implement) next situation: how to calculate value of PI const on your computer using MC method? Lets generate randomly distributed dots  is small sqare region and count their amount. Also we will calculate, how many points lies inside inscribed circle in this sqare. Lets suppose thal edge of square is 1.Scince the area of a circle is PI * D^2 / 4, where D is a circle diameter, which is equal to sqare's edge, if we multiply last summ by 4 and divide on first summ, we will get the PI const. The more dots we throw, the more accurate result we have.
There are many different MC algorithms, two of them - Metropolis and Wang-Landay algo - are implemented in this programs. To learn them, you can watch the source code in 'MCfunctions\.py' and 'WL\.py' files, or read some usefull books.

# Common Usage

All programs were written using Python3, which means that you don't need to compile them - just launch any script using command like

```
./vertex.py
```
Befor doing this, make sure the file is executable. If not, just type

```
chmod +x vertex.py
```

You will get something like this:

```
**********************
* modelling quantum  *
* oscillator         *
**********************
N_MC =  100000 b =  0.5 n =  10
E_mean =  5.612589112568605
E_theor =  6.124482247610395

```

All programs launched as was mention above will do calculation using default parameters. To change some parameters, you need to add them into run command. For example, typing

```
./vertex.py 1
```

will make program to calculate energy of quantum oscillator by vertex method (for clear understanding read this README till end) for dimensionless temperature b = 1 and make more suitable for parsing output:

```
0.5   3.8623474347413063   6.124482247610395
```

Every program do small simulation and has its own simple I/O sytem:

## Vertex method

This program allow you to simulate quantum oscillator - one of the easiest quantum system - and calculate its energy. For doing this, it will calculate Feinman integral for energy by dividing it into a series of ordinal Riemann integral and calculate them using Metropolis Monte-Carlo algorithm. Program allows you to calculate energy for different values of dimensionless temperature b.

To launch simulation with built-in parameters, type

```
./vertex.py
```

You will get something like this:

```
**********************
* modelling quantum  *
* oscillator         *
**********************
N_MC=  100000 b =  0.5 n =  10
E_mean =  5.612589112568605
E_theor =  6.124482247610395

```
To calculate energy of quantum oscillator by vertex method (for clear understanding read this README till end) for dimensionless temperature b = 1 and make more suitable for parsing output, type

```
./vertex.py 1
```

You will get

```
0.5   3.8623474347413063   6.124482247610395
```

To make it more human-readable, add extra parameter: 

```
./vertex.py 1 1 

```
To make it more human-readable and output some debug info in file 'debug.log', add extra parameter: 

```
./vertex.py 1 1 1
```
So, common sommand-line interface for this program is:

```
./vertex.py <double b> <bool human-readable> <bool debug-output>

```
## Fourier method 

This program actually do the same thing as "vertex.py", but instead of dividing Feinman integral into a series of simple ones, it uses fact that you can fit function inside Feinman int by a linear one and a  Fourier series. So, the interface is actually the same:

```
./vertex.py <double b> <bool human-readable> <bool debug-output>
```

## Izing model

This is a program for simple ferromagnetic media simulating - Izing model. System is 3D crystall of particles with spin. Spin can be in 2 states: s=1 and s=-1. In low temperature system has a magnetic moment - all spins are parallel, but when temperature is hight enought, it has no magnetic moment. This program allows you to see this effect and to obtain some physical quantities. For more info, read Wiki :)

To launch simulation with built-in parameters, type

```
./Izing.py
```

Common inerface look like this
```
./vertex.py <double d> <double b> <bool human-readable> <bool debug-output>
```
where d is system size (number of particle into enge), b is dimensionless T (like in previous case)

## Volf claster method

This is a program for simple ferromagnetic media simulating - Izing model using the Volf claster method, which is a way to improve the speed of simulations.

To launch simulation with built-in parameters, type

```
./Volf.py
```
So, common sommand-line interface for this program is just like for vertex\.py

```
./vertex.py <double b> <bool human-readable> <bool debug-output>

```

# Making research

All the programs allow you to make small  research to see how MC simulations works.

## Vertex method

You can run it by youself, but we have an more interesting idea: run 

```
./QuantumOscillator.sh
```
For doing this, you will need to setup GNU Parallel utility, on Debian you can easy get it from repositories just by typing

```
sudo apt install parallel
```
Also, make sure you has Gnuplot utility. If you have no Gnuplot, type (on Debian)

```
sudo apt install gnuplot
```
If you have all this utils, running script 'QuantumOscillator.py' will give you a graph with comparision of energies of quantum oscillator for different b. As you will see, the lower b, the more theory differ from modelling, and this is normal - when b is low, there is almost no transition of system from one state to another, ehich means that you need a lot of MC steps to obtain a good result. Also, if you will re-run script, you will see that graph will changes - this means that should make more long series of experiment to make more accurate values. To do both things (making MC simulation longer and increasing number of simulstions used for averaging), you should fix the source code

## Fourier method

To study the same system using approach with Fourier series, type

```
./QuantumOscillator.sh --Fourier
```

Ypu will obtain the same graph, as in previous case, but for different values of b. You will see that theory and practise isn`t so close as before. Also you will see (by opening "QuantumOscillator.sh" file) that we have to averaging our results more times. This may happen because our target function into Feinman int has many non-zero (and non-small) members of Fourier series, and we cut it too early.

## Izing model

For this model you can do two different research:

* For studying the phase transition, we need to plot graphs for thermal conductivity C, magnetical susceptibility xi and magnetization M for different T. To do it, run
```
./PlotIz.sh
```
Using graph for C and xi, we can see that phase transition really exist in this model - just when xi differs dramatically and C has a peak.

* Also we can study, how the size of the model acts on physics inside. For doing this, type 
```
./PlotIz_P.sh
```
Do it carefully - it takes a long time. You will obtain the same graphs for system of different size. To analyse them is a challange for you :)

## Volf claster method

At first, you can run 

```
time ./Izing.py
```

...and after it...
```
time ./Volf.py
```

...to make sure Volf claster method really works faster.

After this you can make research just as for ordinally Izing model --- seeing that phase transitions really happens. For doing this, run

```
./plotVolf.py
```
All just like in ordinally Izing model --- of course, Volf method didn`t change the physics, it just make simulations faster, because it change a claster of spins per MC step while in simple Izing model we have to change one spin per MC step.
# Source code

This code is under MIT license

All programs use external library of functions for doing MC simulations - 'MCfunctions\.py'. It contains common functions like 'metroCheck(...)' for checking, should we use new system state or remain old one, 'metroFlip' for obtaining new system state, etc. Another .py files contains implementation of some simulations of simple physical system (Izing model) or some calculation of physical quantites (Energy of quantum oscillator) using different approaches. All .sh files contains bash scripts for starting some experiments and plotting graphs using Gnuplot scripts (.gp files)

## Reading and useful links

* Understanding Molecular Simulation: From Algorithms to Applications, Book by Berend Smit and Daan Frenkel --- useful book for studying Monte-Carlo method

* O. Tange (2011): GNU Parallel - The Command-Line Power Tool, ;login: The USENIX Magazine, February 2011:42-47 --- article about GNU Parallel utility

* https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator

* https://en.wikipedia.org/wiki/Ising_model

