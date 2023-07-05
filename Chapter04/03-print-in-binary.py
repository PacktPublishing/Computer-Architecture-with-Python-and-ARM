x = 0b0011100101010011          # A 16-bit binary string we are going to process
y = (x >> 8) & 0xF              # Shift x right 8 places and mask it to 4 bits
print('y is ',bin(y))           # Print the result in binary form using bin()