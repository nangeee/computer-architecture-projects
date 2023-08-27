#!/usr/bin/env python3

def twos_comp_imm(imm_bin, length):
    imm_int = int(imm_bin, 2)
    if (imm_int & (1 << (length - 1))): # negative
        imm_int = imm_int - (1 << length)
    return imm_int



class J_format:
    def __init__(self, bin_str):
        self.opcode = bin_str[-7:]
        self.rd_bin = bin_str[-12:-7]
        self.imm_bin = bin_str[0] + bin_str[12:20] + bin_str[11] + bin_str[1:11] + "0"

    def get_inst_name(self):
        return "jal"

    def get_regis(self):
        rd, imm = 0, 0

        for i in range(5):
            rd += int(self.rd_bin[4 - i]) * (2 ** i)

        #imm = twos_comp_imm(self.imm_bin, len(self.imm_bin))
        imm_decimal = int(self.imm_bin, 2)
        imm = hex(imm_decimal)


        return "x" + str(rd), imm



class U_format:
    def __init__(self, bin_str):
        self.opcode = bin_str[-7:]
        self.rd_bin = bin_str[-12:-7]
        self.imm_bin = bin_str[:-12]

    def get_inst_name(self):
        if self.opcode == "0110111":
            return "lui"
        if self.opcode == "0010111":
            return "auipc"

    def get_regis(self):
        rd, imm = 0, 0

        for i in range(5):
            rd += int(self.rd_bin[4 - i]) * (2 ** i)

        #imm = twos_comp_imm(self.imm_bin + "000000000000", len(self.imm_bin) + 12)
        imm_decimal = int(self.imm_bin, 2)
        imm = hex(imm_decimal)

        return "x" + str(rd), imm


class B_format:
    def __init__(self, bin_str):
        self.opcode = bin_str[-7:]
        self.funct3 = bin_str[17:20]
        self.rs1_bin = bin_str[12:17]
        self.rs2_bin = bin_str[7:12]
        self.imm_bin = bin_str[0] + bin_str[-8] + bin_str[1:7] + bin_str[20:-8] + "0"

    def get_inst_name(self):
        if self.funct3 == "000":
            return "beq"
        if self.funct3 == "001":
            return "bne"
        if self.funct3 == "100":
            return "blt"
        if self.funct3 == "101":
            return "bge"
        if self.funct3 == "110":
            return "bltu"
        if self.funct3 == "111":
            return "bgeu"

    def get_regis(self):
        rs1, rs2, imm = 0, 0, 0
        
        for i in range(5):
            rs1 += int(self.rs1_bin[4 - i]) * (2 ** i)
            rs2 += int(self.rs2_bin[4 - i]) * (2 ** i)
        
        #imm = twos_comp_imm(self.imm_bin, len(self.imm_bin))
        imm_decimal = int(self.imm_bin, 2)
        imm = hex(imm_decimal)


        return "x" + str(rs1), "x" + str(rs2), imm




class I_format:
    def __init__(self, bin_str):
        self.opcode = bin_str[-7:]
        self.funct3 = bin_str[17:20]
        self.rd_bin = bin_str[-12:-7]
        self.rs1_bin = bin_str[12:17]
        self.imm_bin = bin_str[:12]

    def get_inst_name(self):
        if self.opcode == "0010011":
             # use 12 bits for imm
            if self.funct3 == "000":
                return "addi"
            if self.funct3 == "100":
                return "xori"
            if self.funct3 == "110":
                return "ori"
            if self.funct3 == "111":
                return "andi"
            if self.funct3 == "010":
                return "slti"
            if self.funct3 == "011":
                return "sltiu"
            if self.funct3 == "001":
                self.type_num = 2  # use 5 bits for shamt -> shamt should be a positive value
                return "slli"
            if self.funct3 == "101":
                self.type_num = 2 # use 5 bits for shamt
                if self.imm_bin[:7] == "0000000":
                    return "srli"
                else:
                    return "srai"
        if self.opcode == "0000011":
            self.type_num = 3 # offset format (load, jalr)
            if self.funct3 == "000":
                return "lb"
            if self.funct3 == "001":
                return "lh"
            if self.funct3 == "010":
                return "lw"
            if self.funct3 == "100":
                return "lbu"
            if self.funct3 == "101":
                return "lhu"

        return "jalr"  # offset format

    def get_regis(self):
        rd, rs1, imm = 0, 0, 0
        for i in range(5):
            rd += int(self.rd_bin[4 - i]) * (2 ** i)
            rs1 += int(self.rs1_bin[4 - i]) * (2 ** i)
        
        if self.funct3 == "001" or self.funct3 == "101": # use 5 bits for shamt -> should be a positive value
            for i in range(5):
                imm += int(self.imm_bin[11 - i]) * (2 ** i)
        else:
            # imm = twos_comp_imm(self.imm_bin, len(self.imm_bin))
            imm_decimal = int(self.imm_bin, 2)
            imm = hex(imm_decimal)


        return "x" + str(rd), "x" + str(rs1), imm


class S_format:
    def __init__(self, bin_str):
        self.funct3 = bin_str[17:20]
        self.rs1_bin = bin_str[12:17]
        self.rs2_bin = bin_str[7:12]
        self.imm_bin = bin_str[:7] + bin_str[-12:-7]

    def get_inst_name(self):
        if self.funct3 == "000":
            return "sb"
        if self.funct3 == "001":
            return "sh"
        if self.funct3 == "010":
            return "sw"

    def get_regis(self):
        rs1, rs2 = 0, 0

        for i in range(5):
            rs1 += int(self.rs1_bin[4 - i]) * (2 ** i)
            rs2 += int(self.rs2_bin[4 - i]) * (2 ** i)

        # imm = twos_comp_imm(self.imm_bin, len(self.imm_bin))
        imm_decimal = int(self.imm_bin, 2)
        imm = hex(imm_decimal)


        return "x" + str(rs2), imm, "x" + str(rs1)



class R_format:
    def __init__(self, bin_str):
        self.funct3 = bin_str[17:20]
        self.funct7 = bin_str[:7]
        self.rd_bin = bin_str[-12:-7]
        self.rs1_bin = bin_str[12:17]
        self.rs2_bin = bin_str[7:12]

    def get_inst_name(self):
        if self.funct3 == "000":
            if self.funct7 == "0000000":
                return "add"
            else:
                return "sub"
        if self.funct3 == "101":
            if self.funct7 == "0000000":
                return "srl"
            else:
                return "sra"
        if self.funct3 == "100":
            return "xor"
        if self.funct3 == "110":
            return "or"
        if self.funct3 == "111":
            return "and"
        if self.funct3 == "001":
            return "sll"
        if self.funct3 == "010":
            return "slt"
        if self.funct3 == "011":
            return "sltu"
        return 0


    def get_regis(self):
        rd, rs1, rs2 = 0, 0, 0

        for i in range(5):
            rd += int(self.rd_bin[4 - i]) * (2 ** i)
            rs1 += int(self.rs1_bin[4 - i]) * (2 ** i)
            rs2 += int(self.rs2_bin[4 - i]) * (2 ** i)

        return "x" + str(rd), "x" + str(rs1), "x" + str(rs2)

