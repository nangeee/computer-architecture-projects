#!/usr/bin/env python3
import sys
import encoding_formats as ef


num_of_bytes = 0
bin_format = list()
hex_format = list()
with open(sys.argv[1], "rb") as inputFile:
    data = inputFile.read()
    for k in data:
        bin_format.append("{0:0>8}".format(format(k, "b")))
        hex_format.append("{0:0>2}".format(format(k, "x")))
        num_of_bytes += 1
        
num_of_inst = int(num_of_bytes / 4)
bin_little_endian = list()
hex_little_endian = list()
for i in range(num_of_inst):
    for j in range((i + 1) * 4 - 1, i * 4 - 1, -1):
        bin_little_endian.append(bin_format[j])
        hex_little_endian.append(hex_format[j])


index = 0
bin_code = list()
hex_code = list()
for i in range(num_of_inst):
    byte = 0
    bin_inst = ""
    hex_inst = ""
    while byte < 4:
        bin_inst += bin_little_endian[index]
        hex_inst += hex_little_endian[index]
        index += 1
        byte += 1
    bin_code.append(bin_inst)
    hex_code.append(hex_inst)



def get_format(opcode):
    if opcode == "0110011":
        return "R"
    if opcode == "0010011" or opcode == "0000011" or opcode == "1100111":
        return "I"
    if opcode == "0100011":
        return "S"
    if opcode == "1100011":
        return "B"
    if opcode == "1101111":
        return "J"
    if opcode == "0110111" or opcode == "0010111":
        return "U"
    return 0


index = 0
for bin_str in bin_code:
    found_flag = 0
    encoding_format = get_format(bin_str[-7:])
    if encoding_format == "R":
        r_inst = ef.R_format(bin_str)
        rd, rs1, rs2 = r_inst.get_regis()
        print("inst {}: {} {} {}, {}, {}".format(index, hex_code[index], r_inst.get_inst_name(),
            rd, rs1, rs2))
        found_flag = 1
    elif encoding_format == "I":
        i_inst = ef.I_format(bin_str)
        rd, rs1, imm = i_inst.get_regis()
        if bin_str[-7:] == "0010011":
            print("inst {}: {} {} {}, {}, {}".format(index, hex_code[index], i_inst.get_inst_name(),
                rd, rs1, imm))
        else:
            print("inst {}: {} {} {}, {}({})".format(index, hex_code[index], i_inst.get_inst_name(),
                rd, imm, rs1))
        found_flag = 1
    elif encoding_format == "S":
        s_inst = ef.S_format(bin_str)
        rs2, imm, rs1 = s_inst.get_regis()
        print("inst {}: {} {} {}, {}({})".format(index, hex_code[index], s_inst.get_inst_name(),
            rs2, imm, rs1))
        found_flag = 1
    elif encoding_format == "B":
        b_inst = ef.B_format(bin_str)
        rs1, rs2, imm = b_inst.get_regis()
        print("inst {}: {} {} {}, {}, {}".format(index, hex_code[index], b_inst.get_inst_name(),
            rs1, rs2, imm))
        found_flag = 1
    elif encoding_format == "U":
        u_inst = ef.U_format(bin_str)
        rd, imm = u_inst.get_regis()
        print("inst {}: {} {} {}, {}".format(index, hex_code[index], u_inst.get_inst_name(),
            rd, imm))
        found_flag = 1
    elif encoding_format == "J":
        j_inst = ef.J_format(bin_str)
        rd, imm = j_inst.get_regis()
        print("inst {}: {} {} {}, {}".format(index, hex_code[index], j_inst.get_inst_name(),
            rd, imm))
        found_flag = 1

    if found_flag == 0:
        print("inst {}: {} unknown instruction".format(index, hex_code[index]))
    
    index += 1
        
