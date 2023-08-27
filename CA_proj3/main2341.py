#!/usr/bin/env python3
import sys
import execution as exc


num_of_bytes = 0
num_of_data = 0
bin_format = list()
hex_format = list()
data_memory = dict() # decimal data 

if len(sys.argv) == 3:
    inst_file = sys.argv[1]
    inst_exc_num = int(sys.argv[2])
elif len(sys.argv) == 4:
    inst_file = sys.argv[1]
    data_file = sys.argv[2]
    inst_exc_num = int(sys.argv[3])
    with open(data_file, "rb") as dataInputFile:
        data = dataInputFile.read()
        for k in data:
            data_memory[num_of_data + 268435456] = k # 0x10000000 = 268435456
            num_of_data += 1

# range of data memory
# 0x10000000 ~ 0x1000ffff -> 268435456 ~ 268500991
data_memory[num_of_data + 268435456] = -1

with open(inst_file, "rb") as instInputFile:
    data = instInputFile.read()
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

inst_memory = dict()
#for i in range(num_of_inst + 1): # initialize as 0xFF
for i in range(num_of_inst):
    inst_memory[i] = -1


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
    inst_memory[i] = bin_inst # load instruction binary to inst memory 


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

'''
regis = list() # register values
for i in range(32):
    regis.append(0) 
'''

first_regis = list()
for i in range(32):
    first_regis.append(0)

executed = 0
pc = 0
tail_branch = 0
printed = 0

################ sample 5

def run(base_regis):
    regis = list()
    for i in range(32):
        regis.append(base_regis[i])
    global pc
    global data_memory
    global executed
    global tail_branch
    global printed

    while executed < inst_exc_num:  
    #while pc in inst_memory.keys():

        print("*** pc:", pc)
        if pc not in inst_memory.keys():
            print("unknown instruction11")
            printed = 1
            executed += 1 ############
            pc += 1 ###########
            return regis

        executed += 1
        print("executed:", executed, "pc:", pc)
 
        if executed > inst_exc_num:
            print("unknown instruction22")
            pc += 1
            return regis 
        
        if pc < 0 or pc > 16383: # 0x0000FFFC = 65332(16383 * 4)
            print("Memory address error")
            return regis
        
        '''
        if pc == num_of_inst:
            return regis
        
        
        if pc not in inst_memory.keys():
            print("unknown instruction222")
            return regis
        '''

        bin_str = inst_memory[pc]
        encoding_format = get_format(bin_str[-7:])

        if encoding_format == "R":
            r_inst = exc.R_format(bin_str)
            regis = r_inst.exc_inst(regis)
            pc += 1
        elif encoding_format == "I":
            i_inst = exc.I_format(bin_str)
            if bin_str[-7:] == "1100111": # jalr
                rd, rs1, imm = i_inst.get_regis()
                if rd != 0:
                    regis[rd] = (pc + 1) * 4 # return address
                ra = pc + 1
                #pc = regis[rs1] + int(imm / 4)
                pc = int((regis[rs1] + imm) / 4)
                
                if executed < inst_exc_num:
                    if pc > 0 and pc < 16383 and pc in inst_memory.keys():
                        tail_branch += 1
                        regis = run(regis) # here regis[rd] should take the original value of rd, not pc + 1
                        tail_branch -= 1
                        if tail_branch != 0 and executed < inst_exc_num:
                            pc = ra
                            if rd != 0:
                                regis[rd] = pc * 4
                            elif rd == 0:
                                regis[rd] = 0
            else :
                regis = i_inst.exc_inst(regis, data_memory)
                pc += 1
        elif encoding_format == "U":
            u_inst = exc.U_format(bin_str)
            #regis, move = u_inst.exc_inst(regis)
            regis = u_inst.exc_inst(regis, pc)
            pc += 1
            #move = int(move / 4)
            #if move == 1: # lui
             #   pc += move
            #if move != 1: # auipc
             #   pc += 1

        elif encoding_format == "B":
            b_inst = exc.B_format(bin_str)
            regis, move = b_inst.exc_inst(regis)
            move = int(move / 4)
            pc += move
        elif encoding_format == "S":
            s_inst = exc.S_format(bin_str)
            data_memory = s_inst.exc_inst(regis, data_memory)
            pc += 1
        elif encoding_format == "J":
            j_inst = exc.J_format(bin_str)
            rd, imm = j_inst.get_regis()
            if rd != 0:
                regis[rd] = (pc + 1) * 4 # return address 
            ra = pc + 1
            pc = pc + int((imm / 4))
            #pc = int((pc + imm) / 4)
            
            if executed < inst_exc_num:    
                if pc > 0 and pc < 16383 and pc in inst_memory.keys():
                    tail_branch += 1
                    regis = run(regis)
                    tail_branch -= 1
                    if tail_branch != 0 and executed < inst_exc_num: # if this is not a tail function 
                        pc = ra
                        if rd != 0:
                            regis[rd] = pc * 4
                            #print("x{} = {}".format(rd, pc * 4))
                        elif rd == 0:
                            regis[rd] = 0
                    #elif tail_branch == 0:   # if this is a tail function
                        #print("tail pc:", pc)


    return regis

regis = run(first_regis)

#pc += 1

#print("executed:", executed, "inst_exc_num:", inst_exc_num)
if executed < inst_exc_num and printed != 1:
    pc += 1
    print("unknown instruction: out")

#while executed < inst_exc_num:
    #pc += 1
    #executed += 1


for i in range(32):
    value_bin = twos_comp_bin(regis[i], 32)
    value_hex = ""
    for j in range(8):
        n = value_bin[4 * j:4 * j + 4]
        n = int(n[0]) * 8 + int(n[1]) * 4 + int(n[2]) * 2 + int(n[3])
        n = format(n, "x")
        value_hex += n
    print("x{}: 0x{}". format(i, value_hex))

#print("********* final pc:", pc)

pc = pc * 4
pc_bin = twos_comp_bin(pc, 32)
pc_hex = ""
for i in range(8):
    m = pc_bin[4 * i:4 * i + 4]
    m = int(m[0]) * 8 + int(m[1]) * 4 + int(m[2]) * 2 +int(m[3])
    m = format(m, "x")
    pc_hex += m
print("PC: 0x{}".format(pc_hex))


