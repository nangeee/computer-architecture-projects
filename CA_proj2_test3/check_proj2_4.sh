#!/bin/bash
for var in `seq 0 7`
do
	com1=$(./riscv-sim ~swe3005/2022f/proj2/proj2_4.bin $(($var+1)))
	com2=$(~swe3005/2022f/proj2/riscv-sim ~swe3005/2022f/proj2/proj2_4.bin $(($var+1)))
	echo $com1 >text4_$var.txt
	echo $com2 >result4_$var.txt
	com3=$(diff -q text4_$var.txt result4_$var.txt)
	echo $com3
done