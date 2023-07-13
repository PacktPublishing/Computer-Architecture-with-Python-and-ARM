### TC2 CISC machine
### Demonstration register-to-memory architecture Designed 22 January 2022. 
### Instruction formats and addressing modes
### Mode 0:  NOP, STOP        No operand length 1
### Mode 1:  INC R1           Single register operand
### MODE 2:  BEQ XXX          Literal operand
### MODE 3:  Reserved
### MODE 4:  MOV r1,literal   Two-operand, register and literal 
### MODE 5:  MOV r1,r2        Two-operand, register to register
### MODE 6:  MOV r1,[r2]      Two-operand, register indirect to register
### MODE 7:  MOV [r1],r2      Two-operand, register to register indirect
### MODE 8:  MOV [r1],[r2]    Two-operand, register indirect to register indirect
### MODE 9:  MOV M,r2         Two-operand, register to memory address
### MODE 10: MOV M,[r2]       Two-operand, register indirect to memory address
### MODE 11: MOV r1,M         Two-operand, memory address to register
### MODE 12: MOV [r1],M       Two-operand, memory address to register indirect

### The sample test code
###       MOV  r0,#8      @  Memory locations 1 to 8 with random numbers
### Next: RND  r5
###       MOV  [r0],r5
###       DEC  r0
###       BNE  Next
###       EQU   X,#1      @  Vector 1	
###       EQU   Y,#5      @  Vector 5	
###       EQU   Z,#9      @  Vector 9	
###       MOV   r1,#X     @  r0 points to array X         11 0000 0100 000 000 00000001
###       MOV   r2,#Y     @  r1 points to array Y         11 0000 0100 001 000 00000101
###       MOV   r3,#Z     @  r2 points to array Z         11 0000 0100 010 000 00001001
###       MOV   r4,#6     @  r4 number of elements to add 11 0000 0100 011 000 00000100
### Loop: MOV   r5,[r1]   @  REPEAT: Get xi               11 0000 0110 100 000 00000000
###       ADD   r5,#6     @  Add 6 to xi                  11 0001 0100 100 000 00000101
###       ADD   r5,[r2]   @  Add xi + 5 to yi             11 0001 0110 100 001 00000000
###       MOV   [r3],r5   @  Store result in array Z      11 0000 0111 010 100 00000000
###       INC   r1        @  Increment pointer to array X 10 0000 0010 000 000 00000000
###       INC   r2        @  Increment pointer to array Y 10 0000 0010 001 000 00000000
###       INC   r3        @  Increment pointer to array Z 10 0000 0010 010 000 00000000
###       DEC   r4        @  Decrement loop counter       10 0001 0010 011 000 00000000
###       BNE   Loop      @  Continue until counter zero  01 0010 0001 000 000 00000100
###       STOP                                            00 1111 0000 000 000 00000000

import random   # Library of random number operations (used to generate 8-bit random number in a register)



### Dictionaries and variables
mnemon  = {'MOV':48,'MOVE':48,'ADD':49,'SUB':50,'CMP':51,'NOT':52,'AND':53,'OR':54,'EOR':55,  \
           'ONES':56, 'MRG':57,'FFO':58,'LSL':59,'LSR':60,'ADC':61,'INC':32,'DEC':33,'RND':34, \
           'CZN':19,'TST':36,'NOP':0,'BRA':16,'BEQ':17,'BNE':18,'STOP':14,'END':15}
mnemonR = {48:'MOV',49:'ADD',50:'SUB',51:'CMP',52:'NOT',53:'AND',54:'OR',55:'EOR',56:'ONES',  \
           57:'MRG',58:'FFO',59:'LSL',60:'LSR',61:'ADC',32:'INC',33:'DEC', 34:'RND',19:'CZN',  \
          36:'TST',0:'NOP',16:'BRA',17:'BEQ',18:'BNE',14:'STOP',15:'END'}
rName   = {'R0':0,'R1':1,'R2':2,'R3':3,'R4':4,'R5':5,'R6':6,'R7':7}                 # Register table
rNamInd = {'[R0]':0,'[R1]':1,'[R2]':2,'[R3]':3,'[R4]':4,'[R5]':5,'[R6]':6,'[R7]':7} # Indirect registers

iClass0 = ['STOP', 'NOP','END']                                    # class 00 mnemonic with no operands            
iClass1 = ['BRA','BEQ','BNE','CZN']                                # class 01 mnemonic with literal operand
iClass2 = ['INC','DEC','RND','TST']                                # class 10 mnemonic with register operand  
iClass3 = ['MOV','MOVE','ADD','ADC','SUB','CMP', 'NOT', \
           'AND','OR','EOR''ONES','MRG','FFO','LSL','LSR']   # class 11 mnemonic two operands

sTab = {}                                            # Symbol table for equates and labels name:integerValue
pMem = []                                            # Program memory (initially empty)
dMem = [0]*16                                        # Data memory
reg  = [0]*8                                         # Register set
z,c,n = 0,0,0                                        # Define and clear flags zero, carry, negative


def getL(lit8):                                      # Convert string to integer
    lit8v = 9999                                     # Dummy default
    if lit8[0:2]   == 'M:': lit8  = lit8[2:]         # Strip M: prefix from memory literal addresses     
    if lit8[0:1]   == '#':  lit8  = lit8[1:]         # Strip # prefix from literal addresses         
    if   type(lit8) == int: lit8v = lit8             # If integer, return it
    elif lit8.isnumeric():  lit8v = int(lit8)        # If decimal in text from convert to integer
    elif lit8 in sTab:      lit8v = sTab[lit8]       # If in symbol table, retrieve it
    elif lit8[0]   == '%':  lit8v = int(lit8[1:],2)  # If binary string convert to int
    elif lit8[0:2] == '0X': lit8v = int(lit8[2:],16) # If hex string convert to int
    elif lit8[0]   == '-':  lit8v = -int(lit8[1:]) & 0xFF # If decimal negative convert to signed int
    return(lit8v)                                    # Return integer corresponding to text string

def alu(fun,op1,op2):                                # Perform arithmetic and logical operations on operands 1 and 2
    global z,n,c                                     # Make flags global
    z,n,c = 0,0,0                                    # Clear status flags initially   
    if   fun == 0: res = op2                          # MOV: Perform data copy from source to destination
    elif fun == 1:                                    # ADD: Perform addition - and ensure 8 bits plus carry
        res = (op1 + op2)                             #      Do addition of operands
        if thisOp == 'ADC': res = res + c             #      If operation ADC then add carry bit
    elif fun == 2: res = (op1 - op2)                  # SUB: Perform subtraction
    elif fun == 3: res = op1 - op2                    # CMP: Same as subtract without writeback
    elif fun == 4: res = op1 & op2                    # AND: Perform bitwise AND
    elif fun == 5: res = op1 | op2                    # OR
    elif fun == 6: res = ~op2                         # NOT
    elif fun == 7: res = op1 ^ op2                    # EOR
    elif fun == 8:
        res = op2 << 1                                # LSL: Perform single logical shift left
    elif fun == 9:
        res = op2 >> 1                                # LSR: Perform single logical shift right
    elif fun == 10:                                   # ONES (Count number of 1s in register)
       onesCount = 0                                    # Clear the 1s counter
       for i in range (0,8):                            # For i = 0 to 7 (test each bit) AND with 10000000 to get msb
           if op2 & 0x80 == 0x80:                         # If msb is set
               onesCount = onesCount + 1                  # increment the 1s counter
           op2 = op2 << 1                                 # shift the operand one place left
       res = onesCount                                    # Destination operand is 1s count
    elif fun == 11:                                   # MRG (merge alternate bits of two registers)
         t1 = op1 & 0b10101010                          # Get even source operand bits
         t2 = op2 & 0b01010101                          # Get odd destination operand bits
         res = t1 | t2                                  # Merge them using an OR
    elif fun == 12:                                     # FFO (Find position of leading 1)
        res = 8                                         # Set default position 8 (i.e., leading 1 not found)
        for i  in range (0,8):                          # Examine the bits one by one
          temp = op2 & 0x80                               # AND with 10000000 to get leading bit and save
          op2 = op2 << 1                                  # Shift operand left
          res = res - 1                                   # Decrement place counter          
          if temp == 128: break                           # If the last tested bit was 1 then jump out of loop

    if res & 0xFF == 0:        z = 1                  # TEST FLAGS z = 1 if bits 0 to 7 all 0
    if res & 0x80 == 0x80:     n = 1                  # If bit 7 is one, set the carry bit
    if res & 0x100 == 0x100:   c = 1                  # carry bit set if bit 8 set
    if (thisOp == 'LSR') and (op2 & 1 == 1): c = 1    # Deal with special case of shift right (carry out is lsb)
    return(res & 0xFF)                                # Return and ensure value eight bits


def trace():                                          # Function to print execution data                                
    cF   = "{0:<20}".format(" ".join(src[pcOld]))     # 1. instruction
    icF  = 'pc = ' + "{:<3}".format(pcOld)            # 2. pc
    binF = format(inst, "024b")                       # 3. binary code
    iClF = 'Class = '+ str(iClass)                    # 4. instruction class
    modF = 'mode = ' + str(mode)                      # 5. instruction mode NOTE we have to convert mode to string
    t0F  = "{:<5}".format(t0)                         # 6. token 0 (mnemonic)
    t1F  = "{:<5}".format(t1)                         # 7. token 1 (register field 1)
    t2F  = "{:<10}".format(t2)                        # 8. token 2 (register field 2 or literal)
    rF   = 'Reg = '+ " ".join("%02x" % b for b in reg)# 9. Registers in hex format
    m    = dMem[0:11]                                 # 10. First 10 memory locations
    mF   = 'Mem = '+ " ".join("%02x" % b for b in m)  # 11. Hex formatted memory values
    ccrF = 'C = '+ str(c) + ' Z = ' + str(z) +' N = ' + str(n) # 12. Condition codes
    x = input('>>> ')                                 # 13. Wait for keyboard input (return)
    print(cF,icF,binF,iClF, modF, rF, mF,ccrF)        # 14. Print the computer status data
    return()

testCode = "test_TC3_1.txt"           # Source filename on my computer
with open(testCode) as src:                    # Open source file with assembly language program
    lines = src.readlines()                    # Read the program into lines
src.close()                                    # Close the source file
src = [i[0:-1].lstrip()  for i in lines ]      # Remove the /n newline from each line of the source code
src = [i.split("@")[0] for i in src]           # Remove comments in the code
src = [i for i in src if i != '']              # Remove empty lines
for i in range(0,len(src)):                    # Scan source code line-by-line
    src[i] = src[i].replace(',',' ')           # Replace commas by a space
    src[i] = src[i].upper()                    # Convert to upper-case
    src[i] = src[i].split()                    # Split into tokens (label, mnemonic, operands)

src1 = []                                      # Set up dummy source file, initially empty
for i in range (0,len(src)):                   # Read source and stop on first END operation
    src1.append(src[i])                        # Append line to dummy source file
    if src[i][0] == 'END': break               # Stop on 'END' token
src = src1                                     # Copy dummy file to source (having stopped on 'END')
    
for i in range (0,len(src)):                   # Deal with equates of the form EQU PQR 25
    if src[i][0] == 'EQU':                     # If the line is 3 or more tokens and first token is EQU
        sTab[src[i][1]] = getL(src[i][2])      # Put token in symbol table as integer  getL deals with number format
src = [i for i in src if i.count("EQU") == 0]  # Remove lines with "EQU" from source code (these are not instructions)

for i in range(0,len(src)):                    # Add label addresses to symbol table
    if src[i][0][-1] == ':':                   # If first token is a label with : terminator
        sTab.update({src[i][0][0:-1]:i})       # add it to the symbol table. 
   
xLm = 0                                        # Length of maximum instruction (for printing)
for i in range (0,len(src)):                   # Step through source array
    xL = len(' '.join(src[i]))                 # Get the length of each line after joining tokens
    if xL > xLm: xLm = xL                      # If xL > xLm  NOTE: THIS facility is not used in this version

print('Source code')                           # Display tokenized source code
for i in range(0,len(src)): print(src[i])      # 
print("\nEquate and branch table\n")           # Display the symbol table
for x,y in sTab.items():                       # Step through the symbol table dictionary structure
    print("{:<8}".format(x),y)                 # Display each line as label and value 

##testing
for i in range (0,len(src)):
    print('code ', src[i])
    
      





print('\nAssembly loop \n')

for ic in range(0,len(src)):                   # ASSEMBLY LOOP (ic = instruction counter)
    t0,t1,t2 = '','',''                        # Prepare to assign tokens. Initialize to null string
    if src[ic][0][-1] != ':':                  # If the first token doesn't end in colon, its an instruction
        j = 0                                  # j = 0 for line starting with mnemonic
    else:                                      # If the first token ends in a colon it's a label
        j = 1                                  # j = 1 if mnemonic is second token
    t0 = src[ic][j]                            # Set t0 to mnemonic
    if len(src[ic]) > 1+j: t1 = src[ic][j+1]   # Set t1 to single operand 
    if len(src[ic]) > 2+j: t2 = src[ic][j+2]   # Set t2 to second operand
    tLen = len(src[ic]) - j - 1                # tLen is the number of tokens (adjusted for any label)

    binC = 0                                   # Initialize binary code for this instruction to all zeros
    opCode = mnemon[t0]                        # Look up op-code in table mnemon using token t0
    iClass = opCode >> 4                       # Get two most significant bits of op-code (i.e., class)
    if   t0 in iClass0:                        # If in iClass0 it's a single instruction, no operands
        mode = 0                               # The mode is 0 for everything in this class
        binC = (mnemon[t0] << 18)              # All fields zero except op_code        

    elif t0 in iClass1:                        # If in iClass1 it's an 0p-code plus offset (e.g., branch)
        mode = 1                               # All class 1 instruction are mode 1 (op-code plus literal)
        binC = (mnemon[t0] << 18) + (mode << 14)  + getL(t1) # Create binary code with operation plus address (literal)

    elif t0 in iClass2:                        # If in iClass2 it's an op-code plus register number
        mode = 2                               # All instruction are mode 2
        binC = (mnemon[t0] << 18) + (mode << 14)  + (rName[t1] << 11) # Create binary code 

    elif t0 in iClass3:                             # Two-operand inst. All data-processing and movement ops in iClass3
        if   (t1 in rName) and (t2[0] == '#'):      # Look for register name and literal for mode 4
            mode = 4                                #
        elif (t1 in rName) and (t2 in rName):       # Look for register name and register name for mode 5
            mode = 5       
        elif (t1 in rName) and (t2 in rNamInd):     # Look for register name and register indirect name (r1,[r2])
            mode = 6 
        elif (t1 in rNamInd) and (t2 in rName):     # Look for register indirect name and register ([r1],r2)
            mode = 7   
        elif (t1 in rNamInd) and (t2 in rNamInd):   # Look for two register indirect names ([r1],[r2])
            mode = 8  
        elif (t1[0:2] == 'M:') and (t2 in rName):   # Look for literal prefixed by M: and register name (M:12,r4)
            mode = 9
        elif (t1[0:2] == 'M:') and (t2 in rNamInd): # Look for literal prefixed by M: and register indirect name (M:12,[r4])
            mode = 10
        elif (t1 in rName) and (t2[0:2] == 'M:'):   # Look register name and literal prefixed by M:
            mode = 11    
        elif (t1 in rNamInd) and (t2[0:2] == 'M:'): # Look register indirect name and literal prefixed by M:
            mode = 12       
        binC = (mnemon[t0] << 18) + (mode << 14)     # Insert op_Code and mode fields in the instruction
        
        rField1, rField2, lField = 0, 0, 0           # Calculate register and literal fields. Initialize to zero
        if mode in [4,5,6,11]: rField1 = rName[t1]   # Convert register names into register numbers rField1is first register
        if mode in [7,8,12]:   rField1 = rNamInd[t1] #       
        if mode in [5,7,9]:    rField2 = rName[t2]   # rFiled2 is second register field
        if mode in [6,8,10]:   rField2 = rNamInd[t2] #
        if mode in [4,11,12]:  lField  = getL(t2)    # if (mode == 4) or (mode == 11) or (mode == 12): Get literal
        if mode in [9,10]:     lField  = getL(t1)    # if (mode == 9) or (mode == 10):  lField = getL(t1) Literal field
        
        binC = binC+(rField1 << 11)+(rField2 << 8)+lField   # Binary code with register and literal fields added
    pMem.append(binC)                                       # Append instruction to program memory in pMem 

### Display the assembly details of each instruction (this is for diagnostics)
    pcF  = "{0:<20}".format(" ".join(src[ic]))                   # 1. instruction
    icF  = 'pc = ' + "{:<3}".format(ic)                          # 2. pc
    binF = format(binC, "024b")                                  # 3. binary code
    iClF = 'Class = '+ str(iClass)                               # 4. instruction class
    modF = 'mode = ' + str(mode)                                 # 5. instruction mode NOTE convert mode to string
    t0F  = "{:<5}".format(t0)                                    # 6. token 0 (mnemonic)
    t1F  = "{:<5}".format(t1)                                    # 7. token 1 (register field 1)
    t2F  = "{:<10}".format(t2)                                   # 8. token 2 (register field 2 or literal)
    print(pcF,icF,binF,iClF,modF,t0F,'t1 =',t1F,t2F)             # Print these fields

print('\nEXECUTE \n')
### EXECUTE LOOP                            # reverse assemble the binary instruction to recover the fields and execute the instruction
pc = 0                                      # Reset the program counter to 0
run = True                                  # run flag: True to execute, False to stop (stop on END or STOP)
while run == True:                          # MAIN LOOP
    op1, op2, op3 = 0,0,0                   # Initialize data operands
    inst = pMem[pc]                         # Fetch current instruction. inst is the binary op-code  executed in this cycle
    pcOld = pc                              # Remember current pc for printing/display 
    pc = pc + 1                             # Increment program counter for next cycle
    iClass = inst >> 22                     # Extract operation class 0 to 3 (top two bits)
    opCode = (inst >> 18)   & 0b111111      # Extract the current op-code
    mode   = (inst >> 14)   & 0b1111        # Extract the addressing mode
    reg1   = (inst >> 11)   & 0b0111        # Extract register 1 number
    reg2   = (inst >>  8)   & 0b0111        # Extract register 2 number
    lit    = inst           & 0b11111111    # Extract the 8-bit literal in the least significant bits


### EXECUTE THE CODE
    thisOp = mnemonR[opCode]                                     # Reverse assemble. Get mnemonic from op-code 
    if iClass == 0:  # Class 0 operation                        # Class 0 no-operand instructions
        if thisOp == 'END' or thisOp == 'STOP': run = False      # If END or STOP clear run flag to stop execution
        if opCode == 'NOP': pass                                 # If NOP then do nothing and "pass"
    elif iClass == 1:  # Class 1 operation   branch              # Class 1 branch and instr with literal operandÂ’s
        if    thisOp == 'BRA': pc = lit                          # BRA Branch unconditionally PC = L
        elif (thisOp == 'BEQ') and (z == 1): pc = lit            # BEQ Branch on zero
        elif (thisOp == 'BNE') and (z == 0): pc = lit            # BNE Branch on not zero
        elif thisOp == 'CZN':                                    # Set/clear c, z, and n flags.
            c = (lit & 0b100) >> 2                               # Bit 2 of literal is c
            z = (lit & 0b010) >> 1                               # Bit 1 of literal is z            
            n = (lit & 0b001)                                    # Bit 0 of literal is c
            
    elif iClass == 2:                                            # Class 0 single-register operand
        if   thisOp == 'INC': reg[reg1] = alu(1,reg[reg1],1)     # Call ALU with second operand 1 to do increment
        elif thisOp == 'DEC': reg[reg1] = alu(2,reg[reg1],1)     # Decrement register
        elif thisOp == 'RND': reg[reg1] = random.randint(0,0xFF) # Generate random number in range 0 to 0xFF 
        elif thisOp == 'TST':                                    # Test a register: return z and n flags. Set c to 0
            z, n, c = 0, 0, 0                                    #    Set all flags to 0                                              
            if reg[reg1] == 0:           z = 1                   #    If operand 0 set z flag
            if reg[reg1] & 0x80 == 0x80: n = 1                   #    If operand ms bit 1 set n bit
 
    elif iClass == 3:                                            # Class 3 operation: Two operands. 
        if   mode in [4,5,6,11]: op1 = reg[reg1]                 # Register, literal e.g. MOVE r1,#5 or ADD r3,#0xF2
        elif mode in [7,8,12]:   op1 = dMem[reg[reg1]]           # Register, literal e.g. MOVE r1,#5 or ADD r3,#0xF2
        elif mode in [9,10]:     op1 = lit                       # MOV M:12,r3 moves register to memory     
        if   mode in [4,11,12]:  op2 = lit                       # Mode second operand literal
        elif mode in [5,7,9]:    op2 = reg[reg2]                 # Modes with second operand contents of register
        elif mode in [6,8,10]:   op2 = dMem[reg[reg2]]           # Second operand pointed at by register
 
        if thisOp == 'MOV' : fun = 0                             # Use mnemonic to get function required by ALU
        if thisOp == 'ADD' : fun = 1                             # ADD and ADC use same function
        if thisOp == 'ADC' : fun = 1
        if thisOp == 'SUB' : fun = 2
        if thisOp == 'AND' : fun = 4
        if thisOp == 'OR'  : fun = 5
        if thisOp == 'NOT' : fun = 6
        if thisOp == 'EOR' : fun = 7
        if thisOp == 'LSL' : fun = 8
        if thisOp == 'LSR' : fun = 9
        if thisOp == 'ONES': fun = 10
        if thisOp == 'MRG' : fun = 11        
        if thisOp == 'FFO' : fun = 12
        op3 = alu(fun,op1,op2)                                   # Call ALU to perform the function
        if   mode in [4,5,6,11]: reg[reg1]       = op3           # Writeback ALU result in op3 result to a register
        elif mode in [7,8,12]:   dMem[reg[reg1]] = op3           # Writeback result to mem pointed at by reg       
        elif mode in [9,10]:     dMem[lit]       = op3           # Writeback the result to memory
  
    trace()                                                      # Display the results line by line