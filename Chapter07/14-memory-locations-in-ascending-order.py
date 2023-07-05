import random # System library to generate random numbers
mem = [0] * 32 # Set up memory
r = [0] * 8 # Set up registers
for i in range(32): mem[i] = random.randint(0,256) # Fill memory with random numbers
for i in range(32): print(i, mem[i])
def ord(reg,rD,memory): # Pass registers, memory, and register number
    temp = memory[reg[rD]] # rD is the destination register
    if memory[reg[rD] + 1] > temp:
        memory[reg[rD]] = memory[reg[rD]+1]
        memory[reg[rD] + 1] = temp
    return()
go = True
r = [0] * 8
rD = 0
while go:
    x = input('Type address of first: ')
    r[rD] = int(x)
    if r[rD] > 30: # Exit on memory address 31 or higher
        print('End of run')
        break
    else:
        print('Before: mem[x] = ',mem[r[rD]], 'next = ',mem[r[rD] + 1])
        ord(r,0,mem)
        print('After: mem[x] = ',mem[r[rD]], 'next = ',mem[r[rD] + 1])