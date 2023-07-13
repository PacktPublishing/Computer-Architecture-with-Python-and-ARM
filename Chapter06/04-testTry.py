myProg = 'testException1.txt'                           # Name of default program
try:                                                    # Check whether this file exists
    with open(myProg,'r') as prgN:                      # If it's there, open it and read it
        myFile = prgN.readlines()
except:                                                 # Call exception if file not there
    altProg = input('Enter source file name: ')         # Request a filename
    with open(altProg,'r') as prgN:                     # Open the user file
        myFile = prgN.readlines()
print('File loaded: ', myFile)