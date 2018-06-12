#!/usr/bin/gnuplot
set terminal png
set output 'picFinal.png'
set xlabel 'b'
set ylabel 'E_{mean}'
plot 'dots.dat' u 1:2 w l title 'experiment','dots.dat' u 1:3 w l title 'theory'
exit
