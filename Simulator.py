




"""                                                               MIPS LITE ISA SIMULATOR

                                                ECE - 485/585 Computer Architecture Project Spring 2023
                                                
                            DESIGNED BY : Somu Jayanth Kumar Reddy , Nagulla Bhuvan Yadav, Sai Bhargav Reddy Gujjula, SaiNikhil Reddy Lokasani                       """






#opcodes for ISA    
ADD = '000000'
ADDI = '000001'
SUB = '000010'
SUBI = '000011'
MUL = '000100'
MULI = '000101'
OR = '000110'
ORI = '000111'
AND = '001000'
ANDI = '001001'
XOR = '001010'
XORI = '001011'
LDW = '001100'
STW = '001101'
BZ = '001110'
BEQ = '001111'
JR = '010000'
HALT = '010001'



#Registers and declarations
PC = 0     
arithmetic_inst = 0     
logical_inst = 0     
memory_inst = 0  
count_in = 0  
Imm = 0     
f = 0      
stalls = 0  
stalls_with_f = 0 
penalties = 0   
Rs = 0  
Rt = 0  
Rd = 0  
destination_reg = []   
trace = []  
dynamic_inst = []   
branch_flags = {}     
RAW = {}    
branch_f = {}   
memory_stores = {}  
reg_stores = {}    
current_inst = ''   


#filling all registers with 0
for x in range(32):
    destination_reg.append(0)
    


for temp in range(0, 32):
    reg_stores[temp] = 0
rtype = [ADD, SUB, MUL, OR, AND, XOR]       
itype = [ADDI, SUBI, MULI, ORI, ANDI, XORI] 
arithmetic = [ADD, ADDI, SUB, SUBI, MUL, MULI]  
logic = [OR, ORI, AND, ANDI, XOR, XORI]     
mem = [LDW, STW]                            
cont = [BZ, BEQ, JR]                        


# Reading all the instructions AND memory values from the given input trace file

lf = [l.rstrip('\n') for l in
      open('C:\\Users\\Student\\Desktop\\CDAAA\\final_proj_trace.txt')]
for temp in lf:
    trace.append(str(bin(int(temp, 16)))[2:].zfill(32))


# Displaying the end results

def display():
    global reg_stores, arithmetic_inst, logical_inst, memory_inst, count_in, dynamic_inst, stalls_with_f, f, destination_reg
    print('Instruction counts:')
    print('*' * 50)
    print('Total number of instructions: ', arithmetic_inst + logical_inst + memory_inst + count_in)
    print('Arithmetic instructions: ', arithmetic_inst)
    print("Logical instructions: ", logical_inst)
    print('Memory Access instructions: ', memory_inst)
    print('Control Transfer instructions: ', count_in)
    print('*' * 50)
    print('*' * 50)
    
    print('Final register states->')
    print('Program counter: ', PC)
   
    for x, y in reg_stores.items():
        if destination_reg[x] == 1:
            print('R',x, ':',y)
    print('Stalls without forwarding: ', stalls)
    print('Stalls with forwarding: ', stalls_with_f)
    for x, y in memory_stores.items():
        print('Address: ', x, ', Contents: ', y)
    print('_' * 50)
    print('_' * 50)
    #functional simulator complete
    print('Timing simulator output without forwarding:')
    print('Total number of clock cycles: ', f + 5 + stalls + penalties)
    print('Program Halted')
    #Timing simulator output without forwarding
    print('_' * 50)
    print('_' * 50)
    print('Timing simulator output with forwarding:')
    print("Total no. of cycles(with forwarding): ", f + 5 + stalls_with_f + penalties)
    print('Program Halted')
    print('_' * 50)
    print('_' * 50)
    

    


    
    #print('Stalls without forwarding: ', stalls)
    #print("average cycle stall for hazards:", stalls/len(RAW))
    #print('Single stalls: ', list(RAW.values()).count(-2))
    #print('Double stalls: ', list(RAW.values()).count(-1))
    #print('No. of RAW hazards: ', len(RAW))
    #print('_' * 50)
    #print('Penalties because of branches: ', penalties)
    #print('No. of branches leading to penalties: ', len(branch_f)) 
    #print('Average Branch Penality: ', penalties/len(branch_f) , 'cycles')
    #print('_' * 50)
    #print('_' * 50)
    #print('Stalls with forwarding: ', stalls_with_f)
    #print('_' * 50)
    #print('_' * 50)
    #print('Total no. of cycles(without forwarding): ', f + 5 + stalls + penalties)
    #print("Total no. of cycles(with forwarding): ", f + 5 + stalls_with_f + penalties)
    #print('_' * 50)
    #print('_' * 50)
    #print("Speedup acheive by forwarding: ", ((f + 5 + stalls + penalties)/(f + 5 + stalls_with_f + penalties)))
    
    
    


# Implementing 2's complement

def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


# Decoding values for immediate operands

def imme():
    global current_inst, Imm
    Imm = twos_comp(int(current_inst[16:], 2), len(current_inst[16:]))


# Arithmetic operations in functional simulation

def arit():
    global reg_stores, Imm, current_inst
    if current_inst[:6] == ADD:     # ADD
        reg_stores[Rd] = reg_stores[Rs] + reg_stores[Rt]
        destination_reg.insert(Rd,1)   #turning tracking bit of the destination register high
        destination_reg.pop(Rd+1)
        return
    elif current_inst[:6] == SUB:   # SUB
        reg_stores[Rd] = reg_stores[Rs] - reg_stores[Rt]
        destination_reg.insert(Rd,1)
        destination_reg.pop(Rd+1)
        return
    elif current_inst[:6] == MUL:   # MUL
        reg_stores[Rd] = reg_stores[Rs] * reg_stores[Rt]
        destination_reg.insert(Rd,1)
        destination_reg.pop(Rd+1)
        return
    else:
        imme()
        if current_inst[:6] == ADDI:    # ADDI
            reg_stores[Rt] = reg_stores[Rs] + Imm
            destination_reg.insert(Rt,1)   #turning tracking bit of the destination register high
            destination_reg.pop(Rt+1)
            return
        elif current_inst[:6] == SUBI:  # SUBI
            reg_stores[Rt] = reg_stores[Rs] - Imm
            destination_reg.insert(Rt,1)
            destination_reg.pop(Rt+1)
            return
        elif current_inst[:6] == MULI:  # MULI
            reg_stores[Rt] = reg_stores[Rs] * Imm
            destination_reg.insert(Rt,1)
            destination_reg.pop(Rt+1)
            return


# Performing logical operations in functional simulation

def logi():
    global reg_stores, Imm, current_inst
    if current_inst[:6] == OR:      # or
        reg_stores[Rd] = reg_stores[Rs] | reg_stores[Rt]
        destination_reg.insert(Rd,1)
        destination_reg.pop(Rd+1)
        return
    elif current_inst[:6] == AND:   # AND
        reg_stores[Rd] = reg_stores[Rs] & reg_stores[Rt]
        destination_reg.insert(Rd,1)
        destination_reg.pop(Rd+1)
        return
    elif current_inst[:6] == XOR:   # XOR
        reg_stores[Rd] = reg_stores[Rs] ^ reg_stores[Rt]
        destination_reg.insert(Rd,1)
        destination_reg.pop(Rd+1)
        return
    else:
        imme()
        if current_inst[:6] == ORI:     # ORI
            reg_stores[Rt] = reg_stores[Rs] | Imm
            destination_reg.insert(Rt,1)
            destination_reg.pop(Rt+1)
            return
        elif current_inst[:6] == ANDI:  # ANDI
            reg_stores[Rt] = reg_stores[Rs] & Imm
            destination_reg.insert(Rt,1)
            destination_reg.pop(Rt+1)
            return
        elif current_inst[:6] == XORI:  # XORI
            reg_stores[Rt] = reg_stores[Rs] ^ Imm
            destination_reg.insert(Rt,1)
            destination_reg.pop(Rt+1)
            return


# Performing memory operations in functional simulation

def memo():
    global reg_stores, Imm, current_inst
    imme()
    if current_inst[:6] == LDW:     # LDW
        reg_stores[Rt] = twos_comp(int(trace[int((reg_stores[Rs] + Imm) / 4)], 2), 32)
        destination_reg.insert(Rt,1)
        destination_reg.pop(Rt+1)
        return
    elif current_inst[:6] == STW:   # STW
        trace[int((reg_stores[Rs] + Imm) / 4)] = str(bin(reg_stores[Rt]))[2:].zfill(32)
        memory_stores[(reg_stores[Rs] + Imm)] = reg_stores[Rt]
        return


# Performing control operations in functional simulation

def contr():
    global reg_stores, PC, current_inst, branch_flags, f
    imme()
    branch_flags[f] = 0
    if current_inst[:6] == BZ:      # BZ
        if reg_stores[Rs] == 0:
            PC += (Imm * 4)
            branch_flags[f] = 1
        else:
            PC += 4
            return
    elif current_inst[:6] == BEQ:   # BEQ
        if reg_stores[Rs] == reg_stores[Rt]:
            PC += (Imm * 4)
            branch_flags[f] = 1
        else:
            PC += 4
            return
    elif current_inst[:6] == JR:    # JR
        PC = reg_stores[Rs]
        branch_flags[f] = 1


# Stalls AND checks for RAW dependencies
 
def depen():
    global f, dynamic_inst, stalls, penalties, RAW, stalls_with_f
    if (dynamic_inst[f][:6] in rtype) or (dynamic_inst[f][:6] == STW) or (dynamic_inst[f][:6] == BEQ):
        if dynamic_inst[f - 1][:6] in rtype:
            if (dynamic_inst[f][6:11] == dynamic_inst[f - 1][16:21]) or (dynamic_inst[f][11:16] == dynamic_inst[f - 1][16:21]):
                if dynamic_inst[f - 1][:6] in mem:
                    stalls_with_f += 1
                stalls += 2
                RAW[f] = -1
                return
        elif (dynamic_inst[f - 1][:6] in itype) or (dynamic_inst[f - 1][:6] == LDW):
            if (dynamic_inst[f][6:11] == dynamic_inst[f - 1][11:16]) or (dynamic_inst[f][11:16] == dynamic_inst[f - 1][11:16]):
                if dynamic_inst[f - 1][:6] in mem:
                    stalls_with_f += 1
                stalls += 2
                RAW[f] = -1
                return
        if f-1 in RAW.values():
            return
        elif dynamic_inst[f - 2][:6] in rtype:
            if (dynamic_inst[f][6:11] == dynamic_inst[f - 2][16:21]) or (dynamic_inst[f][11:16] == dynamic_inst[f - 2][16:21]):
                stalls += 1
                RAW[f] = -2
                return
        elif (dynamic_inst[f - 2][:6] in itype) or (dynamic_inst[f - 2][:6] == LDW):
            if (dynamic_inst[f][6:11] == dynamic_inst[f - 2][11:16]) or (dynamic_inst[f][11:16] == dynamic_inst[f - 2][11:16]):
                stalls += 1
                RAW[f] = -2
                return
    elif (dynamic_inst[f][:6] in itype) or (dynamic_inst[f][:6] == LDW) or (dynamic_inst[f][:6] == BZ) or (dynamic_inst[f][:6] == JR):
        if dynamic_inst[f - 1][:6] in rtype:
            if dynamic_inst[f][6:11] == dynamic_inst[f - 1][16:21]:
                if dynamic_inst[f - 1][:6] in mem:
                    stalls_with_f += 1
                stalls += 2
                RAW[f] = -1
                return
        elif (dynamic_inst[f - 1][:6] in itype) or (dynamic_inst[f - 1][:6] == LDW):
            if dynamic_inst[f][6:11] == dynamic_inst[f - 1][11:16]:
                if dynamic_inst[f - 1][:6] in mem:
                    stalls_with_f += 1
                stalls += 2
                RAW[f] = -1
                return
        if f - 1 in RAW.keys():
            return
        elif dynamic_inst[f - 2][:6] in rtype:
            if dynamic_inst[f][6:11] == dynamic_inst[f - 2][16:21]:
                stalls += 1
                RAW[f] = -2
                return
        elif (dynamic_inst[f - 2][:6] in itype) or (dynamic_inst[f - 2][:6] == LDW):
            if dynamic_inst[f][6:11] == dynamic_inst[f - 2][11:16]:
                stalls += 1
                RAW[f] = -2
                return


# Checking for all hazards

def checkhaz():
    global f, dynamic_inst, stalls, penalties, RAW, branch_f, branch_flags, stalls_with_f
    if f == 0:
        return
    elif f == 1:
        if (dynamic_inst[f][:6] in rtype) or (dynamic_inst[f][:6] == STW) or (dynamic_inst[f][:6] == BEQ):
            if dynamic_inst[f - 1][:6] in rtype:
                if (dynamic_inst[f][6:11] == dynamic_inst[f - 1][16:21]) or (dynamic_inst[f][11:16] == dynamic_inst[f - 1][16:21]):
                    if dynamic_inst[f - 1][:6] in mem:
                        stalls_with_f += 1
                    stalls += 2
                    RAW[f] = -1
                    return
                else:
                    return
            elif (dynamic_inst[f - 1][:6] in itype) or (dynamic_inst[f - 1][:6] == LDW):
                if (dynamic_inst[f][6:11] == dynamic_inst[f - 1][11:16]) or (dynamic_inst[f][11:16] == dynamic_inst[f - 1][11:16]):
                    if dynamic_inst[f - 1][:6] in mem:
                        stalls_with_f += 1
                    stalls += 2
                    RAW[f] = -1
                    return
                else:
                    return
        elif (dynamic_inst[f][:6] in itype) or (dynamic_inst[f][:6] == LDW) or (dynamic_inst[f][:6] == BZ) or (
                dynamic_inst[f][:6] == JR):
            if dynamic_inst[f - 1][:6] in rtype:
                if dynamic_inst[f][6:11] == dynamic_inst[f - 1][16:21]:
                    if dynamic_inst[f - 1][:6] in mem:
                        stalls_with_f += 1
                    stalls += 2
                    RAW[f] = -1
                    return
                else:
                    return
            elif (dynamic_inst[f - 1][:6] in itype) or (dynamic_inst[f - 1][:6] == LDW):
                if dynamic_inst[f][6:11] == dynamic_inst[f - 1][11:16]:
                    if dynamic_inst[f - 1][:6] in mem:
                        stalls_with_f += 1
                    stalls += 2
                    RAW[f] = -1
                    return
                else:
                    return
        else:
            return
    else:
        if (dynamic_inst[f - 1][:6] not in cont) and (dynamic_inst[f - 2][:6] not in cont):
            depen()
        elif (branch_flags[f - 1] != 1) and (branch_flags[f - 2] != 1):
            depen()
        elif branch_flags[f - 1] == 1:
            penalties += 2
            branch_f[f] = -1
        elif branch_flags[f - 2] == 1:
            depen()
        else:
            return


# Instructions which are called in other blocks of the program only when HALT doesn't occur.

while True:
    current_inst = trace[int(PC / 4)]
    dynamic_inst.append(current_inst)
    branch_flags[f] = 0
    Rs = int(current_inst[6:11], 2)
    Rt = int(current_inst[11:16], 2)
    Rd = int(current_inst[16:21], 2)
    if current_inst[:6] == HALT:    # HALT
        count_in += 1         # The value of memory instruction count is increamented
        PC += 4             # The value of program counter is updated
        break
    elif current_inst[:6] in arithmetic: # Validating whether current instruction is arithmetic operation or not
        checkhaz()
        arithmetic_inst += 1            # The value of arithmetic instruction count is increamented
        arit()
        PC += 4             # The value of program counter is updated

    elif current_inst[:6] in logic: # Validating whether current instruction is logical operation or not
        checkhaz()
        logical_inst += 1            # The value of logical instruction count is increamented
        logi()
        PC += 4             # The value of program counter is updated
    elif current_inst[:6] in mem:   # Validating whether current instruction is memory operation or not
        checkhaz()
        memory_inst += 1          # The value of memory instruction count is increamented
        memo()
        PC += 4             # The value of program counter is updated
    elif current_inst[:6] in cont:  # Validating whether current instruction is control operation or not
        checkhaz()
        count_in += 1         # The value of control instruction count is increamented
        contr()
    f += 1
display()
