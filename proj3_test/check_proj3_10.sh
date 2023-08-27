#!/bin/bash
for var in `seq 0 13`
do
	com1=$(./riscv-sim ~swe3005/2022f/proj3/proj3_10_inst.bin $(($var+1)))
	com2=$(~swe3005/2022f/proj3/riscv-sim ~swe3005/2022f/proj3/proj3_10_inst.bin $(($var+1)))
	echo $com1 >text1_$var.txt
	echo $com2 >result1_$var.txt
	com3=$(diff -q text1_$var.txt result1_$var.txt)
	echo $com3
done
