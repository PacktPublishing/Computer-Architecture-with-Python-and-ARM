# @ Test fetch/execute cycle
#0 LDRL r0 0 @ Load register r0 with 0 (the sum)
#1 LDRL r1 0 @ Load register r1 with 0 (the counter)
#2 Loop ADDL r1 r1 1 @ REPEAT Increment counter in r1. Loop address = 2
#3 ADD r0 r0 r1 @ Add the count to the sum in r0
#4 CMPL r1 10 @ Compare the count with 10
#5 BNE Loop @ Branch back to Loop until all numbers added (BNE 2)
#6 STOP @ Terminate execution
prog=['LDRL r0 0','LDRL r1 0','ADDL r1 r1 1','ADD r0 r0 r1','CMPL r1 10','BNE2','STOP']
r = [0] * 8                         # Initialize r[0], r[1], ... r[7] and initialize to 0
z = 0                               # z = zero flag: if a compare result is 0, z = 1
run = True                          # run flag True to execute
pc = 0                              # pc = program counter, initially 0
while run == True:                  # The fetch/execute loop.
 inst = prog[pc]                    # Read next instruction from memory
 oldPC = pc                         # Save the old value of the PC (
 pc = pc + 1                        # Point to the next instruction
 inst = inst.split(' ')             # Split divides the instruction into tokens (separate fields)
 if inst[0] == 'ADD':               # Test for ADD rd,rS1,rS2 instruction
    rd = int(inst[1][1])            # Get dest, source 1 and source 2
    rS1 = int(inst[2][1])
    rS2 = int(inst[3][1])
    r[rd] = r[rS1] + r[rS2]         # Add reg 1 and 2 sum in desti reg
 elif inst[0] == 'ADDL':            # Test for ADD literal instruction, ADDL
    rd = int(inst[1][1])            # If found get destination register
    rS1 = int(inst[2][1])           # Now get source 1 register
    literal = int(inst[3])          # Now get the literal
    r[rd] = r[rS1] + literal        # Add reg 1 and literal
 elif inst[0] == 'BNE':             # Test for branch on not zero
    if z == 0:                      # if z is 0 (last register not zero)
        pc = int(inst[1])           # get branch destination from operation
 elif inst[0] == 'CMPL':            # Test register for equality with a literal
    z = 0                           # set z flag to 0 (assume not equal)
    rVal = r[int(inst[1][1])]       # register value
    intVal = int(inst[2])           # literal value
    if rVal == intVal: z = 1        # If reg value =s literal, z=1
 elif inst[0] == 'LDRL':            # Test for load literal into register operation
    rd = int(inst[1][1])            # Get destination register
    data = int(inst[2])             # Test literal value
    r[rd] = data                    # Store literal in destination register
 elif inst[0] == 'STOP':            # Test for STOP instruction
    run = False                     # If STOP found then set run flag to False
    print('End of program reached')
 else:                              # If we end up here, not a valid instruction
    run = False                     # So set run flag to False and stop.
    print('Error: illegal instruction ',inst)
 print('PC = ',oldPC,'r0 = ',r[0],'r1 = ',r[1],'z = ',z) # Print results
# Repeat loop until Run = False