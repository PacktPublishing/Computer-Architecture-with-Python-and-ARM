sFile=[['test','EQU','5'],['not','a','thing'],['xxx','EQU','88'],['ADD','r1','r2','r3']]
print('Source: ', sFile)
symbolTab = {}                                          # Creates empty symbol table
for i in range (0,len(sFile)):                          # Deal with equates eg PQR EQU 25
    print('sFile[i]', sFile[i])
    if len(sFile[i]) > 2 and sFile[i][1] == 'EQU':      # Is the second token 'EQU'?
        print('key/val', sFile[i][0], sFile[i][2])      # Display key and value pair
        symbolTab[sFile[i][0]] = sFile[i][2]            # Now update symbol table
sFile = [i for i in sFile if i.count('EQU') == 0]       # Delete equates from source file
print('Symbol table: ', symbolTab)
print('Processed input: ',sFile)