# Implement fetch cycle and execute cycle: include three test instructions

mem = [0] * 12                                                      # Setup 12-location memory
pc = 0                                                              # Initialize pc to 0
mem[0] = 0b000100001100                                             # First instruction load r0 with 12
mem[1] = 0b001000000111                                             # Second instruction add mem[7] to r0
mem[2] = 0b111100000000                                             # Third instruction is stop
mem[7] = 8                                                          # Initial data in location 7 is 8
def fetch(memory):                                                  # Function for fetch phase
    global pc                                                       # Make pc a global variable
    ir = memory[pc]                                                 # Read instruction and move to IR
    pc = pc + 1                                                     # Increment program counter for next cycle
    return(ir >> 8, ir & 0xFF)                                      # Returns opCode and operand
run = 1                                                             # run = 1 to continue
while run == 1:                                                     # REPEAT: The program execution loop
    opCode, address = fetch(mem)                                    # Call fetch to perform fetch phase
    if opCode == 0b1111: run = 0                                    # Execute phase for stop (set run to 0 on stop)
    elif opCode == 0b0001:                                          # Execute phase for load number
        r0 = address                                                # Load r0 with contents of address field
    elif opCode == 0b0010:                                          # Execute phase for add
        mar = address                                               # Copy address in opCode to MAR
        mbr = mem[mar]                                              # Read the number to be added
        r0 = mbr + r0                                               # Do the addition
    print('pc = ',pc - 1, 'opCode =', opCode, 'Register r0 =',r0)   # We print pc – 1 because the pc is incremented