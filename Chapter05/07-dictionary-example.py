regs = {'r0':0, 'r1':1, 'r2':2, 'r3':3, 'r4':4}                 # Register name-to-number translation
symTab = {'start':0,'time':24,'stackP':'sp','next':0xF2}        # Symbol table converts symbolic name to value
x0 = 'add r1,r2,r4'                                             # An example of an instruction in text form
x1 = x0.split(' ')                                              # Split instruction into op-code and predicate
x2 = x1[1].split(',')                                           # Split the predicate into tokens
x3 = x2[0]                                                      # Get the first token of x2
if x3 in regs:                                                  # Is this a valid register?
    x4 = regs.get(x3)                                              # Use get() to read its value
    print ('x0 = ',x0, '\nx1 = ',x1, '\nx2 = ',x2, '\nx3 = ',x3, '\nx4 = ',x4)
y0 = 'beq next'                                                 # Another example: instruction with a label
y1 = y0.split(' ')                                              # Split into op-code and predicate on the space
y2 = y1[1]                                                      # Read the predicate (i.e.,'next')
y3 = symTab.get(y2)                                             # Get its value from the symbol table (i.e., 0xF2)
print('beq ',y3)                                                # Print the instruction with the actual address
z = symTab.get('beq next'.split(' ')[1])                        # We've done it all in one line. Not so easy to follow.
print('beq ',z)
print('Symbol table ', symTab)                                  # Print the symbol table using a print
symTab['nextOne'] = 1234                                        # This is how we add a new key and value
print('Symbol table ', symTab)                                  # Here's the augmented symbol table
opCode = {'add':('Arith',0b0001,3),'ldr':('Move',0b1100,2),'nop':('Miscellaneous',1111,0)}
 # New directory. Each key has three values in a tuple
thisInst = 'ldr'                                                # Let's look up an instruction
if thisInst in opCode:                                          # First test if it's valid and in the dictionary
    if thisInst == 'ldr':                                       # If it is:
        instClass = opCode.get('ldr')[0]                        # Get first element of the instruction
        binaryVal = opCode.get('ldr')[1]                        # Get the second element
        operands = opCode.get('ldr')[2]                         # Get the third element
print('\nFor opCode: ',thisInst, '\nClass = ', instClass, '\nBinary code = ', bin(binaryVal), '\nNumber of operands = ',operands)
print('\nThis is how to print a directory')                     # Now print a formatted dictionary (key and value on each line)
for key,value in opCode.items():
    print(key, ':', value)
print()
for i,j in opCode.items():                                      # Note that key and value can be any two variables
    print(i, ':', j)
theKeys = opCode.keys()                                         # The function .keys() returns the keys in a dictionary
print('The keys are: ',theKeys)
test = {'a':0,'b':0,'c':0,'d':0}                                # A new directory. The values are just integers
test['a'] = test['a'] + 1                                       # You can change a value! Use the key to locate it
test['d'] = test['d'] + 7
test1 = {'e':0, 'f':0}                                          # Here's a second dictionary
test.update(test1)                                              # Append it to test using .update()
print('Updated dictionary test is: ',test)                      # Not convinced? Here it is then.