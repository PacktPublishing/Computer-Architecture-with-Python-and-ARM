def display(): # Display processor status
    if oldPC in breakTab: print('Breakpoint at %03x' %oldPC) # if pc in the table
    print("PC = %03x" %oldPC, ' Op-code = %s' %instruction)
    return()
opCodes = ['nop', 'test', 'test1', 'stop'] # Op-code set
traceCodes = [] # List of codes to be traced (initially empty)
mem = ['nop'] * 32 # Initialize memory to NOPs
mem[10] = 'test' # Dummy operation at 10
mem[20] = 'test' # Dummy operation at 20
mem[25] = 'test1' # Dummy operation at 25
r = [0] * 4 # Set up 4 registers (not used)
pc = 0 # Initialize program counter
oldPC = 0 # Initialize previous program counter
run = 1 # Set run to 1 to go
trace = 1 # Set trace to 1 to single-step
count = 0 # Count is the number of cycles not displayed
breakTab = [] # Create table for breakpoints
while run == 1: # PROGRAM LOOP
    instruction = mem[pc] # read instruction
    oldPC = pc # Save current PC for display
    pc = pc + 1 # Increment PC
    # Do processing here # For experimentation (add stuff here)
    if pc == 32 or instruction == 'stop': run = 0 # End on stop instruction or max PC
    if trace == 0 and count != 0: # Test for single-step mode
        count = count - 1 # If not single-step, decrement counter
        if count == 0: # If count zero, return to single step mode
            trace = 1 # Exit silent mode
            continue # Now drop to bottom of the loop
if trace == 0 and pc in breakTab: # If not single-step, check for breakpoint
    print('Breakpoint\n') # Print status at the breakpoint
    display()
if trace == 0 and instruction in traceCodes: # If not single-step and opcode in table
    print('Trace Code') # Print status info
    display()
if trace == 1: # If single-step with trace on
    display() # Display the status
    c = input('>> ') # Wait for keyboard input
    if c == '': continue # If it's just a return, continue
    elif c[0]== 't' and len(c) > 2 and c[2:].isdigit(): # Test for 't' and number
        count = int(c[2:]) # Set the count for silent mode
        trace = 0 # Turn off single-step
    elif c[0] == 'b' and len(c) > 2 and c[2:].isdigit():# Test for b (set breakpoint)
        breakPoint = int(c[2:]) # Get breakpoint address and add to table
        breakTab.append(breakPoint)
    elif c == 'd': # Test for d to display breakpoint info
        print('Display status: breakpoints =', breakTab, \
        'traced codes =',traceCodes)
    elif c in opCodes: traceCodes.append(c) # Test for a valid opcode and add to list
print('\nProgram terminated')