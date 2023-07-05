# Testing Python parsing # 22 Aug 2020 Version of 29 July 2021
import sys # System library used to exit program
codes = {'NOP':(0,0), 'STOP': (0,1),'BEQ':(1,4), 'INC':(8,2), \
'MOVE':(12,23), 'LDRL':(9,13), 'ADD':(14,12),'ADDL':(13,12)}
def syntaxTest(token): # Test the format of a register operand for validity (R0 to R7)
    if token[0] != 'R': return(4,0) # Fail on missing initial R. Return error 2
    if not token[1:].isnumeric(): return(5,0) # Fail on missing register number. Return error 3
    if int(token[1:]) > 7: return(6,0) # Fail on register number not in range 0-7. Return error 4
    return(0,int(token[1:])) # Success return with error code 0 and register number
def printError(error):
    if error != 0:
        if error == 1: print("Error 1: Non-valid operation")
        if error == 2: print("Error 2: Too few operands")
        if error == 3: print("Error 3: Too many operands")
        if error == 4: print("Error 4: Register operand error- no 'R'")
        if error == 5: print("Error 5: Register operand error - no valid num")
        if error == 6: print("Error 6: Register operand error - not in range")
run = 1
error = 0
while run == 1:
    if error != 0: printError(error) # if error not zero, print message
    x = input("\nEnter instruction >> ")# Type an instruction (for testing)
    x = x.upper() # Convert lowercase into uppercase
    x = x.replace(',',' ') # Replace comma with space to allow add r1,r2 or add r1 r2
    y = x.split(' ') # Split into tokens. y is the tokenized instruction
    if len(y) > 0: # z is the predicate (or null if no operands)
        z = y[1:]
    else: z = ''
    print("Inst =",y, 'First token',y[0])
    if y[0] not in codes: # Check for valid opcode
        error = 1 # Error 1: instruction not valid
        print("Illegal instruction", y[0])
        continue
    form = codes.get(y[0]) # Get the code's format information
    print('Format', form)
    if form[1] == 1: # Detect STOP, opcode value 1,and terminate
        print("\nProgram terminated on STOP") # Say "Goodbye"
        sys.exit() # Call OS function to leave
    opType = form[0]
    if opType == 0: totalOperands = 1
    elif opType == 8 or opType == 4 or opType == 1: totalOperands = 2
    elif opType == 12 or opType == 9: totalOperands = 3
    elif opType == 14 or opType == 13: totalOperands = 4
    totalTokens = len(y) # Compare tokens we have with those we need
    if totalTokens < totalOperands:
        error = 2 # Error 2: Too few operands
        continue
    if totalTokens > totalOperands:
        error = 3 # Error 3: Too many operands
        continue
    if opType & 0b1000 == 0b1000:
        rDname = y[1]
        error,q = syntaxTest(rDname)
        if error != 0: continue
    if opType & 0b0100 == 0b0100:
        rS1name = y[2]
        error,q = syntaxTest(rS1name)
        if error != 0: continue
    if opType & 0b0010 == 0b0010:
        rS2name = y[3]
        error,q = syntaxTest(rS2name)
        if error != 0: continue
    if opType & 0b0001 == 0b0001:
        if not y[-1].isnumeric():
            error == 7
            print("Error 7: Literal error")
    if error == 0:
        print("Instruction", x, "Total operands", totalOperands,"Predicate", z)