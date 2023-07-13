# 31 Aug 2020 TESTING a variable format instruction set V1
x = input("Enter three width for: rD,rS1,rS2 (e.g., 2,2,3) >> ")
x = x.replace(' ',',')
x = x.split(",") # Get register sizes and convert list into tokens
x1 = int(x[0]) # First register size rD
x2 = int(x[1]) # Second register size rS1
x3 = int(x[2]) # Third register size rS2
y = (x1,x2,x3) # Convert data size elements into a tuple
z = input("Enter three register operands for: rD,rS1,rS2 (e.g. R1,R3,R2)>> ")
opCode = 0b1111110 # Dummy 7-bit binary opcode
z = z.replace(' ',',')
z = z.split(",")
t1,t2,t3 = 0,0,0 # t1,t2,t3 are up to three tokens in the predicate
t1 = int(z[0][1:]) # Extract three parameters
t2 = int(z[1][1:])
t3 = int(z[2][1:])
print ('Register widths: rD = ',t1, 'rS1 = ',t2,'rS2 = ',t3) # Print the registers
opCode = opCode << x1 | t1 # Insert the rD field
opCode = opCode << x2 | t2 # Insert the rS1 field
opCode = opCode << x3 | t3 # Insert the rS2 field
intLen = 32 - 7 - x1 - x2 - x3 # Calculate the length of the literal field
opCode = opCode << intLen # Shift left by literal size to create 16-bit instruction
print("opCode",bin(opCode)) # Print the result