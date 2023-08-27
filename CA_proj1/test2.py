#!/usr/bin/env python3
import sys

original_hex = list()
num_of_bytes = 0
with open(sys.argv[1], "rb") as inputFile:
    data = inputFile.read()
    for k in data:
        #print("k =", k, ", binary =", format(k, "b"), type(format(k, "b")))
        print("k =", k, ", binary =", "{0:0>8}".format(format(k, "b")))
        # print(type(k)) # int
        num_of_bytes += 1
        if len(str(hex(k))[2:]) == 1:
            original_hex.append(str(0) + str(hex(k))[2:])
            continue
        original_hex.append(str(hex(k))[2:])

print(original_hex)
print("num of bytes: ", num_of_bytes)

def getHexFormat(original_hex, num_of_bytes):
    hex_le = list() # Little Endian
    for i in range(int(num_of_bytes / 4)): # num of bytes / 4 == num of instructions
        to_le = "" # to Little Endian
        for j in range(3, -1, -1):
            to_le += original_hex[j]
            del original_hex[j]
        hex_le.append(to_le)
    return hex_le
    

hex_format = getHexFormat(original_hex, num_of_bytes)
print(hex_format)

binary_format = list()
for data in hex_format:
    #bin_str = ""
    for i in data:
        print(format(i, "b"))
       # bin_str += bin(int(i, base=16))[2:]
    print("\n")
   # binary_format.append(bin_str)

