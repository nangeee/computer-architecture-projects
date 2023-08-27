#!/usr/bin/env python3

def twos_comp_imm(imm_bin, length):
    imm_int = int(imm_bin, 2)
    if (imm_int & (1 << (length - 1))): # negative
        imm_int = imm_int - (1 << length)
    return imm_int


def twos_comp_bin(decimal, bits):
    s = bin(decimal & int("1" * bits, 2))[2:]
    return ("{0:0>%s}"%(bits)).format(s)



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

        imm = twos_comp_imm(self.imm_bin, len(self.imm_bin))

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

        imm = twos_comp_imm(self.imm_bin + "000000000000", len(self.imm_bin) + 12)

        return rd, imm

    def exc_inst(self, regis):
        rd, imm = self.get_regis()
        
        if self.opcode == "0110111":
            regis[rd] = imm

        return regis




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
        
        imm = twos_comp_imm(self.imm_bin, len(self.imm_bin))

        return "x" + str(rs1), "x" + str(rs2), imm




class I_format:
    def __init__(self, bin_str):
        self.opcode = bin_str[-7:]
        self.funct3 = bin_str[17:20]
        self.rd_bin = bin_str[-12:-7]
        self.rs1_bin = bin_str[12:17]
        self.imm_bin = bin_str[:12]
        
    def get_regis(self):
        rd, rs1, imm = 0, 0, 0
        for i in range(5):
            rd += int(self.rd_bin[4 - i]) * (2 ** i)
            rs1 += int(self.rs1_bin[4 - i]) * (2 ** i)
        
        if self.funct3 == "001" or self.funct3 == "101":
            for i in range(5):
                imm += int(self.imm_bin[11 - i]) * (2 ** i)
        else:
            imm = twos_comp_imm(self.imm_bin, len(self.imm_bin))
        
        return rd, rs1, imm
        #return "x" + str(rd), "x" + str(rs1), imm

    def exc_inst(self, regis):
        rd, rs1, imm = self.get_regis()
        
        if self.opcode == "0010011":
             # use 12 bits for imm
            if self.funct3 == "000": # addi
                regis[rd] = regis[rs1] + imm
            elif self.funct3 == "100": # xori
                regis[rd] = regis[rs1] ^ imm
            elif self.funct3 == "110": # ori
                regis[rd] = regis[rs1] | imm
            elif self.funct3 == "111": # andi
                regis[rd] = regis[rs1] & imm
            elif self.funct3 == "010": # slti
                if regis[rs1] < imm:
                    regis[rd] = 1
                else:
                    regis[rd] = 0
            elif self.funct3 == "011": # sltiu
                if regis[rs1] < imm:
                    regis[rd] = 1
                else:
                    regis[rd] = 0
            elif self.funct3 == "001": # slli
                # use 5 bits for shamt -> shamt should be a positive value
                regis[rd] = regis[rs1] << imm
            elif self.funct3 == "101":
                # use 5 bits for shamt
                if self.imm_bin[:7] == "0000000": # srli
                    if regis[rs1] < 0: # negative value
                        n = regis[rs1] >> imm
                        n_bin = twos_comp_bin(n, 32) # get two's comp bin string
                        n_bin = "0" * imm + n_bin[imm:]
                        n = twos_comp_imm(n_bin, len(n_bin))
                        regis[rd] = n
                    else: # positive value
                        regis[rd] = regis[rs1] >> imm
                else: # srai
                    regis[rd] = regis[rs1] >> imm
        
        return regis


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

        imm = twos_comp_imm(self.imm_bin, len(self.imm_bin))

        return "x" + str(rs2), imm, "x" + str(rs1)



class R_format:
    def __init__(self, bin_str):
        self.funct3 = bin_str[17:20]
        self.funct7 = bin_str[:7]
        self.rd_bin = bin_str[-12:-7]
        self.rs1_bin = bin_str[12:17]
        self.rs2_bin = bin_str[7:12]

    def get_regis(self):
        rd, rs1, rs2 = 0, 0, 0

        for i in range(5):
            rd += int(self.rd_bin[4 - i]) * (2 ** i)
            rs1 += int(self.rs1_bin[4 - i]) * (2 ** i)
            rs2 += int(self.rs2_bin[4 - i]) * (2 ** i)

        return rd, rs1, rs2

    def exc_inst(self, regis):
        rd, rs1, rs2 = self.get_regis()

        if self.funct3 == "000":
            if self.funct7 == "0000000": # add
                regis[rd] = regis[rs1] + regis[rs2]
            else: # sub
                regis[rd] = regis[rs1] - regis[rs2]
        if self.funct3 == "101":
            if self.funct7 == "0000000": # srl
                if regis[rs1] < 0: # negative value
                    n = regis[rs1] >> regis[rs2]
                    n_bin = twos_comp_bin(n, 32) # get two's comp bin string
                    n_bin = "0" * regis[rs2] + n_bin[regis[rs2]:]
                    n = twos_comp_imm(n_bin, len(n_bin))
                    regis[rd] = n
            else: # sra
                regis[rd] = regis[rs1] >> regis[rs2]
        if self.funct3 == "100": # xor
            regis[rd] = regis[rs1] ^ regis[rs2]
        if self.funct3 == "110": # or
            regis[rd] = regis[rs1] | regis[rs2]
        if self.funct3 == "111": # and
            regis[rd] = regis[rs1] & regis[rs2]
        if self.funct3 == "001": # sll
            regis[rd] = regis[rs1] << regis[rs2]
        if self.funct3 == "010": # slt
            if regis[rs1] < regis[rs2]:
                regis[rd] = 1
            else:
                regis[rd] = 0
        if self.funct3 == "011": # sltu
            if regis[rs1] < regis[rs2]:
                regis[rd] = 1
            else:
                regis[rd] = 0
        
        return regis


