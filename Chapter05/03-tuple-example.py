opCodes = [('NOP','misc',0),('BEQ','flow',1),('LDR','move',2),('ADD','arith',3)]
for instruction in opCodes:                 # Step through the op-codes
 print(instruction)                         # Print the current op-code
 op = instruction[0]                        # Extract the three tuple members
 group = instruction[1]
 params = instruction[2]
 print(op, group, params)                   # Print the three tuple values
 if op == 'BEQ': print('beq found')         # Demo! Print BEQ when we find it