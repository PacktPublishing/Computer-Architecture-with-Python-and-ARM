mem = [4,6,1,2,7,8,4,4,5]               # Create a 9-location memory. Fill with some data
r = [0,0,0,0,0,0,0,0]                   # Create a set of 8 registers, all initialized to 0
inst = 'add r[4],mem[3],mem[7]'         # inst is our solitary instruction, stored as a string
inst1 = inst.replace(' ',',')           # Step 1: Replace any space with a comma
inst2 = inst1.split(',')                # Step 2: Split instruction into tokens at each comma
token0 = inst2[0]                       # Step 3: Get token0 via the 'add' instruction
token1 = inst2[1]                       # Step 4: Get token1, register 'r[4]'
token2 = inst2[2]                       # Step 5: Get token2, 'mem[3]'
token3 = inst2[3]                       # Step 6: Get token3, 'mem[7]'
value1 = int(token1[2])                 # Step 7: Get the register number as an integer
value2 = int(token2[4])                 # Step 8: Get the first memory number as an integer
value3 = int(token3[4])                 # Step 9: Get the second memory number as an integer
if token0 == 'add':                     # Step 10: Test for an 'add' instruction
 r[value1] = mem[value2] + mem[value3] # Step 11: If ADD, then add the contents of the memory
print('Registers: ',r)