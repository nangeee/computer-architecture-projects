#!/bin/bash
for var in `seq 0 9`
do
	com1=$(./riscv-sim ~swe3005/2022f/proj2/proj2_3.bin $(($var+1)))
	com2=$(~swe3005/2022f/proj2/riscv-sim ~swe3005/2022f/proj2/proj2_3.bin $(($var+1)))
	echo $com1 >text3_$var.txt
	echo $com2 >result3_$var.txt
	com3=$(diff -q text3_$var.txt result3_$var.txt)
	echo $com3
done
