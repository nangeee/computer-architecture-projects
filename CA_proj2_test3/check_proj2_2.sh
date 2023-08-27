#!/bin/bash
for var in `seq 0 7`
do
	com1=$(./riscv-sim ~swe3005/2022f/proj2/proj2_2.bin $(($var+1)))
	com2=$(~swe3005/2022f/proj2/riscv-sim ~swe3005/2022f/proj2/proj2_2.bin $(($var+1)))
	echo $com1 >text2_$var.txt
	echo $com2 >result2_$var.txt
	com3=$(diff -q text2_$var.txt result2_$var.txt)
	echo $com3
done
