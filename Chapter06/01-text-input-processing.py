testCode = 'testCode.txt'
altCode = ['nop', 'NOP 5', 'add R1,R2','', 'LDR r1,[r2]', 'ldr r1,[R2]','\n', 'BEQ test @www','\n']
x = input('For disk enter d, else any character ')
if x == 'd':
    with open(testCode, 'r') as source0:
        source = source0.readlines()
    source = [i.replace('\n','') for i in source]
else: source = altCode
print('Source code to test is',source)
sFile0 = []
for i in range(0,len(source)):                          # Process the source file in list sFile
    t1 = source[i].replace(',',' ')                     # Replace comma with space
    t2 = t1.replace('[',' ')                            # Remove [ brackets
    t3 = t2.replace(']',' ')                            # Remove ] brackets
    t4 = t3.replace(' ',' ')                            # Remove any double spaces
    sFile0.append(t4)                                   # Add result to source file
sFile1= [i for i in sFile0 if i[-1:]!='\n']             # Remove end-of-lines
sFile2= [i.upper() for i in sFile1]                     # All uppercase
sFile3= [i.split('@')[0] for i in sFile2]               # Remove comments with @
sFile4= [i.rstrip(' ') for i in sFile3 ]                # Remove trailing spaces
sFile5= [i.lstrip(' ') for i in sFile4 ]                # Remove leading spaces
sFile6=[i for i in sFile5 if i != '']                   # Remove blank lines
print ('Post-processed output', sFile6)