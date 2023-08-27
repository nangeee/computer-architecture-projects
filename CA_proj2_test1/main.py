#!/usr/bin/env python3
import sys
#import riscv_ver2 as riscv
import execution as exc


num_of_bytes = 0
bin_format = list()
hex_format = list()
file_name = sys.argv[1]
inst_exc_num = int(sys.argv[2])
with open(file_name, "rb") as inputFile:
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


def twos_comp_bin(n, bits):
    s = bin(n & int("1" * bits, 2))[2:]
    return ("{0:0>%s}"%(bits)).format(s)


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



regis = list() # register values
for i in range(32):
    regis.append(0) 
   # regis.append("0x{0:0>8}".format(format(0, "x"))

#exc.get_regis(inst_exc_list) # execute instructions



executed = 0
for bin_str in bin_code:
    encoding_format = get_format(bin_str[-7:])
    if encoding_format == "R":
        r_inst = exc.R_format(bin_str)
        regis = r_inst.exc_inst(regis)
        #rd, rs1, rs2 = r_inst.get_regis()
        #inst = "{} {}, {}, {}".format(r_inst.get_inst_name(), rd, rs1, rs2)
    
    elif encoding_format == "I":
        i_inst = exc.I_format(bin_str)
        #rd, rs1, imm = i_inst.get_regis()
        regis = i_inst.exc_inst(regis) # *********************
        #inst = "{} {}, {}, {}".format(i_inst.get_inst_name(), rd, rs1, imm)

    elif encoding_format == "U":
        u_inst = exc.U_format(bin_str)
        regis = u_inst.exc_inst(regis)
        #rd, imm = u_inst.get_regis()
        #inst = "{} {}, {}".format(u_inst.get_inst_name(), rd, imm)
        
    '''
    elif encoding_format == "S":
        s_inst = riscv.S_format(bin_str)
        rs2, imm, rs1 = s_inst.get_regis()
        inst = "{} {}, {}({})".format(s_inst.get_inst_name(), rs2, imm, rs1)
        found_flag = 1
    
    elif encoding_format == "B":
        b_inst = riscv.B_format(bin_str)
        rs1, rs2, imm = b_inst.get_regis()
        inst = "{} {}, {}, {}".format(b_inst.get_inst_name(), rs1, rs2, imm)
        found_flag = 1

    elif encoding_format == "J":
        j_inst = riscv.J_format(bin_str)
        rd, imm = j_inst.get_regis()
        inst = "{} {}, {}".format(j_inst.get_inst_name(), rd, imm)
        found_flag = 1
    '''

    executed += 1

    if executed == inst_exc_num:
        break

if executed < inst_exc_num:
    print("No more instructions")

for i in range(32):
    value_bin = twos_comp_bin(regis[i], 32)
    value_hex = ""
    for j in range(8):
        n = value_bin[4 * j:4 * j + 4]
        n = int(n[0]) * 8 + int(n[1]) * 4 + int(n[2]) * 2 + int(n[3])
        n = format(n, "x")
        value_hex += n
    print("x{}: 0x{}". format(i, value_hex))
    #print("x{}: {}".format(i, regis[i]))
    #print("x{}: 0x{}".format(i, "{0:0>8}".format(format(regis[i], "x"))))






