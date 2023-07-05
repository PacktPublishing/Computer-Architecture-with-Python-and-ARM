# Simple program to test a branch instruction
mem = [0] * 12                              # Setup a 12-location memory
pc = 0                                      # Initialize program counter to 0
mem[0] = 0b000100001001                     # First instruction loads r0 with 9 (i.e., 1001)
mem[1] = 0b001100000111                     # Second instruction subtracts mem[7] from r0
mem[2] = 0b010000000110                     # Third instruction is BEQ 0 (branch on zero to 6)
mem[3] = 0b111100000000                     # Fourth instruction is stop
mem[6] = 0b111100000000                     # Seventh instruction is stop
mem[7] = 9                                  # Initial data in location 7 is 9
                                            # Fetch returns op-code and address
def fetch(memory):                          # This function, fetch, gets the instruction from memory
    global pc                               # Declare pc as global because we modify it in the function
    ir = memory[pc]                         # Read the instruction from memory
    pc = pc + 1                             # Now point to the next instruction
    return(ir>>8, ir&0xFF)                  # Return the opcode and address
z = 0                                                           # Clear z bit initially
run = 1                                                         # run = 1 to continue
while run == 1:                                                 # Main loop REPEAT until stop found
    pcOld = pc                                                  # Save current pc for display
    opCode, address = fetch(mem)                                # Perform fetch to get op-code
    if opCode == 0b1111: run = 0                                # Test for stop
    elif opCode == 0b0001: r0 = address                         # Test for load literal
    elif opCode == 0b0010: r0 = r0 + mem[address]               # Test for add
    elif opCode == 0b0011:                                      # Test for subtract
        r0 = r0 - mem[address]                                  # Do subtraction
        if r0 == 0: z = 1                                       # Update z flag on subtract
        else: z = 0
    elif opCode == 0b0100:                                      # Test for branch on zero
        if z == 1: pc = address                                 # If BEQ load PC on zero flag
    print('pc = ',pcOld,'opCode =',opCode,'\tRegister r0 =',r0,'z = ',z)
                                                                # The '\t' performs a tab operation