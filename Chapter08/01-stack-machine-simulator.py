# Stack machine simulator
prog = [['push',0],['push',1],['add'],\
['push',2],['push',1],['sub'], ['push',3], ['sub'],\
['mul'], ['push',4],['swap'], ['dup'],['pull',4],\
['stop']]
stack = [0] * 8 # 8-location stack. Stack grows to lower addresses
mem = [3,2,7,4,6,0] # Data memory (first 4 locations are preloaded 3, 2, 7, 4, 6)
run = True # Execution continues while run is true
pc = 0 # Program counter - initialize
sp = 8 # Initialize stack pointer to 1 pastend of stack
while run: # Execute MAIN LOOP until run is false (STOP command)
    inst = prog[pc] # Read the next instruction
    pc = pc + 1 # Increment programcounter
    if inst[0] == 'push': # Test for push operation
        sp = sp - 1 # Pre-decrement stack pointer
        address = int(inst[1]) # Get data from memory
        stack[sp] = mem[address] # Store it on the stack
    elif inst[0] == 'pull': # Test for a pull instruction
        address = int(inst[1]) # Get destination address
        mem[address] = stack[sp] # Store the item in memory
        sp = sp + 1 # Increment stack pointer
    elif inst[0] == 'add': # If operation add TOS to NOS and push result
        p = stack[sp]
        sp = sp + 1
        q = stack[sp]
        stack[sp] = p + q
    elif inst[0] == 'sub': # sub
        p = stack[sp]
        sp = sp + 1
        q = stack[sp]
        stack[sp] = q - p
    elif inst[0] == 'mul': # mul
        p = stack[sp]
        sp = sp + 1
        q = stack[sp]
        stack[sp] = p * q
    elif inst[0] == 'div': # div (note floor division with integer result)
        p = stack[sp]
        sp = sp + 1
        q = stack[sp]
        stack[sp] = p//q
    elif inst[0] == 'dup': # dup (duplicate top item on stack)
        p = stack[sp] # get current TOS
        sp = sp - 1 # and push it on the stack to duplicate
        stack[sp] = p
    elif inst[0] == 'swap': # swap (exchange top of stack and next on stack)
        p = stack[sp]
        q = stack[sp+1]
        stack[sp] = q
        stack[sp+1]=p
    elif inst[0] == 'stop': # stop
        run = False
    if sp == 8: TOS = 'empty' # Stack elements 0 to 7. Element 8 is before the TOS
    else: TOS = stack[sp]
    print('pc =', pc-1,'sp =',sp,'TOS \
    =',TOS,'Stack',stack,'Mem',mem,'op',inst)
