myFile = 'testText.txt'
with open(myFile,'r') as sFile:
 sFile = sFile.readlines() # Open the source program
print (sFile)
sFile = ['ADD R1 R2 R3', 'BEQ LOOP', '', 'LDRL R2 4','']
sFile = [i.split() for i in sFile if i != ""]
print(sFile)