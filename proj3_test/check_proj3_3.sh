#!/bin/bash
for var in `seq 0 12`
do
	com1=$(./riscv-sim ~swe3005/2022f/proj3/proj3_3_inst.bin ~swe3005/2022f/proj3/proj3_3_data.bin $(($var+1)))
	com2=$(~swe3005/2022f/proj3/riscv-sim ~swe3005/2022f/proj3/proj3_3_inst.bin ~swe3005/2022f/proj3/proj3_3_data.bin $(($var+1)))
	echo $com1 >text1_$var.txt
	echo $com2 >result1_$var.txt
	com3=$(diff -q text1_$var.txt result1_$var.txt)
	echo $com3
done
