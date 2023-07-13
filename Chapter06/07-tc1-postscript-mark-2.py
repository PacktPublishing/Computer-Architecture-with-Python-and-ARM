# Version 12 July 2023

# Instruction formats
# NOP             # class 0
# BRA 4           # Class 1
# INC r1          # class 2
# LDR r1,#4       # class 3
# MOV r1,r2       # class 4
# ADD r1,r2,5     # class 5
# ADD r1,r2,r3    # class 6
# LDR r1,[r2]     # class 7
# LDR r1,[r2],4   # class 8
# MLA r1,r2,r3,r4 # class 9 [r1] = [r2] + [r3] * [r3]

def getLit(lit):                                             # Extract a literal
    if    lit in symTab:    literal = symTab[lit]            # Look in symbol table and get if there
    elif  lit       == "%": literal = int(lit[1:],2)         # If first symbol % convert binary to integer
    elif  lit[0:1]  == "$": literal = int(lit[1:],16)        # If first symbol $, convert hex to integer
    elif  lit[0]    == "-": literal = (-int(lit[1:]))&0xFFFF # If negative convert string to two's comp integer
    elif  lit.isnumeric():  literal = int(lit)               # If number is a decimal string then convert to integer
    else:                   literal = 0                      # Default value 0 if all else fails
    return(literal)

regList = {'r0':0,'r1':1,'r2':2,'r3':3,'r4':4,'r5':5,'r6':6,'r7':7}
iRegList = {'[r0]':0,'[r1]':1,'[r2]':2,'[r3]':3,'[r4]':4,'[r5]':5,'[r6]':6,'[r7]':7}
class0 = ['NOP','STOP','RTS'] # none
class1 = ['BRA','BEQ', 'BSR'] # register, literal
class2 = ['INC', 'DEC']       # register
class3 = ['LDR','STR','CMP','DBNE','LSL','LSR','ROR']  # register, literal
class4 = ['MOV','CMP','ADD'] # register, register Note ADD r1,r2
class5 = ['ADD','SUB'] # register, register, literal
class6 = ['ADD','SUB'] # register, register, register
class7 = ['LDR','STR'] # register, pointer        
class8 = ['LDR','STR'] # register, pointer, literal
class9 = ['MLA'] # register, register, register, register
 
inputSource = 0 # Manual (keyboard) input if 0; file input if 1
singleStep  = 0  # Select single-step mode or execute all to end mode
x = input('file input? type y or n ')  # Ask for file input (y) or keyboard input (any key)
if x == 'y':
    inputSource = 1
    x = input('Single step type y ')  # Type 'y' for single-step mode
    if x == 'y': singleStep = 1
    with open('c.txt','r') as fileData: 
        fileData = fileData.readlines()
    for i in range (0,len(fileData)): # Remove leading and trailing spaces
        fileData[i] = fileData[i].strip()
 
r =     [0] * 8 # Eight registers
m =     [0] * 16  # Sixteen memory locations
stack = [0] * 8  # Stack for return addresses (BSR/RTS)
prog =  []  * 64  # Program memory
progDisp = [] * 64  # Program for display
symTab = {} # Symbol table for symbolic name to value binding
run = True
pc = 0  # Clear program counter
sp = 7 # Set stack pointer to bottom of stack
while run == True:  # Program processing loop
    predicate = [] # Dummy
    if inputSource == 1: # Get instruction from file
        line = fileData[pc]
    else: line = input('>> > ') # Or input instruction from keyboard
    if line == '':
        run = False
        break
    line = " ".join(line.split()) # Remove multiple spaces USES join and split!!!
    progDisp.append(line)  # Make copy of this line for later display
    line = line.replace(',',' ')
    line = line.split(' ') # Split instruction into tokens
    if (len(line) > 1) and (line[0][-1] == ':'): # Look for a label (token 0 ending in :)
        label = line[0]
        symTab[line[0]] = pc  # Put a label in the symTab alongside the pc       
    else:
        line.insert(0,'    :') # If no label insert a dummy one (for pretty printing)
    mnemonic  = line[1]  # Get the mnemonic, second token
    predicate = line[2:] # What's left is the predicate (registers and literal)
    
    prog.append(line) # Append the line to the program
    pc = pc + 1       # And bump up the program counter
    progLength = pc - 1 # Record the total number of instructions
for i in range (0,pc-1):
    print('pc =', f'{i:3}', (' ').join(prog[i])) # Print the program
print('Symbol table =', symTab, '\n') # Display the symbol table
pc = 0
run = True
z = 0
c = 0
classNum = 10
while run == True: # Program execution loop
    instruction = prog[pc]
    pcOld = pc
    pc = pc + 1
    if instruction[1] == 'STOP': 	# Halt on STOP instruction
        print('End of program exit')
        break
    mnemonic  = instruction[1]
    predicate = instruction[2:]

    predLen   = len(predicate)
    if (predLen > 0) and (mnemonic not in class1): rD = regList[predicate[0]]  # Get rD for classes 2 to 8
    
    if mnemonic in class0: 	# Deal with instruction by their group (class)
        classNum = 0
        if mnemonic == 'NOP': pass 
        if mnemonic == 'RTS':
            pc = stack[sp]
            sp = sp + 1

    if mnemonic in class1:
        classNum = 1
        literal = getLit(predicate[0])
        if   mnemonic == 'BRA': pc = literal
        elif mnemonic == 'BEQ':
            if z == 1: pc = literal
        elif mnemonic == 'BSR':
            sp = sp - 1
            stack[sp] = pc
            pc = literal
        
    if mnemonic in class2:
        classNum = 2
        if mnemonic == 'INC': r[rD] = r[rD] + 1
        if mnemonic == 'DEC':
            r[rD] = r[rD] - 1
            if r[rD] == 0: z = 1
            else: z = 0

    if (mnemonic in class3) and (predLen == 2) and (predicate[1] not in regList): #CHECK
        classNum = 3
        literal = getLit(predicate[-1])
        if mnemonic == 'CMP':
            diff = r[rD] - literal
            if diff == 0: z = 1
            else:         z = 0
        elif mnemonic == 'LDR': r[rD] = literal
        elif mnemonic == 'STR': m[literal] = r[rD]
        elif mnemonic == 'DBNE':
            r[rD] = r[rD] - 1
            if r[rD] != 0: pc = literal # Note we don't use z flag
        elif mnemonic == 'LSL':
            for i in range(0,literal):
                c = ((0x8000) & r[rD]) >> 16
                r[rD] = (r[rD] << 1) & 0xFFFF # Shift left and constrain to 16 bits
        elif mnemonic == 'LSR':
            for i in range(0,literal):
                c = ((0x0001) & r[rD])
                r[rD] = r[rD] >> 1                
        elif mnemonic == 'ROR':
            for i in range(0,literal):
                c = ((0x0001) & r[rD])
                r[rD] = r[rD] >> 1
                r[rD] = r[rD] | (c << 15)

    if (mnemonic in class4) and (predLen == 2) and (predicate[1] in regList):  #
        classNum = 4        
        rS1 = regList[predicate[1]] # Get second register        
        if mnemonic == 'MOV':
           r[rD] = r[rS1]
        elif mnemonic == 'CMP':
            diff = r[rD] -  r[rS1]
            if diff == 0: z = 1
            else:         z = 0
        elif mnemonic == 'ADD':
            r[rD] = r[rD] + r[rS1]

    if (mnemonic in class5) and (predLen == 3) and (predicate[2] not in regList):
        classNum = 5
        literal = getLit(predicate[2])
        rS1 = regList[predicate[1]]
        if   mnemonic == 'ADD': r[rD] = r[rS1] + literal
        elif mnemonic == 'SUB': r[rD] = r[rS1] - literal        

    if (mnemonic in class6) and (predLen == 3) and (predicate[-1] in regList):
        classNum = 6
        rS1 = regList[predicate[1]]
        rS2 = regList[predicate[2]]        
        if   mnemonic == 'ADD': r[rD] = r[rS1] + r[rS2]
        elif mnemonic == 'SUB': r[rD] = r[rS1] - r[rS2]	

    if (mnemonic in class7) and (predLen == 2) and (predicate[1] in iRegList):
        classNum = 7
        pReg  = predicate[1]
        pReg1 = iRegList[pReg]
        pReg2 = r[pReg1]
        if   mnemonic == 'LDR': r[rD] = m[pReg2] 
        elif mnemonic == 'STR': m[pReg2] = r[rD]  

    if (mnemonic in class8) and (predLen == 3):
        classNum = 8
        pReg  = predicate[1]
        pReg1 = iRegList[pReg]
        pReg2 = r[pReg1]
        literal = getLit(predicate[2]) 
        if   mnemonic == 'LDR': r[rD] = m[pReg2 + literal] 
        elif mnemonic == 'STR': m[pReg2 + literal] = r[rD] 	

    if mnemonic in class9:
        classNum = 9
        if mnemonic == 'MLA':
            rS1 = regList[predicate[1]]
            rS2 = regList[predicate[2]]
            rS3 = regList[predicate[3]] 
            r[rD] = r[rS1] * r[rS2] + r[rS3] 

    pInst = ' '.join(instruction) ##############
    regs = " ".join("%04x" % i for i in r)

    
    print("pc {:<2}".format(pcOld),'Class =', classNum, "{:<20}".format(pInst),'Regs: ', regs, 'Mem', m, 'r[0] =', '{:016b}'.format(r[0]),  'c =', c, 'z =', z, '\n')
    print(progDisp[pcOld])
    if singleStep == 1: input(' >>> ')