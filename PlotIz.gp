#!/usr/bin/gnuplot
set terminal png
set output 'E.png'
set xlabel 'b'
set ylabel 'E'
plot 'izing.dat' u 1:2 w l title 'energy'
set output 'C.png'
set xlabel 'b'
set ylabel 'C'
plot 'izing.dat' u 1:3 w l title 'termal condactivity'
set output 'M.png'
set xlabel 'b'
set ylabel 'M'
plot 'izing.dat' u 1:4 w l title 'magnetivity'
set output 'xi.png'
set xlabel 'b'
set ylabel 'xi'
plot 'izing.dat' u 1:5 w l title 'xi'
exit
