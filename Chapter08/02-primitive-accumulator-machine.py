# The TC2: A primitive accumulator machine
mnemonics = {0:'LDA/STR', 1:'ADD', 2:'SUB', 3:'CLR', 4:'BRA', 5:'BEQ',
6:'BNE', 7:'STOP'}
def progSet():
    global mem
    mem = [0] * 32 # The memory holds both instructions and data
    # Format CCCDMLLLLL # 000 LDA/STR, 001 ADD, 010 SUB, 011 CLR, 100 BRA, 101 BEQ, 110 BNE, 111 STOP
    mem[0] = 0b0000110000 # LDA 16 [A] = M[16]
    mem[1] = 0b0010110001 # ADD 17 [A] = [A] + M[17]
    mem[2] = 0b0001110010 # STA 18 M[18] = [A]
    mem[3] = 0b0100000011 # SUB #3 [A] = [A] - 3
    mem[4] = 0b1010001000 # BEQ 8
    mem[5] = 0b0000010010 # LDA #18 [A] = 18
    mem[6] = 0b0001110010 # STA 18 M[18] = [A]
    mem[7] = 0b0110000000 # CLR [A] = 0
    mem[8] = 0b0000000010 # LDA #2 [A] = 2
    mem[9] = 0b0100000010 # SUB #2 [A] = [A] - 3
    mem[10] = 0b1010001101 # BEQ 12
    mem[11] = 0b0000001111 # LDA #15 LDA #18 [A] = 18 Dummy not executed
    mem[12] = 0b1110000000 # STOP
    mem[16] = 0b0000000100 # 4 Data for test
    mem[17] = 0b0000000101 # 5 Data for test
    mem[31] = 0b1110000000 # Ensure STOP operation
    return(mem)
run = True # run is True for code execution. Setting run to False stops the computer
PC = 0 # The program counter points to the next instruction to execute. Initially 0
z = 0 # Initialize z-bit (note no n and c bits implemented)
mem = progSet()
# MAIN LOOP – FETCH/EXECUTE
while run: # This is the fetch/execute cycle loop that continues until run is False
    MAR = PC # FETCH PC to mem Address Register
    pcOld = PC # Keep a copy of the PC for display
    PC = PC + 1 # Increment PC
    MBR = mem[MAR] # Read the instruction, copy it to the mem Buffer Register
    IR = MBR # Copy instruction to Instruction Register – prior to decoding it
    OpCode = (IR >> 7) & 0x7 # Extract Op-Code from instruction bits 7 to 10 by shifting/masking
    Dir = (IR >> 6) & 1 # Extract data direction from instruction (0 = read, 1 = write)
    Mode = (IR >> 5) & 1 # Extract address mode from instruction (0 = literal, 1 = mem)
    Lit = IR & 0x1F # Extract literal/address field (0 = address, 1= literal)
# EXECUTE The EXECUTE block is an if statement, one for each opcode
    if OpCode == 0: # Test for LDA and STA (Dir is 0 for load acc and 1 for store in mem)
        if Dir == 0: # If Direction is 0, then it's a load accumulator, LDA
            if Mode == 0: # Test for Mode bit to select literal or direct mem operand
                Acc = Lit # If mode is 0, then the accumulator is loaded with L
            else: # If mode is 1, then read mem to get operand
                MAR = Lit # Literal (address) to MAR
                MBR = mem[MAR] # Do a read to get operand in MBR
                Acc = MBR # and send it to the accumulator
        else:
            MAR = Lit # If Direction is 1, then it's a store accumulator
            MBR = Acc # Copy accumulator to MBR
            mem[MAR] = MBR # and write MBR to mem
    elif OpCode == 1: # Test for ADD to accumulator
        if Mode == 0: # Test for literal or direct mem operand
            total = Acc + Lit # If mode is 0, then it's a literal operand
            if total == 0: z = 1 # Deal with z flag
            else: z = 0
        else: # If mode is 1, then it's a direct mem access
            MAR = Lit # Literal (address) to MAR
            MBR = mem[MAR] # Do a read to get operand in MBR
            total = MBR + Acc # And send it to the accumulator
        if Dir == 0: Acc = total # Test for destination (accumulator)
        else: mem[MAR] = total # Or mem
    elif OpCode == 2: # Test for SUB from accumulator
        if Mode == 0: # Test for literal or direct mem operand
            total = Acc - Lit # If mode is 0 then it's a literal operand
        else: # If mode is 1 then it's a direct mem access
            MAR = Lit # Literal (address) to MAR
            MBR = mem[MAR] # Do a read to get operand in MBR
            total = Lit - MBR # and send it to the accumulator
        if total == 0: z = 1 # Now update z bit (in all cases)
        if Dir == 0: Acc = total # Test for destination (accumulator)
        else: mem[MAR] = total # Or mem
    elif OpCode == 3: # Test for CLR (clear Accumulator or clear mem location)
        if Mode == 0: # If Mode = 0 Then clear accumulator
            Acc = 0
        else:
            MAR = Lit # If Mode = 1
            mem[MAR] = 0 # Then clear mem location mem[Literal]
    elif OpCode == 4: # Test for BRA Branch unconditionally
        PC = Lit - 1 # Calculate new branch target address (-1 because PC auto increment)
    elif OpCode == 5: # Test for BEQ Branch on zero
        if z == 1: PC = Lit - 1 # If z bit = 1 then calculate new branch target address
    elif OpCode == 6: # Test for BNE Branch on not zero
        if z == 0: PC = Lit - 1 # If z bit = 0 calculate new branch target address
    elif OpCode == 7: # Test for STOP
        run = False # If STOP then clear run flag toexit while loop and stop
    # End of main fetch-execute loop
    mnemon = mnemonics.get(OpCode) # Get the mnemonic for printing
    print('PC',pcOld, 'Op ',OpCode, 'Mode = ', Mode, \
    'Dir = ',Dir, 'mem', mem[16:19], 'z',z, 'Acc', Acc, \
    mnemon)