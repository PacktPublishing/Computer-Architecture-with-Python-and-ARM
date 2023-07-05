regSet = {'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7}
def regTest(tokNam,token): # Test format of a register operand for validity (R0 to R7)
    if token in regSet: # Is it in the register set?
        return (0,regSet.get(token)) # If it's there, return 0 and token value
    else: # If not there, return error code 4 and the token's name
        print("Error in register ",tokNam)
        return (4,0)