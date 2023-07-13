# Input error checking - using dictionaries Modified 30 July 2021
# Instruction dictionary 'mnemonic':(format, style, op_code, length)
# Style definition and example of the instruction format
# 0 NOP mnemonic only
# 1 BEQ L mnemonic + literal
# 2 INC R1 mnemonic + rD
# 3 MOVE R1,R2 mnemonic + rD1 + rS1
# 4 LDRL R1,L mnemonic + rD1 + literal
# 5 ADD R1 R2 R3 mnemonic + rD + rS1 + rS2
# 6 ADDL R1 R2 L mnemonic + rD + rS1 + literal
# 7 LDRI R1 (R2 L) mnemonic + rD + rS1 + literal (same as 6)
import sys # System library used to exit program
# Dictionary of instructions (format, style, op_code, length)
codes = {'NOP': (0b0000,0,0,1),'STOP':(0b0000,0,1,1),'BEQ': (0b0001,1,2,2), \
'INC': (0b1000,2,3,2),'MOVE':(0b1100,3,4,3),'LDRL':(0b1001,4,6,3), \
'LDRI':(0b1101,7,7,4),'ADD': (0b1110,5,8,4),'ADDL':(0b1101,6,9,4)}
regSet = {'R0':0,'R1':1,'R2':2,'R3':3,'R4':4,'R5':5,'R6':6,'R7':7} # Registers
def regTest(token): # Test register operand for R0 to R7
    if token in regSet: return (0) # Return with error 0 if legal name
    else: return (4) # Return with error 4 if illegal register name
def printError(error): # This function prints the error message
    if error != 0:
        if error == 1: print("Error 1: Non-valid operation")
        if error == 2: print("Error 2: Too few operands")
        if error == 3: print("Error 3: Too many operands")
        if error == 4: print("Error 4: Register name error")
        if error == 5: print("Error 5: Failure in pointer-based expression")
        if error == 6: print("Error 6: Invalid literal")
def litCheck(n): # Check for invalid literal format (this is just a demo)
    if n.isnumeric(): error = 0 # Decimal numeric OK
    elif n[0] == '-': error = 0 # Negative number OK
    elif n[0] == '%': error = 0 # Binary number OK
    elif n[0:2] == '0X': error = 0 # Hex number OK
    else: error = 6 # Anything else is an error
    return(error) # Return with error number
error = 0
while True: # Infinite loop
    if error != 0: printError(error)
    error = 0
    x = input(">> ").upper() # Read instruction and provide limited processing
    if len(x) == 0: continue # Ignore empty lines and continue
    x = x.replace(',',' ') # remove commas
    x = x.replace('(','') # remove (
    x = x.replace(')','') # remove )
    y = x.split(' ') # Create list of tokens (mnemonic + predicate)
    mnemonic = y[0] # Get the mnemonic (first token)
    if mnemonic not in codes: # Check for validity
        error = 1 # If not valid, set error code and drop out
        continue
    opData = codes.get(mnemonic) # Read the four parameters for this instruction
    opForm = opData[0] # opcode format (rDS,rS1,rS2,L)
    opStyle = opData[1] # Instruction style (0 to 7)
    opCode = opData[2] # Numeric opcode
    opLen = opData[3] # Length (total mnemonic + operands in range 1 to 4)
    if opLen > 1: predicate = y[1:] # Get predicate if this is one
    else: predicate = '' # If single token, return null
    print("Mnemonic =",mnemonic, "Predicate", predicate, \
    "Format =", bin(opForm),"Style =",opStyle,"Code =",opCode, \
    "Length =",opLen)
    if opCode == 1: # Used to terminate this program
        print("\nProgram ends on STOP")
        sys.exit()
    totalTokens = len(y)
    if totalTokens < opLen:
        error = 2 # Error 2: Too few operands
        continue
    if totalTokens > opLen:
        error = 3 # Error 3: Too many operands
        continue
    if opStyle == 0: # e.g., NOP or STOP so nothing else to do
        continue
    elif opStyle == 1: # e.g., BEQ 5 just check for literal
        literal = predicate[0]
        error = litCheck(literal)
        continue
    elif opStyle == 2: # e.g., INC r6 check for single register
        error = regTest(predicate[0])
        continue
    elif opStyle == 3: # e.g., MOVE r1,r2 check for two registers
        e1 = regTest(predicate[0])
        e2 = regTest(predicate[1])
        if e1 != 0 or e2 != 0:
            error = 4
        continue
    elif opStyle == 4: # e.g., LDRL r1,12 Check register then literal
        error = regTest(predicate[0])
        if error != 0: continue
        literal = predicate[1]
        error = litCheck(literal)
        continue
    elif opStyle == 5: # e.g., ADD r1,r2,r3 Check for three register names
        e1 = regTest(predicate[0])
        e2 = regTest(predicate[1])
        e3 = regTest(predicate[2])
        if e1 != 0 or e2 != 0 or e3 !=0:
            error = 4
        continue
    elif opStyle == 6: # e.g., ADDL R1,R2,4 Check for two registers and literal
        e1 = regTest(predicate[0])
        e2 = regTest(predicate[1])
        literal = predicate[2]
        e3 = litCheck(literal)
        if e1 != 0 or e2 != 0:
            error = 4
        if e1==0 and e2==0 and e3 !=0: # If registers are OK but not literal
            error = 6 # report literal error
        continue
    elif opStyle == 7: # e.g., LDRI r4,r0,23 or LDRI r4,(r0,23)
        e1 = regTest(predicate[0])
        e2 = regTest(predicate[1])
        literal = predicate[2]
        e3 = litCheck(literal)
        if e1 != 0 or e2 != 0:
            error = 4
        if e1==0 and e2==0 and e3 !=0: # If registers are OK but not literal
            error = 6 # report literal error
        continue