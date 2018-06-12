#!/bin/bash
rm -f izing.dat
times=("2.75" "3" "3.25" "3.5" "3.75" "4" "4.25" "4.5" "4.75" "5")
d=4
for i in ${times[*]}
do
echo "doing job for b = $i"
./Izing.py $d $i 
done
mv "izing$d.dat" "izing.dat"
echo "plotting..."
./PlotIz.gp
echo "done!"
