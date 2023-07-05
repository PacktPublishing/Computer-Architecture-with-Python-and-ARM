mem = [0]*8                     # Create memory with 8 locations, all set to 0. This is Python
mem[3] = 4                      # Load location 3 with 4
mem[5] = 9                      # Load location 5 with 9
sum = mem[3] + mem[5]           # Add locations 3 and 5 and assign result to sum
mem[6] = sum                    # Store sum in location 6
print('mem[6] =', mem[6])       # Print contents of location 6
print('Memory =', mem)          # Print all memory locations