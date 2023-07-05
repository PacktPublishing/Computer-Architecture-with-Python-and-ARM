# This function simulates an 8-bit ALU and provides 16 operations
# It is called by alu(op,a,b,cIn,display). Op defines the ALU function
# a,b and cIn are the two inputs and the carry in
# If display is 1, the function prints all input and output on the terminal
# Return values: q, z, n, v, cOut) q is the result
def alu(op,a,b,cIn,display):
    allOps = {0:'clr', 1:'add',2:'sub',3:'mul',4:'div',\
    5:'and',6:'or',7:'not', 8:'eor', 9:'lsl',10:'lsr',\
    11:'adc',12:'sbc',13:'min',14:'max',15:'mod'}
    a, b = a & 0xFF, b & 0xFF # Ensure the input is 8 bits
    cOut,z,n,v = 0,0,0,0 # Clear all status flags
    if op == 0: q = 0 # Code 0000 clear
    elif op == 1: q = a + b # Code 0001 add
    elif op == 2: q = a - b # Code 0010 subtract
    elif op == 3: q = a * b # Code 0011 multiply
    elif op == 4: q = a // b # Code 0100 divide
    elif op == 5: q = a & b # Code 0100 bitwise AND
    elif op == 6: q = a | b # Code 0100 bitwise OR
    elif op == 7: q = ~a # Code 0111 bitwise negate (logical complement)
    elif op == 8: q = a ^ b # Code 0100 bitwise EOR
    elif op == 9: q = a << b # Code 0100 bitwise logical shift left b places
    elif op == 10: q = a >> b # Code 0100 bitwise logical shift right b places
    elif op == 11: q = a + b + cIn # Code 0100 add with carry in
    elif op == 12: q = a - b - cIn # Code 0100 subtract with borrow in
    elif op == 13: # Code 1101 q = minimum(a,b)
        if a > b: q = b
        else: q = a
    elif op == 14: # Code 1110 q = maximum(a,b)
        if a > b: q = a # Note: in unsigned terms
        else: q = b
    elif op == 15: # Code 1111 q = mod(a)
        if a > 0b01111111: q = (~a+1)&0xFF # if a is negative q = -a (2s comp)
        else: q = a # if a is positive q = a
# Prepare to exit: Setup flags
    cOut = (q&0x100)>>8 # Carry out is bit 8
    q = q & 0xFF # Constrain result to 8 bits
    n = (q & 0x80)>>7 # AND q with 10000000 and shift right 7 times
    if q == 0: z = 1 # Set z bit if result zero
    p1 = ( (a&0x80)>>7)& ((b&0x80)>>7)&~((q&0x80)>>7)
    p2 = (~(a&0x80)>>7)&~((b&0x80)>>7)& ((q&0x80)>>7)
    if p1 | p2 == True: v = 1 # Calculate v-bit (overflow)
    if display == 1: # Display parameters and results
        a,b = a&0xFF, b&0xFF # Force both inputs to 8 bits
        print('Op =',allOps[op],'Decimals: a =',a,' b =',b,'cIn =',cIn,'Result =',q)
        print('Flags: Z =',z, 'N =',n, 'V =',v, 'C =',cOut)
        print('Binaries A =',format(a,'08b'), 'B =',format(b,'08b'), 'Carry in =',
                  format(cIn,'01b'), 'Result = ',format(q,'08b'))
        print ()
    return (q, z, n, v, cOut) # Return c (result), and flags as a tuple
#### MAIN BODY
def literal(lit):
    if lit.isnumeric(): lit = int(lit) # If decimal convert to integer
    elif lit[0] == '%': lit = int(lit[1:],2) # If binary string convert to int
    elif lit[0:1]== '$': lit = int(lit[1:],16) # If hex string convert to int
    elif lit[0] == '-': lit = -int(lit[1:])&0xFF # If negative convert to signed int
    return(lit)
opsRev = {'clr':0,'add':1,'sub':2,'mul':3,'div':4,\
'and':5,'or':6,'not':7,'eor':8,'lsl':9,'lsr':10,'adc':11,\
'sbc':12,'min':13,'max':14,'mod':15}
x,y,op1,op2,cIn = 0,0,0,0,0 # Dummy value prior to test in while loop
while True:
    x = input('Enter operation and values ')
    if x == '': break # Exit on return
    y = x.split() # Divide     into tokens
    print (y) # Show the input
    fun = opsRev[y[0]] # Convert function name into number
    if len(y) > 1: op1 = literal(y[1]) # One parameter
    if len(y) > 2: op2 = literal(y[2]) # Two parameters
    if len(y) > 3: cIn = literal(y[3]) # Three parameters
    q, z, n, v, cOut = alu(fun,op1,op2,cIn,1) # Call the ALU function
    # Repeat until return entered