# Testing the fetch cycle
mem = [0] * 16                  # Setup 16 locations in memory
pc = 0                          # Initialize pc to 0
mem[0] = 0b011000001010         # Dummy first instruction (op-code in bold) 0b indicates binary value
mem[1] = 0b100011111111         # Dummy second instruction
def fetch(memory):              # Fetch cycle implemented using a function
    global pc                       # Make pc global because we change it
    mar = pc                        # Copy pc to mar
    pc = pc + 1                     # Increment the pc ready for next instruction
    mbr = memory[mar]               # Read instruction from memory
    ir = mbr                        # Copy instruction to instruction register
    cu = ir >> 8                    # Shift instruction 8 places right to get the operation code
    address = ir & 0xFF             # Mask op-code to 8-bit address
    return(cu, address)             # Return instruction and address
opCode,address = fetch(mem)         # Do a fetch cycle
print('pc =', pc - 1, 'op-code =', opCode, ' Operand =', address)
opCode,address = fetch(mem)         # Do a fetch cycle
print('pc =', pc - 1, 'op-code =', opCode, ' Operand =', address)