#!/bin/bash
rm -f izing.dat
Ls='4 8 16 32'
for i in $Ls
do
    rm -f "izing$i.dat" 
    rm -f "C$i.png"
    rm -f "E$i.png"
    rm -f "M$i.png"
    rm -f "xi$i.png"
done
parallel ./Izing.py ::: $Ls
echo "plotting..."
for i in $Ls
do
    mv "izing$i.dat" "izing.dat"
    ./PlotIz.gp
    mv "C.png" "C$i.png"
    mv "E.png" "E$i.png"
    mv "M.png" "M$i.png"
    mv "xi.png" "xi$i.png"
done
echo "done!"
