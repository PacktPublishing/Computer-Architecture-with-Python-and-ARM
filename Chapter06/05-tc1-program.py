### TC1 computer simulator and assembler. Version of 11 September 2022
''' This is the table of instructions for reference and is not part of the program code
00 00000 stop operation STOP 00 00000 000 000 000 0 0000
00 00001 no operation NOP 00 00001 000 000 000 0 0000
00 00010 get character from keyboard GET r0 00 00010 rrr 000 000 0 1000
00 00011 get character from keyboard RND r0 00 00011 rrr 000 000 L 1001
00 00100 swap bytes in register SWAP r0 00 00100 rrr 000 000 0 1000
00 01000 print hex value in register PRT r0 00 01000 rrr 000 000 0 1000
00 11111 terminate program END! 00 11111 000 000 000 0 0000
01 00000 load register from register MOVE r0,r1 01 00000 rrr aaa 000 0 1100
01 00001 load register from memory LDRM r0,L 01 00001 rrr 000 000 L 1001
01 00010 load register with literal LDRL r0,L 01 00010 rrr 000 000 L 1001
01 00011 load register indirect LDRI r0,[r1,L] 01 00011 rrr aaa 000 L 1101
01 00100 store register in memory STRM r0,L 01 00100 rrr 000 000 L 1001
01 00101 store register indirect STRI r0,[r1,L] 01 00101 rrr aaa 000 L 1101
10 00000 add register to register ADD r0,r1,r2 10 00000 rrr aaa bbb 0 1110
10 00001 add literal to register ADDL r0,r1,L 10 00001 rrr aaa 000 L 1101
10 00010 subtract register from register SUB r0,r1,r2 10 00010 rrr aaa bbb 0 1110
10 00011 subtract literal from register SUBL r0,r1,L 10 00011 rrr aaa 000 L 1101
10 00100 multiply register by register MUL r0,r1,r2 10 00100 rrr aaa bbb 0 1110
10 00101 multiply literal by register MULL r0,r1,L 10 00101 rrr aaa 000 L 1101
10 00110 divide register by register DIV r0,r1,r2 10 00110 rrr aaa bbb 0 1110
10 00111 divide register by literal DIVL r0,r1,L 10 00111 rrr aaa 000 L 1101
10 01000 mod register by register MOD r0,r1,r2 10 01000 rrr aaa bbb 0 1110
10 01001 mod register by literal MODL r0,r1,L 10 01001 rrr aaa 000 L 1101
10 01010 AND register to register AND r0,r1,r2 10 01000 rrr aaa bbb 0 1110
10 01011 AND register to literal ANDL r0,r1,L 10 01001 rrr aaa 000 L 1101
10 01100 OR register to register OR r0,r1,r2 10 01010 rrr aaa bbb 0 1110
10 01101 NOR register to literal ORL r0,r1,L 10 01011 rrr aaa 000 L 1101
10 01110 EOR register to register OR r0,r1,r2 10 01010 rrr aaa bbb 0 1110
10 01111 EOR register to literal ORL r0,r1,L 10 01011 rrr aaa 000 L 1101
10 10000 NOT register NOT r0 10 10000 rrr 000 000 0 1000
10 10010 increment register INC r0 10 10010 rrr 000 000 0 1000
10 10011 decrement register DEC r0 10 10011 rrr 000 000 0 1000
10 10100 compare register with register CMP r0,r1 10 10100 rrr aaa 000 0 1100
10 10101 compare register with literal CMPL r0,L 10 10101 rrr 000 000 L 1001
10 10110 add with carry ADC 10 10110 rrr aaa bbb 0 1110
10 10111 subtract with borrow SBC 10 10111 rrr aaa bbb 0 1110
10 11000 logical shift left LSL r0,L 10 10000 rrr 000 000 0 1001
10 11001 logical shift left literal LSLL r0,L 10 10000 rrr 000 000 L 1001
10 11010 logical shift right LSR r0,L 10 10001 rrr 000 000 0 1001
10 11011 logical shift right literal LSRL r0,L 10 10001 rrr 000 000 L 1001
10 11100 rotate left ROL r0,L 10 10010 rrr 000 000 0 1001
10 11101 rotate left literal ROLL r0,L 10 10010 rrr 000 000 L 1001
10 11110 rotate right ROR r0,L 10 10010 rrr 000 000 0 1001
10 11111 rotate right literal RORL r0,L 10 10010 rrr 000 000 L 1001
11 00000 branch unconditionally BRA L 11 00000 000 000 000 L 0001
11 00001 branch on zero BEQ L 11 00001 000 000 000 L 0001
11 00010 branch on not zero BNE L 11 00010 000 000 000 L 0001
11 00011 branch on minus BMI L 11 00011 000 000 000 L 0001
11 00100 branch to subroutine BSR L 11 00100 000 000 000 L 0001
11 00101 return from subroutine RTS 11 00101 000 000 000 0 0000
11 00110 decrement & branch on not zero DBNE r0,L 11 00110 rrr 000 000 L 1001
11 00111 decrement & branch on zero DBEQ r0,L 11 00111 rrr 000 000 L 1001
11 01000 push register on stack PUSH r0 11 01000 rrr 000 000 0 1000
11 01001 pull register off stack PULL r0 11 01001 rrr 000 000 0 1000
'''
import random                               # Get library for random number generator
def alu(fun,a,b):                           # Alu defines operation and a and b are inputs
    global c,n,z                            # Status flags are global and are set up here
    if fun == 'ADD': s = a + b
    elif fun == 'SUB': s = a - b
    elif fun == 'MUL': s = a * b
    elif fun == 'DIV': s = a // b           # Floor division returns an integer result
    elif fun == 'MOD': s = a % b            # Modulus operation gives remainder: 12 % 5 = 2
    elif fun == 'AND': s = a & b            # Logic functions
    elif fun == 'OR': s = a | b
    elif fun == 'EOR': s = a & b
    elif fun == 'NOT': s = ~a
    elif fun == 'ADC': s = a + b + c        # Add with carry
    elif fun == 'SBC': s = a - b - c        # Subtract with borrow
    c,n,z = 0,0,0                           # Clear flags before recalculating them
    if s & 0xFFFF == 0: z = 1               # Calculate the c, n, and z flags
    if s & 0x8000 != 0: n = 1               # Negative if most sig bit 15 is 1
    if s & 0xFFFF != 0: c = 1               # Carry set if bit 16 is 1
    return (s & 0xFFFF)                     # Return the result constrained to 16 bits
def shift(dir,mode,p,q):                    # Shifter: performs shifts and rotates. dir = left/right, mode = logical/rotate
    global z,n,c                            # Make flag bits global. Note v-bit not implemented
    if dir == 0:                            # dir = 0 for left shift, 1 for right shift
        for i in range (0,q):               # Perform q left shifts on p
            sign = (0x8000 & p) >> 15       # Sign bit
            p = (p << 1) & 0xFFFF           # Shift p left one place
            if mode == 1:p = (p & 0xFFFE) | sign # For rotate left, add in bit shifted out
    else:                                   # dir = 1 for right shift
        for i in range (0,q):               # Perform q right shifts
            bitOut = 0x0001 & p             # Save lsb shifted out
            sign = (0x8000 & p) >> 15       # Get sign-bit for ASR
            p = p >> 1                      # Shift p one place right
            if mode == 1:p = (p&0x7FFF)|(bitOut<<15) # If mode = 1, insert bit rotated out
            if mode == 2:p = (p&0x7FFF)|(sign << 15) # If mode = 2, propagate sign bit
    z,c,n = 0,0,0                           # Clear all flags
    if p == 0: z = 1                        # Set z if p is zero
    if p & 0x8000 != 0: n = 1               # Set n-bit if p = 1
    if (dir == 0) and (sign == 1): c = 1    # Set carry if left shift and sign 1
    if (dir == 1) and (bitOut == 1): c = 1  # Set carry bit if right shift and bit moved out = 1
    return(0xFFFF & p)                      # Ensure output is 16 bits wide
def listingP():                             # Function to perform listing and formatting of source code
    global listing                          # Listing contains the formatted source code
    listing = [0]*128                       # Create formatted listing file for display
    if debugLevel > 1: print('Source assembly code listing ')
    for i in range (0,len(sFile)):          # Step through the program
        if sFile[i][0] in codes:            # Is first token in opcodes (no label)?
            i2 = (' ').join(sFile[i])       # Convert tokens into string for printing
            i1 = ''                         # Dummy string i1 represents missing label
        else:
            i2 = (' ').join(sFile[i][1:])   # If first token not opcode, it's a label
            i1 = sFile[i][0]                # i1 is the label (first token)
        listing[i] = '{:<3}'.format(i) + '{:<7}'.format(i1) + '{:<10}'.format(i2) # Create listing table entry
        if debugLevel > 1:                  # If debug  = 1, don't print source program
            print('{:<3}'.format(i),'{:<7}'.format(i1),'{:<10}'.format(i2))     # print: pc, label, opcode
    return()
def getLit(litV):                           # Extract a literal
    if litV[0] == '#': litV = litV[1:]      # Some systems prefix literal with '#
    if litV in symbolTab:                   # Look in sym tab and get value if there
        literal = symbolTab[litV]           # Read the symbol value as a string
        literal = int(literal)              # Convert string into integer
    elif litV[0] == '%': literal = int(litV[1:],2)          # If first char is %, convert to integer
    elif litV[0:2] == '0B':literal = int(litV[2:],2)        # If prefix 0B, convert binary to integer
    elif litV[0:2] == '0X':literal = int(litV[2:],16)       # If 0x, convert hex string to integer
    elif litV[0:1] == '$': literal = int(litV[1:],16)       # If $, convert hex string to integer
    elif litV[0] == '-': literal = (-int(litV[1:]))&0xFFFF     # Convert 2's complement to int
    elif litV.isnumeric(): literal = int(litV)              # If decimal string, convert to integer
    else: literal = 0                                       # Default value 0 (default value)
    return(literal)
def printStatus():                                          # Display machine status (registers, memory)
    text = '{:<27}'.format(listing[pcOld])                  # Format instruction for listing
    m = mem[0:8]                                            # Get the first 8 memory locations
    m1 = ' '.join('%04x' % b for b in m)                    # Format memory location's hex
    m2 = ' '.join('%04x' % b for b in r)                    # Format register's hex
    print(text, 'PC =', '{:>2}'.format(pcOld) , 'z =',z,'n =',n,'c =',c, m1, 'Registers ', m2)
    if debugLevel == 5:
        print('Stack =', ' '.join('%04x' % b for b in stack), 'Stack pointer =', sp)
    return()
print('TC1 CPU simulator 11 September 2022 ')               # Print the opening banner
debugLevel = input('Input debug level 1 - 5: ')             # Ask for debugging level
if debugLevel.isnumeric():                                  # If debug level is an integer, get it
    debugLevel = int(debugLevel)                            # Convert text to integer
else: debugLevel = 1                                        # Else, set default value to level 1
if debugLevel not in range (1,6): debugLevel = 1            # Ensure range 1 to 5
print()
global c,n,z                                                # Processor flags (global variables)
symbolTab = {'START':0}                                     # Create symbol table for labels + equates with dummy entry
c,n,z = 0,0,0                                               # Initialize flags: carry, negative, zero
sFile = ['']* 128                                           # sFile holds the source text
memP = [0] * 128                                            # Create program memory of 128 locations
mem = [0] * 128                                             # Create data memory of 128 locations
stack = [0] * 16                                            # Create a stack for return addresses
# codes is a dictionary of instructions {'mnemonic':(x.y)} where x is the instruction operand format, and y the opcode
codes = { \
 'STOP':(0,0), 'NOP' :(0,1), 'GET' :(8,2), 'RND' : (9,3), \
 'SWAP':(8,4), 'SEC' :(0,5), 'PRT' :(8,8), 'END!':(0,31), \
 'MOVE':(12,32),'LDRM':(9,33), 'LDRL':(9,34), 'LDRI':(13,35), \
 'STRM':(9,36), 'STRI':(13,37),'ADD' :(14,64),'ADDL':(13,65), \
 'SUB' :(14,66),'SUBL':(13,67),'MUL' :(14,68),'MULL':(13,69), \
 'DIV' :(14,70),'DIVL':(13,71),'MOD' :(14,72),'MODL':(13,73), \
 'AND' :(14,74),'ANDL':(13,75),'OR' :(14,76),'ORL' :(13,77), \
 'EOR' :(14,78),'EORL':(13,79),'NOT' :(8,80), 'INC' :(8,82), \
 'DEC' :(8,83), 'CMP' :(12,84),'CMPL':(9,85), 'LSL' :(12,88), \
 'LSLL':(9,89), 'LSR' :(12,90),'LSRL':(9,91), 'ROL' :(12,92), \
 'ROLL':(9,93), 'ROR' :(12,94),'RORL':(9,95), 'ADC':(14,102), \
 'SBC':(14,103),'BRA' :(1,96), 'BEQ' :(1,97), 'BNE' :(1,98), \
 'BMI' :(1,99), 'BSR' :(1,100),'RTS' :(0,101),'DBNE':(9,102), \
 'DBEQ':(9,103),'PUSH':(8,104),'PULL':(8,105) }
branchGroup = ['BRA', 'BEQ', 'BNE', 'BSR', 'RTS']               # Operations responsible for flow control
# Read the input source code text file and format it. This uses a default file and a user file if default is absent
prgN = 'C_2_test.txt'               # prgN = program name: default test file
try:                                                            # Check whether this file exists
    with open(prgN,'r') as prgN:                                # If it's there, open it and read it
        prgN = prgN.readlines()
except:                                                         # Call exception program if not there
    prgN = input('Enter source file name: ')                    # Request a filename (no extension needed)
    prgN = 'Chapter06/' + prgN + '.txt'       # Build filename
    with open(prgN,'r') as prgN:                                # Open user file
        prgN = prgN.readlines()                                 # Read it
for i in range (0,len(prgN)):                                   # Scan source prgN and copy it to sFile
    sFile[i] = prgN[i]                                          # Copy prgN line to sFile line
    if 'END!' in prgN[i]: break                                 # If END! found, then stop copying
 # Format source code
sFile = [i.split('@')[0] for i in sFile]                        # But first, remove comments     ###
for i in range(0,len(sFile)):                                   # Repeat: scan input file line by line
    sFile[i] = sFile[i].strip()                                 # Remove leading/trailing spaces and eol
    sFile[i] = sFile[i].replace(',',' ')                        # Allow use of commas or spaces
    sFile[i] = sFile[i].replace('[','')                         # Remove left bracket
    sFile[i] = sFile[i].replace(']','')                         # Remove right bracket and convert [R4] to R4
    while ' ' in sFile[i]:                                      # Remove multiple spaces
        sFile[i] = sFile[i].replace('  ',' ')
sFile = [i.upper() for i in sFile]                              # Convert to uppercase
sFile = [i.split(' ') for i in sFile if i != '']                # Split the tokens into list items
 # Remove assembler directives from source code
for i in range (0,len(sFile)):                                  # Deal with equates of the form PQR EQU 25
    if len(sFile[i]) > 2 and sFile[i][1] == 'EQU':              # If line is > 2 tokens and second is EQU
        symbolTab[sFile[i][0]] = sFile[i][2]                    # Put third token EQU in symbol table
sFile = [i for i in sFile if i.count('EQU') == 0]               # Remove all lines with 'EQU'
 # Debug: 1 none, 2 source, 3 symbol tab, 4 Decode i, 5 stack
listingP()                                                      # List the source code if debug level is 1
 # Look for labels and add to symbol table
for i in range(0,len(sFile)):                                   # Add branch addresses to symbol table
    if sFile[i][0] not in codes:                                # If first token not opcode, then it is a label
        symbolTab.update({sFile[i][0]:str(i)})                  # Add it to the symbol table
if debugLevel > 2:                                              # Display symbol table if debug level 2
    print('\nEquate and branch table\n')                        # Display the symbol table
    for x,y in symbolTab.items(): print('{:<8}'.format(x),y)    # Step through the symbol table dictionary
    print('\n')
 # Assemble source code in sFile
if debugLevel > 3: print('Decoded instructions')                # If debug level 4/5, print decoded ops
for pcA in range(0,len(sFile)):                                 # ASSEMBLY: pcA = prog counter in assembly
    opCode, label, literal, predicate = [], [], 0, []           # Initialize variables
    # Instruction = label + opcode + predicate
    rD, rS1, rS2 = 0, 0, 0                                      # Clear all register-select fields
    thisOp = sFile[pcA]                                         # Get current instruction, thisOPp, in text form
    # Instruction: label + opcode or opcode
    if thisOp[0] in codes: opCode = thisOp[0]                   # If token opcode, then get token
    else:                                                       # Otherwise, opcode is second token
        opCode = thisOp[1]                                      # Read the second token to get opcode
        label = sFile[i][0]                                     # Read the first token to get the label
    if (thisOp[0] in codes) and (len(thisOp) > 1):              # If first token opcode, rest is predicate
        predicate = thisOp[1:]                                  # Now get the predicate
    else:                                                       # Get predicate if the line has a label
        if len(thisOp) > 2: predicate = thisOp[2:]
    form = codes.get(opCode)                                    # Use opcode to read type (format)
    # Now check the bits of the format code
    if form[0] & 0b1000 == 0b1000:                              # Bit 4 selects destination register rD
        if predicate[0] in symbolTab:                           # Check if first token in symbol table
            rD = int(symbolTab[predicate[0]][1:])               # If it is, then get its value
        else: rD = int(predicate[0][1:])                        # If not label, get register from the predicate
    if form[0] & 0b0100 == 0b0100:                              # Bit 3 selects source register 1, rS1
        if predicate[1] in symbolTab:
            rS1 = int(symbolTab[predicate[1]][1:])
        else: rS1 = int(predicate[1][1:])
    if form[0] & 0b0010 == 0b0010:                              # Bit 2 of format selects register rS1
        if predicate[2] in symbolTab:
            rS2 = int(symbolTab[predicate[2]][1:])
        else: rS2 = int(predicate[2][1:])
    if form[0] & 0b0001 == 0b0001:                              # Bit 1 of format selects the literal field
        litV = predicate[-1]
        literal = getLit(litV)
        if debugLevel > 3:                                      # If debug level > 3, print decoded fields
            t0 = '%02d' % pcA                                   # Format instruction counter
            t1 = '{:<23}'.format(' '.join(thisOp))              # Format operation to 23 spaces
            t3 = '%04x' % literal                               # Format literal to 4-character hex
            t4 = '{:04b}'.format(form[0])                       # Format the 4-bit opcode format field
            print('pc =',t0,'Op =',t1,'literal',t3,'Dest reg =',rD,'rS1=',rS1,'rS2 =',rS2,'format =',t4) # Concatenate fields to create 32-bit opcode
            binCode = form[1]<<25|(rD)<<22|(rS1)<<19|(rS2)<<16|literal # Binary pattern
            memP[pcA] = binCode                                 # Store instruction in program memory
 # End of the assembly portion of the program
  # The code is executed here
r = [0] * 8                                                     # Define registers r[0] to r[7]
pc = 0                                                          # Set program counter to 0
run = 1                                                         # run = 1 during execution
sp = 16                                                         # Initialize the stack pointer (BSR/RTS)
goCount = 0                                                     # goCount executes n operations with no display
traceMode = 0                                                   # Set to 1 to execute n instructions without display
skipToBranch = 0                                                # Used when turning off tracing until a branch
silent = 0                                                      # silent = 1 to turn off single stepping
 # Executes instructions when run is 1
while run == 1:                                                 # Step through instructions: first, decode them!
    binCode = memP[pc]                                          # Read binary code of instruction
    pcOld = pc                                                  # pc in pcOld (for display purposes)
    pc = pc + 1                                                 # Increment the pc
    binOp = binCode >> 25                                       # Extract the 7-bit opcode as binOp
    rD = (binCode >> 22) & 7                                    # Extract the destination register, rD
    rS1 = (binCode >> 19) & 7                                   # Extract source register 1, rS1
    rS2 = (binCode >> 16) & 7                                   # Extract source register 2, rS2
    lit = binCode & 0xFFFF                                      # Extract the 16-bit literal
    op0 = r[rD]                                                 # Get contents of destination register
    op1 = r[rS1]                                                # Get contents of source register 1
    op2 = r[rS2]                                                # Get contents of source register 2
    # Instead of using the binary opcode to determine the instruction, I use the text opcode
# It makes the code more readable if I use 'ADD' rather than its opcode
    mnemonic=next(key for key,value in codes.items() if value[1]==binOp)
                                                                # Get mnemonic from dictionary
### INTERPRET INSTRUCTIONS # Examine the opcode and execute it
    if mnemonic == 'STOP': run = 0                              # STOP ends the simulation
    elif mnemonic == 'END!': run = 0                            # END! terminates reading source code and stops
    elif mnemonic == 'NOP': pass                                # NOP is a dummy instruction that does nothing
    elif mnemonic == 'GET':                                     # Reads integer from the keyboard
        printStatus()
        kbd = (input('Type integer '))                          # Get input
        kbd = getLit(kbd)                                       # Convert string to integer
        r[rD] = kbd                                             # Store in register
        continue
    elif mnemonic == 'RND': r[rD] = random.randint(0,lit)       # Generate random number
    elif mnemonic == 'SWAP': r[rD] = shift(0,1,r[rD],8)         # Swap bytes in a 16-bit word
    elif mnemonic == 'SEC': c = 1                               # Set carry flag
    elif mnemonic == 'LDRL': r[rD] = lit                        # LDRL R0,20 loads R0 with literal 20
    elif mnemonic == 'LDRM': r[rD] = mem[lit]                   # Load register with memory location (LDRM)
    elif mnemonic == 'LDRI': r[rD] = mem[op1 + lit]             # LDRI r1,[r2,4] memory location [r2]+4
    elif mnemonic == 'STRM': mem[lit] = r[rD]                   # STRM stores register in memory
    elif mnemonic == 'STRI': mem[op1 + lit] = r[rD]             # STRI stores rD at location [rS1]+L
    elif mnemonic == 'MOVE': r[rD] = op1                        # MOVE copies register rS1 to rD
    elif mnemonic == 'ADD': r[rD] = alu('ADD',op1, op2)         # Adds [r2] to [r3] and puts result in r1
    elif mnemonic == 'ADDL': r[rD] = alu('ADD',op1,lit)         # Adds 12 to [r2] and puts result in r1
    elif mnemonic == 'SUB': r[rD] = alu('SUB',op1,op2) #
    elif mnemonic == 'SUBL': r[rD] = alu('SUB',op1,lit)
    elif mnemonic == 'MUL': r[rD] = alu('MUL',op1,op2)
    elif mnemonic == 'MULL': r[rD] = alu('MUL',op1,lit)
    elif mnemonic == 'DIV': r[rD] = alu('DIV',op1,op2)          # Logical OR
    elif mnemonic == 'DIVL': r[rD] = alu('DIV',op1,lit)
    elif mnemonic == 'MOD': r[rD] = alu('MOD',op1,op2)          # Modulus
    elif mnemonic == 'MODL': r[rD] = alu('MOD',op1,lit)
    elif mnemonic == 'AND': r[rD] = alu('AND',op1,op2)          # Logical AND
    elif mnemonic == 'ANDL': r[rD] = alu('AND',op1,lit)
    elif mnemonic == 'OR': r[rD] = alu('OR', op1,op2)           # Logical OR
    elif mnemonic == 'ORL': r[rD] = alu('OR', op1,lit)
    elif mnemonic == 'EOR': r[rD] = alu('EOR',op1,op2)          # Exclusive OR
    elif mnemonic == 'EORL': r[rD] = alu('EOR',op1,lit)
    elif mnemonic == 'NOT': r[rD] = alu('NOT',op0,1)            # NOT r1 uses only one operand
    elif mnemonic == 'INC': r[rD] = alu('ADD',op0,1)
    elif mnemonic == 'DEC': r[rD] = alu('SUB',op0,1)
    elif mnemonic == 'CMP': rr = alu('SUB',op0,op1)             # rr is a dummy variable
    elif mnemonic == 'CMPL': rr = alu('SUB',op0,lit)
    elif mnemonic == 'ADC': r[rD] = alu('ADC',op1,op2)
    elif mnemonic == 'SBC': r[rD] = alu('SBC',op1,op2)
    elif mnemonic == 'LSL': r[rD] = shift(0,0,op0,op1)
    elif mnemonic == 'LSLL': r[rD] = shift(0,0,op0,lit)
    elif mnemonic == 'LSR': r[rD] = shift(1,0,op0,op1)
    elif mnemonic == 'LSRL': r[rD] = shift(1,0,op0,lit)
    elif mnemonic == 'ROL': r[rD] = shift(1,1,op0,op2)
    elif mnemonic == 'ROLL': r[rD] = shift(1,1,op0,lit)
    elif mnemonic == 'ROR': r[rD] = shift(0,1,op0,op2)
    elif mnemonic == 'RORL': r[rD] = shift(0,1,op0,lit)
    elif mnemonic == 'PRT': print('Reg',rD,'=', '%04x' % r[rD])
    elif mnemonic == 'BRA': pc = lit
    elif mnemonic == 'BEQ' and z == 1: pc = lit
    elif mnemonic == 'BNE' and z == 0: pc = lit
    elif mnemonic == 'BMI' and n == 1: pc = lit
    elif mnemonic == 'DBEQ':                                    # Decrement register and branch on zero
        r[rD] = r[rD] - 1
        if r[rD] != 0: pc = lit
    elif mnemonic == 'DBNE':                                    # Decrement register and branch on not zero
        r[rD] = alu('SUB',op0,1)                                # Note the use of the alu function
        if z == 0: pc = lit
    elif mnemonic == 'BSR':                                     # Stack-based operations. Branch to subroutine
        sp = sp - 1                                             # Pre-decrement stack pointer
        stack[sp] = pc                                          # Push the pc (return address)
        pc = lit                                                # Jump to target address
    elif mnemonic == 'RTS':                                     # Return from subroutine
        pc = stack[sp]                                          # Pull pc address of the stack
        sp = sp + 1                                             # Increment stack pointer
    elif mnemonic == 'PUSH':                                    # Push register to stack
        sp = sp - 1                                             # Move stack pointer up to make space
        stack[sp] = op0                                         # Push register in op on the stack
    elif mnemonic == 'PULL':                                    # Pull register off the stack
        r[rD] = stack[sp]                                       # Transfer stack value to register
        sp = sp + 1                                             # Move stack down
        if silent == 0:                                         # Read keyboard ONLY if not in silent mode
            x = input('>>>')                                    # Get keyboard input to continue
            if x == 'b': skipToBranch = 1                       # Set flag to execute to branch with no display
            if x.isnumeric():                                   # Is this a trace mode with a number of steps to skip?
                traceMode = 1                                   # If so, set traceMode
                goCount = getLit(x) + 1                         # Record the number of lines to skip printing
        if skipToBranch == 1:                                   # Are we in skip-to-branch mode?
            silent = 1                                          # If so, turn off printing status
            if mnemonic in branchGroup:                         # Have we reached a branch?
                silent = 0                                      # If branch, turn off silent mode and allow tracing
                skipToBranch = 0                                # Turn off skip-to-branch mode
        if traceMode == 1:                                      # If in silent mode (no display of data)
            silent = 1                                          # Set silent flag
            goCount = goCount - 1                               # Decrement silent mode count
            if goCount == 0:                                    # If we've reached zero, turn display on
                traceMode = 0                                   # Leave trace mode
                silent = 0                                      # Set silent flag back to zero (off)
        if silent == 0: printStatus()