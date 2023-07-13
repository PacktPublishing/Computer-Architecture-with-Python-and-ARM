sFile = ['ADD R1 R2 R3', 'BEQ LOOP', '', 'LDRL R2 4','']
sFile = [i.split() for i in sFile if i != ""]
print(sFile)