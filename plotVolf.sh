#!/bin/bash
rm -f volf.dat
temps=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
d=4
for i in ${temps[*]}
do
echo "doing job for b = $i"
./Volf.py $i
done
echo "plotting..."
mv volf.dat izing.dat
./PlotIz.gp
echo "done!"
