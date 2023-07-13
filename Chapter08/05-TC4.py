import re # Library for regular expressions for removing spaces  1
from random import  * # Random number library
import sys # Operating system call library
from datetime import date # Import date function 2

bPt = [] # Breakpoint table (labels and PC values)
bActive = 0

today = date.today() # Get today's date  2
print('Simulator', today, '\n')

deBug, trace, bActive  = 0, 0, 0  # Turn off debug, trace and breakpoint modes  3
x1 = input('D for debug >>> ') # Get command input
if x1.upper() == 'D': deBug = 1 # Turn on debug mode if D' or 'd' entered
x2 = input('T or B')  # Get command input 
x2 = x2.upper() # Convert to upper-case
if x2 == 'T': trace = 1 # Turn on trace mode if 'T' or 't' entered
elif x2 == 'B': # If 'B' or 'b' get breakpoints until 'Q' input BREAKPOINT ENTRY  4
    next = True
    bActive = 1 # Set breakpoint active mode
    while next == True: # Get breakpoint as either label or PC value
        y = input('Breakpoint ')
        y = y.upper()
        bPt.append(y) # Put breakpoint (upper-case) in table
        if y == 'Q': next = False
    if deBug == 1:  # Display breakpoint table if in debug mode
        print ('\nBreakpoint table')
        for i in range (0,len(bPt)): print(bPt[i])
        print()

print()



def memProc(src): # Memory processing  5
    global memPoint, memD # Deal with directives
    for i in range(len(src)):  # and remove directives from source code
        if src[i][0] == '.WORD': # Test for .word directive
            lit = get_lit(src[i],2) # Get the literal value
            sTab.update({src[i][1]:memPoint}) # Bind literal name to the memory address
            memD[memPoint] = lit # Store the literal in memory
            memPoint = memPoint + 1 # Move the memory pointer on one word location
        if src[i][0] == '.ASCII':  # .ASCII: test for an ASCII character
            sTab.update({src[i][1]:memPoint}) # Bind name to memory address
            character = ord(src[i][2]) # Convert character to numeric form
            memD[memPoint] = character # Store the character in memory as ASCII code
            memPoint = memPoint + 1 # Move the memory pointer on 
        if src[i][0] == '.DSW': # Test for .DSW to reserve locations in memory
            sTab.update({src[i][1]:memPoint}) # Save name in table and bind to memory address
            memPoint = memPoint + int(src[i][2]) # Move memory pointer by space required
    src = [i  for i in src if i[0] != '.WORD'] # Remove .word from source
    src = [i  for i in src if i[0] != '.ASCII'] # Remove .ASCII from source
    src = [i  for i in src if i[0] != '.DSW'] # Remove .DSW from source
    memD[memPoint] = 'END' # Add terminator to data memory (for display)
    return(src)

def get_reg(pred,p):  # Extract a register number from predicate
    reg = pred[p] # Read token p is the predicate
    if reg in sTab: # Check if this is a symbolic name
        reg = sTab.get(reg) # If symbolic name read it from symbol table
        reg = int(reg[1:]) # Convert register name into number
    else: reg = int(reg[1:]) # If not symbolic name convert name into number
    return(reg) # Otherwise return the register number

def get_lit(pred,p): # Extract literal from place p in predicate
    global sTab # We need the symbol table
    lit = pred[p] # Read the literal from the predicate
    if lit in sTab: # If literal is in symbol table, look it up
        lit = int(sTab.get(lit))
    else: # Convert literal format to an integer
        if   lit[0]   == "%": lit = int(pred[-1][1:],2) # If prefix % then binary
        elif lit[0:2] == "0X": lit = int(pred[-1][2:],16) # If prefix 0X then hexadecimal
        elif lit[0].isnumeric(): lit = int(pred[-1]) # If numeric get it
        elif lit[0].isalpha(): lit = ord(lit) # Convert ASCII character to integer
        elif lit[0:2] == "0X": lit = int(pred[-1][2:],16) # If prefix 0X then hexadecimal 
        else:  lit = 0 # Default (error) value 0
    return(lit)

def display():  # Print the state after each instruction
    thisOp = ' '.join(src[pcOld]) # Join this op-code's tokens into a string
    a =[format(x,'04x') for x in r] # Format registers into hex strings
    b = (' ').join(a) # Join the hex strings with a space 
    f1 = f'{pcOld:<4}' # Format the PC as a string
    f2 = f'{thisOp:<18}'  # Format the instruction to fixed width
    print('PC =',f1,'Reg =',b,'Z =',z,'N =',n,'C =',c,f2) # Print the data
    return()

def alu(a,b,f): # ALU for addition/subtraction and flag calculation  6
# a and b are the numbers to add/subtract and f the function
    global z,c,n # Make flags global
    z,c,n = 0,0,0 # Clear flags initially
    if f == 1: s = a + b # f = 1 for add
    if f == 2: s = a - b # f = 2 for subtract
    s = s & 0x1FFFF # Constrain result to 17 bits
    if s > 0xFFFF: c = 1 # Carry set if 17th bit 1
    if 0x8000 & s == 0x8000 : n = 1 # Bit 15 set to 1 for negative 
    if s & 0xFFFF == 0: z = 1 # Zero flag set to 1 if bits 0-15 all 0  
    s = 0xFFFF & s  # Ensure 16-bit result
    return(s)

codes = {"STOP":(0,0),"NOP":(0,1),"RND":(1,4),"BRA":(2,5),"BEQ":(2,6),"BNE":(2,7),"MOV":(3,8),"LDRM":(4,9), \
         "LDRL":(4,10),"LDRI":(7,11),"LDRI+":(7,12),"STRM":(4,13),"STRI":(7,14),"STRI+":(7,15),"ADD":(5,16),\
         "ADDL":(6,17),"SUB":(5,18),"SUBL":(6,19),"AND":(5,20),"ANDL":(6,21),"OR":(5,22),"ORL":(6,23),      \
         "EOR":(5,24),"EORL":(6,25),"CMP":(3,26),"CMPL":(4,27),"LSL":(3,28),"LSR":(3,29),"ROL":(3,30),      \
         "ROR": (3,31), "BSR":(2,32),"RTS":(0,33),"PUSH":(1,34),"POP":(1,35),"BL":(2,36),"RL":(0,37),       \
         "INC":(1,48), "DEC":(1,49), "PRT":(1,3), "BHS": (2,71)}

# Style Code Format (a,b) where a is the instruction style and b is the actual op-code
# 0     Zero operand STOP
# 1     Destination register operand INC  R0
# 2     Literal operand BEQ  5
# 3     Two registers Rd, Rs1 MOV  R2,R4
# 4     Register and literal Rd L LDR  R6,23
# 5     Three registers Rd, Rs1 Rs2 ADD  R1,R2,R3
# 6     Two registers, literal Rs, Rd1, L ADDL R1,R2,9
# 7     Indexed, Rd, Rs, L LDRI R4,(R6,8)
# 8     UNDEFINED

testFile = 'TC4_test.txt' # Source filename on my computer 
with open(testFile) as myFile: # Open source file with assembly language program
    lines = myFile.readlines() # Read the program into lines
myFile.close() # Close the source file (not actually needed)
lines = [i[0:-1]  for i in lines ] # Remove the /n newline from each line of the source code
src = lines # Copy lines to variable scr (i.e., source code)

if deBug == 1:  # If in debug mode print the source file  3
    print('Debug mode: original source file')
    for i in range(0,len(src)): print(i, src[i]) # Listing file

for i in range(0,len(src)): # Remove comments from source
   src[i] = src[i].split('@',1)[0] # Split line on first occurrence of @ and keep first item

src = [i.strip(" ") for i in src ] # Remove leading  and trailing spaces
src = [i for i in src if i != ""] # Remove blank lines
src = [i.upper() for i in src] # Convert lower- to upper-case
src = [re.sub(' +', ' ',i) for i in src ] # Remove multiple spaces  1
src = [i.replace(', ',' ') for i in src] # Replace commas space by single space
src = [i.replace('[','') for i in src] # Remove [ in register indirect mode
src = [i.replace(']','') for i in src] # Remove [
src = [i.replace(',',' ') for i in src] # Replace commas by spaces
src = [i for i in src if i[0] != "@"] # Remove lines with just a comment
src = [i.split(' ')  for i in src] # Tokenize


if deBug == 1: # If in debug mode print the source file
    print('\nProcessed source file\n')
    [print(i) for i in src]
# Initialize key variables
# memP program memory, memD data memory
sTab = {} # Setup symbol table for labels and equates 
memP = [0] * 64 # Define program memory
memD = [0] * 64 # Define data memory
memPoint = 0  # memPoint points to next free  location

[sTab.update({i[1]:i[2]}) for i in src if i[0] == '.EQU'] # Scan source file: Deal with equates

src = [i  for i in src if i[0] != '.EQU'] # Remove equates from source
src = memProc(src) # Deal with memory related directives

for i in range (0,len(src)): # Insert labels in symbol table
    if src[i][0][-1]== ':': sTab.update({src[i][0][0:-1]:i}) # Remove the colon from labels

print('\nSymbol table\n')
for x,y in sTab.items(): print("{:<8}".format(x),y) # Display symbol table

if deBug == 1:
    print("\nListing with assembly directives removed\n")
    for i in range(0,len(src)): # Step through each line of code
        z = '' # Create empty string for non-labels
        if src[i][0][-1] != ':': z = '        ' # Create 8-char empty first spaced
        for j in range(0,len(src[i])): # Scan all tokens of instruction 
            y = src[i][j] # Get a token
            y = y.ljust(8) # Pad it  with spaces to 8 chars width
            z = z + y # Add it to the line
        print(str(i).ljust(3),z) # Print line number and  instruction
 
if deBug == 1:  # DISPLAY data memory for debugging
    print("\nData memory")
    [print(memD[i]) for i in range(0,memPoint+1)] # print pre-loaded data in memory
    print()
 
#### MAIN ASSEMBLY LOOP 
if deBug == 1: print('Assembled instruction\n') # If in debug mode print heading  4
pc = 0
for pc in range(0,len(src)):
    rD,rS1,rS2,lit = 0,0,0,0 # Initialize operand fields
    if src[pc][0][-1] != ':': # Extract mnemonic and predicate
        mnem  = src[pc][0]
        if len(src[pc]) > 1: pred = src[pc][1:] # Check for single mnemonic only
        else: pred = '[]' # If only mnemonic with no predicate
    else:
        mnem  = src[pc][1] # For lines with a label
        if len(src[pc]) > 2: pred = src[pc][2:] # Get predicate if one exists 
        else: pred = '[]'  # If only mnemonic, no pred
    if mnem in codes:   
       opFormat = codes.get(mnem) # Read of op-code format of mnemonic
    else: print('Illegal opcode ERROR, mnem') # Display error message  

# OP-CODE FORMATS  
    if opFormat[0] == 1: # Type 1 single register rD: inc r0
        rD = get_reg(pred,0) #
    if opFormat[0] == 2: # Type 2 literal operand: BEQ 24
        lit = get_lit(pred,-1)
    if opFormat[0] == 3: # Type 3 two registers dD, rS1: MOV r3,R0
        rD  = get_reg(pred,0) 
        rS1 = get_reg(pred,1) 
    if opFormat[0] == 4: # Type 4 register and literal Rd, lit: LDRL R1,34
        rD  = get_reg(pred,0)
        lit = get_lit(pred,-1)
    if opFormat[0] == 5: # Type 5 three registers Rd, Rs1 Rs2: ADD  R1,R2,R3
        rD  = get_reg(pred,0) 
        rS1 = get_reg(pred,1) 
        rS2 = get_reg(pred,2) 
    if opFormat[0] == 6: # Type 6 two registers and lit Rd, Rs1 lit: ADD  R1,R2,lit
        rD  = get_reg(pred,0) 
        rS1 = get_reg(pred,1) 
        lit = get_lit(pred,-1) 
    if opFormat[0] == 7: # Type 7 two registers and lit Rd, Rs1 lit: LDR  R1,(R2,lit)
        rD  = get_reg(pred,0)
        pred[1] = pred[1].replace("(","") # Remove braces
        pred[2] = pred[2].replace(")","") 
        rS1 = get_reg(pred,1) 
        lit = get_lit(pred,-1) 
    if opFormat[0] == 8: # Type 8 UNDEFINED
        pass
# Assemble the instruction to create binary form
    opCd     = opFormat[1] << 25 # Move op-code to left-most 7 bits
    rDs      = rD          << 22 # Move destination reg into place
    rS1s     = rS1         << 19 # Move source reg 1 in place
    rS2s     = rS2         << 16 # Move source reg 2 in place
    binCode=opCd|rDs|rS1s|rS2s|lit # Assemble the instruction by combining fields
    memP[pc] = binCode  # Store 32-bit binary code in program memory

    if deBug == 1: # If in debug mode show the binary output of the assembler
        a1 = f'{pc:<4}' # Format for the PC (4 chars wide) 
        a2 = format(binCode,'032b') # Create 32-bit binary string for op-code
        a3 = f'{mnem:<5}' # Format the mnemonic to 5 places
        a4 = f'{rD:<4}' # Format source register to 4 places
        a5 = f'{rS1:<4}' 
        a6 = f'{rS2:<4}'
        a7 = f'{lit:<6}' 
        print('PC =',a1,a2,a3,a4,a5,a6,a7,src[pc])# Assemble items and print them
# CODE EXECUTE LOOP
print('\nExecute code\n')
r = [0] * 8  # Register set
stack = [0] * 16  # stack with 16 locations  7 

sp = 16 # stack pointer initialize to bottom of stack + 1
lr = 0 # link register initialize to 0
run = 1 # run = 1 to execute code
pc = 0 # Initialize program counter
z,c,n = 0,0,0 # Clear flag bits. Only z-bit is used 

while run == 1: # Main loop
   
    instN = memP[pc] # Read instruction
    pcOld = pc # Remember the pc (for printing)
    pc = pc + 1 # Point to the next instruction
    op  = (instN >> 25) & 0b1111111 # Extract the op-code (7 most-significant bits)
    rD  = (instN >> 22) & 0b111  # Extract the destination register
    rS1 = (instN >> 19) & 0b111 # Extract source register 1
    rS2 = (instN >> 16) & 0b111  # Extract source register 2    
    lit = (instN      ) & 0xFFFF # Extract literal in lest-significant 16 bits
    rDc = r[rD] # Read destination register contents)
    rS1c = r[rS1] # Read source register 1 contents
    rS2c = r[rS2] # Read source register 2 contents
# Instruction execution   
    if op == 0b0000001: # NOP   Nothing to see here ... it's NOP so just drop out
        pass
    if op == 0b0000100: # RND # RND r0 generates random number in r0
       r[rD] = randint(0,0xFFFF)
    if op == 0b0000101: # BRA # Branch to the label or literal. Absolute address
        pc = lit
    if op == 0b0000110: # BEQ   # Branch on zero flag     
        if z == 1: pc = lit 
    if op == 0b0000111: # BNE   # Branch on not zero
        if z != 1: pc = lit
    if op == 0b1000111:  # BHS   # Branch on unsigned higher or same  8
        if c == 0 : pc = lit
    if op == 0b0001000: # MOV   # Copy one register to another
        r[rD] = rS1c
    if op == 0b0001001: # LDRM  # Load register from address in memory
        r[rD] = memD[lit]
    if op == 0b0001010: # LDRL  # Load register with a literal
        r[rD] = lit
    if op == 0b0001011:  # LDRI  # Load register indirect with offset; LDRI r1,[r2,4]
        r[rD] = memD[rS1c + lit]
    if op == 0b0001100: # LDRI+ # Auto-indexed. Increment pointer after use  9
        r[rD] = memD[rS1c + lit]
        r[rS1] = rS1c + 1
    if op == 0b0001101: # STRM  # 
        memD[lit] = rDc
    if op == 0b0001110: # STRI  # Store register indexed
        memD[rS1c + lit] = rDc
    if op == 0b0001111: # STRI+ # Auto indexed
        memD[rS1c + lit] = rDc
        r[rS1] = rS1c + 1        
    if op == 0b0010000: # ADD   # r1 = r2 + r3
        r[rD] = alu(rS1c,rS2c,1)
    if op == 0b0010001: # ADDL  # r1 = r2 + literal
        r[rD] = alu(rS1c,lit,1)
    if op == 0b0010010: # SUB
        r[rD] = alu(rS1c,rS2c,2) 
    if op == 0b0010011: # SUBL
        r[rD] = alu(rS1c,lit,2)
    if op == 0b0010100:  # AND
        r[rD] = (rS1c & rS2c) & 0xFFFF
    if op == 0b0010101: # ANDL
        r[rD] = (rS1c & lit) & 0xFFFF
    if op == 0b0010110: # OR
        r[rD] = (rS1c | rS2c) & 0xFFFF
    if op == 0b0010111: # ORL
        r[rD] = (rS1c | lit) & 0xFFFF
    if op == 0b0011000: # EOR (XOR)
        r[rD] = (rS1c ^ rS2c) & 0xFFFF
    if op == 0b0011001:  # EORL (XORL)
        r[rD] = (rS1c ^ lit) & 0xFFFF
    if op == 0b0011010: # CMP
        diff = alu(rDc,fS1c,2)
    if op == 0b0011011: # CMPL
        diff = alu(rDc,lit,2)
    if op == 0b0011100: # LSL
        r[rD] = (rS1c << 1) & 0xFFFF
    if op == 0b0011101: # LSR  
        r[rD] = (rS1c >> 1) & 0xFFFF 
    if op == 0b0011110: # ROL  
        bitLost = (rS1c & 0x8000) >> 16
        rS1c = (rS1c << 1) & 0xFFFF
        r[rD] = rS1c | bitLost
    if op == 0b0011111: # ROR  
        bitLost = (rS1c & 0x0001)
        rS1c = (rS1c >> 1) & 0xFFFF
        r[rD] = rS1c | (bitLost << 16)  
    if op == 0b0100000: # BSR
        sp = sp - 1
        stack[sp] = pc
        pc = lit
    if op == 0b0100001: # RTS
        pc = stack[sp]
        sp = sp + 1
    if op == 0b0100010:  # PUSH 7
        sp = sp - 1
        stack[sp] = rDc
    if op == 0b0100011: # POP 7

        r[rD] = stack[sp]
        sp = sp + 1
    if op == 0b0100100: # BL branch with link  10
        lr = pc
        pc = lit
    if op == 0b0100101: # RL return from link
        pc = lr
    if op == 0b0110000: # INC
        r[rD] = alu(rDc,1,1)
    if op == 0b0110001: # DEC
        r[rD] = alu(rDc,1,2)
    if op == 0b0000011: # PRT r0 displays the ASCII character in register r0  See 11
        character = chr(r[rD])
        print(character)
    if op == 0b0000000:                      # STOP
        run = 0
# END OF CODE EXECUTION Deal with display 

    if bActive ==1: # Are breakpoints active?
        if src[pcOld][0] in bPt: # If the current label or mnemonic is in the table
            display() # display the data
        if str(pcOld) in bPt: # If the current PC (i.e., pcOld) is in the table display
            display()
    if trace == 1:  # If in trace mode, display registers
        x = input('<< ') # Wait for keyboard entry (any key will do)
        display() # then display current operation
    elif bActive != 1: display() # If not trace and not breakpoints, display registers
    if run == 0: # Test for end of program  12
        print('End of program') # If end, say 'Goodbye'
        sys.exit() # and return