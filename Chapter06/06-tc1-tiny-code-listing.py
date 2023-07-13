# Version 2023_07_12
# Simple CPU instruction interpreter. Direct instruction interpretation. 30 September 2022. V1.0
# Class 0: no operand                   NOP
# Class 1: literal                      BEQ  3
# Class 2: register                     INC  r1
# Class 3: register,literal             LDRL r1,5
# Class 4: register,register,           MOV  r1,r2
# Class 5: register,register,literal    ADDL r1,r2,5
# Class 6: register,register,register   ADD  r1,r2,r3
# Class 7: register,[register]          LDRI r1,[r2]
import sys                              # System library for exit
codes = {'NOP':[0],'STOP':[0],'END':[0],'ERR':[0], 'BEQ':[1],'BNE':[1],'BRA':[1],'INC':[2], \
         'DEC':[2],'NOT':[2], 'CMPL':[3],'LDRL':[3],'DBNE':[3],  'MOV':[4],'CMP':[4],       \
         'SUBL':[5],'ADDL':[5],'ANDL':[5], 'ADD':[6],'SUB':[6],'AND':[6],'OR':[6],          \
         'LDRI':[7],'STRI':[7]}   
reg1  = {'r0':0,   'r1':1,   'r2':2,  'r3':3, 'r4':4,   'r5':5,   'r6':6,  'r7':7}     # Registers
reg2  = {'[r0]':0, '[r1]':1, '[r2]':2,'[r3]':3, '[r4]':4, '[r5]':5, '[r6]':6,'[r7]':7} # Pointer registers
symTab = {}                                             # Symbol table
r = [0] * 8                                             # Register set
m = [0] * 8
prog = [] * 32                                          # Program memory

def equates():                                          # Process directives an delete
    global symTab, sFile
    for i in range (0,len(sFile)):                      # Deal with equates  
        tempLine = sFile[i].split()
        if len(tempLine) > 2 and tempLine[1] == "EQU":  # If line > 2 tokens and second EQU
            print('SYMB' , sFile[i])
            symTab[tempLine[0]] = tempLine[2]           # Put third token EQU in symbol table
    sFile = [ i for i in sFile if i.count("EQU") == 0]  # Remove all lines with "EQU"
    print('Symbol table ', symTab, '\n')    
    return()

def classDecode(predicate):
    lit,rD,rS1,rS2 = '',0,0,0  	# 
    if opClass in [1]:      lit =  predicate 
    if opClass in [2]:      rD  = reg1[predicate]
    if opClass in [3,4,5,6,7]:
        predicate = predicate.split(',')
        rD = reg1[predicate[0]]
    if opClass in [4,5,6]:  rS1 = reg1[predicate[1]]   # Get source reg 1 for classes 4, 5 and 6
    if opClass in [3,5]:    lit = (predicate[-1])      # Get literal for classes 3 and 5
    if opClass in [6]:      rS2 = reg1[predicate[2]]   # Get source reg 2 for class 6
    if opClass in [7]:      rS1 = reg2[predicate[1]]   # Get source pointer reg  for class 7
    return(lit,rD,rS1,rS2)

def testLine(tokens):      # Check there's a valid instruction in this line
    error = 1
    if len(tokens) == 1:
        if tokens[0] in codes: error = 0
    else:
        if (tokens[0] in codes) or (tokens[1] in codes): error = 0
    return(error)

def testIndex(): # test for reg or memory index out of range
    print('rD,rS1 =', rD,rS1, 'r[rS1] =', r[rS1], 'len(m)', len(m), 'mnemonic =', mnemonic)
    if rD > 7 or rS1 > 7 or rS2 > 7:
        print('Register number error')
        sys.exit() # Exit program on register error
    if mnemonic in ['LDRI', 'STRI']:
        if r[rS1] > len(m) - 1:
            print(' Memory index error')
            sys.exit()  # Exit program on pointer error
    return()

def getLit(litV):                                     # Extract a literal (convert formats)
    if litV == '': return(0)                          # Return zero if literal field empty
    if  litV in symTab:                               # Look in symbol table and get value if there 
        litV = symTab[litV]                           # Read the symbol value as a string
        lit = int(litV)                               # Convert string to integer
    elif  litV[0]    == "%": lit = int(litV[1:],2)    # If first symbol % convert binary  to int
    elif  litV[0:1]  == "$": lit = int(litV[1:],16)   # If first symbol $, convert hex to int
    elif  litV[0]    == "-":
        lit = (-int(litV[1:]))&0xFFFF                 # Deal with negative values
    elif  litV.isnumeric():  lit = int(litV)          # Convert decimal string to integer
    else:                    lit = 0                  # Default value 0 (if all else fails)
    return(lit)

prgN = 'NewIdeas_2.txt'   # prgN = program name:  test file
sFile = [ ]                                           # sFile source data
with open(prgN,'r') as prgN:                          # Open it and read it
    prgN = prgN.readlines()
for i in range(0,len(prgN)):                          # First level of text-processing
    prgN[i] = prgN[i].replace('\n','')                # Remove new line codes in source
    prgN[i] = " ".join(prgN[i].split())               # Remove multiple spaces 
    prgN[i] = prgN[i].strip()                         # First strip spaces
prgN = [i.split("@")[0] for i in prgN]                # Remove comment fields
while '' in prgN: prgN.remove('')                     # Remove blank lines
for i in range(0,len(prgN)):                          # Copy source to sFile: stop on END
    sFile.append(prgN[i])                             # Build new source text file sFile
    if 'END' in sFile[i]: break                       # Leave on 'END' ignore any more source text

for i in range(0,len(sFile)): print(sFile[i])
print()

equates()    # Deal with equates
for i in range(0,len(sFile)): print(sFile[i])
print()

for i in range(0,len(sFile)): # We need to compile list of labels
    label = '' # Give each line a default empty label
    predicate = ''   # Create default predicate (label + mnemonic + predicate)
    tokens = sFile[i].split(' ') # Split into separate label, mnemonic, predicate
 
    error = testLine(tokens) # Test for an invalid instruction
    if error == 1: # If error found
        print('Illegal instruction', tokens, 'at',i) 
        sys.exit() # Exit program

    numTokens = len(tokens) # Process this line
    if numTokens == 1: mnemonic = tokens[0]
    if numTokens > 1:
        if tokens[0][-1] == ':':
            symTab.update({tokens[0][0:-1]:i}) # Insert new value and line number 
            label = tokens[0][0:-1]
            mnemonic = tokens[1]
        else: mnemonic = tokens[0] 
        predicate = tokens[-1]
    opClass = codes.get(mnemonic)[0] # Use the mnemonic to read opClass from codes dictionary 
    thisLine = list((i,label,mnemonic,predicate,opClass))
    prog.append(thisLine)  # Program line + label + mnemonic + predicate + opClass
print('Symbol table ', symTab, '\n')  # Display symbol table for equates and line labels
 
    # instruction execution
run = 1
z = 0
pc = 0
while run == 1:
    thisOp = prog[pc]
    if thisOp[2] in ['STOP', 'END']: run = 0	# Terminate on STOP or END (comment on this)
    pcOld = pc
    pc = pc + 1
    mnemonic  = thisOp[2]
    predicate = thisOp[3]
    opClass   = thisOp[4]
    lit,rD,rS1,rS2 = classDecode(predicate)	
    lit = getLit(lit)

    if   mnemonic == 'NOP': pass
    elif mnemonic == 'BRA': pc = lit
    elif mnemonic == 'BEQ':
        if z == 1: pc = lit
    elif mnemonic == 'BNE':
        if z == 0: pc = lit        
    elif mnemonic == 'INC': r[rD] = r[rD] + 1
    elif mnemonic == 'DEC':
        z = 0
        r[rD] = r[rD] - 1
        if r[rD] == 0: z = 1
    elif mnemonic == 'NOT': r[rD] = (~r[rD])&0xFFFF	# Logical not
    elif mnemonic == 'CMPL':
        z = 0
        diff = r[rD] - lit
        if diff == 0: z = 1        
    elif mnemonic == 'LDRL': r[rD] = lit
    
    elif mnemonic == 'DBNE':
        r[rD] = r[rD] - 1
        if r[rD] != 0: pc = lit
    elif mnemonic == 'MOV':  r[rD] = r[rS1]   
    elif mnemonic == 'CMP':
        z = 0
        diff = r[rD] - r[rS1]
        if diff == 0: z = 1  
    elif mnemonic == 'ADDL': r[rD] = r[rS1] + lit 
    elif mnemonic == 'SUBL': r[rD] = r[rS1] - lit  
    elif mnemonic == 'ADD':  r[rD] = r[rS1] + r[rS2] 
    elif mnemonic == 'SUB':  r[rD] = r[rS1] - r[rS2]
    elif mnemonic == 'AND':  r[rD] = r[rS1] & r[rS2]
    elif mnemonic == 'OR':   r[rD] = r[rS1] | r[rS2]    
    elif mnemonic == 'LDRI':
        testIndex()
        r[rD] = m[r[rS1]]  
    elif mnemonic == 'STRI':
        testIndex()
        m[r[rS1]] = r[rD]
    
    regs = " ".join("%04x" % b for b in r)         # Format memory locations hex
    mem  = " ".join("%04x" % b for b in m)         # Format registers hex
    print('pc =','{:<3}'.format(pcOld),"{:<18}".format(sFile[pcOld]),'Regs =',regs,'Mem =',mem,'z =',z)