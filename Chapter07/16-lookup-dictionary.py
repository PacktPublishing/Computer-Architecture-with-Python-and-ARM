print ('Demonstrating multiple length instructions.Version 3 December 8 2022 \n')
mem = [0] * 128
lookUp = {0b00001:'nop',0b00010:'stop',0b01000:'inc',0b01001:'dec', \
0b01010:'bra',0b01011:'beq',0b01100:'bne',0b10000:'mov', \
0b10001:'cmpl',0b10010:'cmp',0b10011:'ld',0b10100:'st', \
0b11000:'add',0b11001:'sub'}
allOps = {'nop':(1,1),'stop':(1,2),'inc':(2,8),'dec':(2,9),'bra':(2,10), \
'beq':(2,11),'bne':(2,12),'mov':(3,16),'ld':(3,19), \
'cmpl':(3,17),'cmp':(3,18),'add':(4,24),'sub':(4,25),'test':(0,0)}
# NOTE that progS is the actual program to be executed. It is embedded into the program
progS = ['this: equ 26','ld this:,7','that: equ 28','ld 27,2', \
'ld that:,1','loop: add 28,28,26', 'dec 26','bne loop:','stop']
symTab = {} # Label symbol table
prog = [] # progS is prog without equates
for i in range (0,len(progS)): # Process source code for equates
    thisLine = progS[i].split() # Split source code on spaces
    if len(thisLine) > 1 and thisLine[1] == 'equ': # Is this line an equate?
        symTab.update({thisLine[0][0:]:thisLine[2]}) # Store label in symbol table.
    else: prog.append(progS[i]) # Append line to prog unless it's an equate
for i in range (0,len(prog)): # Process source code (now without equates)
    prog[i] = prog[i].replace(',',' ') # Remove commas
    prog[i] = prog[i].split(' ') # Tokenize
    token1 = prog[i][0] # Get first token of instruction
    if token1[-1] == ':': # If it ends in :, it's a label
        j = str(i) # Note: we have to store i as a string not an integer
        symTab.update({token1:j}) # Add label and instruction number to symbol table
        prog[i].pop(0) # Remove label from this line. NOTE "pop"
print('Symbol table: ', symTab)
map = [0] * 64 # Map instruction number to byte address
mC = 0 # Memory counter (store code from 0)
for iC in range (0,len(prog)): # Step through the program
    instruction = prog[iC] # Read an instruction. iC = instruction counter
    mCold = mC # Remember old memory counter (address of first byte)
    map[iC] = mC # Map byte address to instruction address
    mnemonic = instruction[0] # The first token is the mnemonic
    mem[mC] = allOps[mnemonic][1] # Store opcode in memory
    mC = mC + 1 # Point to next free memory location
    numOperands = allOps[mnemonic][0] - 1 # Get the number of operands from dictionary
    if numOperands > 0: # If one or more operands
        if instruction[1] in symTab: # See if operand is in symbol table
            instruction[1] = symTab[instruction[1]] # If it is, convert into as string
        mem[mC] = int(instruction[1]) # Store address in memory as integer
        mC = mC + 1 # Bump up byte counter
    if numOperands > 1: # Do the same for two operands
        if instruction[2] in symTab: # See if operand is in symbol table
            instruction[2] = symTab[instruction[2]] # Convert to address as string
        mem[mC] = int(instruction[2])
        mC = mC + 1
    if numOperands > 2: # Now deal with 3-operand instructions
        if instruction[3] in symTab: # See if operand is in symbol table
            instruction[3] = symTab[instruction[3]] # If it is, convert to string
        mem[mC] = int(instruction[3])
        mC = mC + 1
    instPrint = ' {0:<15}'.format( (' ').join(instruction)) # reformat instruction
    print('iC=', iC,'\t', 'Op =', mnemonic, '\tNumber of operands =', \
          numOperands, '\t mC =', mCold, '\tInstruction =', \
          instPrint, 'memory =', mem[mCold:mC])
print('Memory (in bytes) =', mem[0:40], '\n')
# EXECUTE THE CODE
print('\nCode execution: press enter \n')
pc, iC, z = 0, 0, 0 # Initialize program and instruction counters
run = True
while run: # Instruction execution loop
    pcOld = pc # Remember pc at start of this cycle
    opCode = mem[pc] # Read opcode
    opLen = (opCode >> 3) + 1 # Get instruction length from opcode
    if opCode == 0b00010: # Test for stop
        run = False # Terminate on stop instruction
        print('Execution terminated on stop') # Say 'Goodbye'
        break # and exit the loop
operand1, operand2, operand3 = '', '', '' # Dummy operands (null strings)
if opLen > 1: operand1 = mem[pc + 1]
if opLen > 2: operand2 = mem[pc + 2]
if opLen > 3: operand3 = mem[pc + 3]
pc = pc + opLen
iC = iC + 1
mnemonic = lookUp[opCode]
if mnemonic == 'nop': pass
elif mnemonic == 'inc': mem[operand1] = mem[operand1] + 1
elif mnemonic == 'dec':
    z = 0
    mem[operand1] = mem[operand1] - 1
    if mem[operand1] == 0: z = 1
elif mnemonic == 'bra': pc = map[operand1] # Map instruction address to byte address
elif mnemonic == 'beq' and z == 1: pc = map[operand1]
# Map instruction address to byte address
elif mnemonic == 'bne' and z == 0: pc = map[operand1]
# Map instruction address to byte address
elif mnemonic == 'ld': mem[operand1] = operand2
elif mnemonic == 'mov': mem[operand1] = mem[operand2]
elif mnemonic == 'cmp':
    diff = mem[operand1] - mem[operand2]
    z = 0
    if diff == 0: z = 1
elif mnemonic == 'cmpl':
    diff = mem[operand1] - operand2
    z = 0
    if diff == 0: z = 1
elif mnemonic == 'add': mem[operand1] = mem[operand2] + mem[operand3]
elif mnemonic == 'sub':
    mem[operand1] = mem[operand2] - mem[operand3]
    z = 0
    if mem[operand1] == 0: z = 1
x = input('... ')
xxxx = mnemonic + ' ' + str(operand1) + ' ' + str(operand2) \
+ ' ' + str(operand3)
instPrint = ' {0:<15}'.format(xxxx) # re-format the instruction
print ('iC=',iC-1,'\tpc=',pcOld,'\tOp=',mnemonic,'z=',z, \
'\tmem 24-35=',mem[24:36],'\tInstruction = ', instPrint)