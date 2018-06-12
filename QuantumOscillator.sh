#!/bin/bash
echo $1
if [ "$1" = "--Fourier" ]
then
    time='1 2 5 7.5 10 15'
    aver=6
    script=./Fourier.py
    method='Fourier'
else
    time='0.25 0.5 1 1.5 2 5'
    aver=4
    script=./vertex.py
    method='vertex'
fi
rm -f dots.dat
echo "plotting using $method method"
for i in $time
do
    comm=''
	for ((j=0; j < aver; j++))
	do
        comm=$comm" "$i
	done
	parallel $script ::: $comm > output.txt
	./vertex_format.py
done
./PlotQO.gp
