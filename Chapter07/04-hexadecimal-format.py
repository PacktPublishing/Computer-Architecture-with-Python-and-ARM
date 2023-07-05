p1, p2 = 30, 64123
q1 = "{0:8x}".format(p1)
q2 = "{0:8x}".format(p2)
q3 = "{0:08x}".format(p1)
q4 = "{0:08x}".format(p2)
print('\n', q1, '\n', q3, '\n', q2, '\n', q4,'\n\n')

# Binary and hexadecimal formats combined

x, y = 1037, 325
xBin = "{0:016b}".format(x)
yHex = "{0:04x}".format(y)
print("x is",xBin,"y is",yHex)
print("x is","0b" + xBin,"y is","0x" + yHex)