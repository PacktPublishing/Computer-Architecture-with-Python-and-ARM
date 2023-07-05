# # Test reading a file
with open("simPython.txt",'r') as example:          # Open the file for reading
 theText = example.readlines()                      # Read the file example
print('The source file ',theText)                   # Display the file
for i in range(0,len(theText)):                     # This loop scans the file
 theText[i] = theText[i].rstrip()                   # rstrip() removes end-of-file markers
print('The source file ',theText)
