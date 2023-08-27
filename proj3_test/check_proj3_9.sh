#!/bin/bash
for var in `seq 0 30`
do
	com1=$(./riscv-sim ~swe3005/2022f/proj3/proj3_9_inst.bin ~swe3005/2022f/proj3/proj3_9_data.bin $(($var+1)))
	com2=$(~swe3005/2022f/proj3/riscv-sim ~swe3005/2022f/proj3/proj3_9_inst.bin ~swe3005/2022f/proj3/proj3_9_data.bin $(($var+1)))
	echo $com1 >text5_$var.txt
	echo $com2 >result5_$var.txt
	com3=$(diff -q text5_$var.txt result5_$var.txt)
	echo $com3
done
