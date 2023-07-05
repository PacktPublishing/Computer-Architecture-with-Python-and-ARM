# Simple Calculator V1.0 2021.10.01
print('Hello. Input operations in the form 23 * 4. Type E to end.')         # Say hello!
go = 1                                                                      # go is 1 to run the program
while go == 1:                                                              # Repeat indented instructions until go not 1
    x = input('Type first number: ')                                        # Ask for a number and call it x
    x1 = int(x)                                                             # Convert keyboard input into an integer
    op = input('Type operator + or - or / or *: ')                            # Ask for an operator and call it y
    if op == 'E':                                                           # If the operator is E then 
        go = 0                                                              #       Set go to 0 to stop
        print('Program ended')                                              #       Say goodbye
        break                                                               #       Jump out of the program
    y = input('Type second number: ')                                       # Ask for a second number and call it y
    y1 = int(y)                                                             # Convert keyboard input into an integer
    if op == '+': result = x1 + y1                                          # If the operator is + do addition
    if op == '-': result = x1 - y1
    if op == '/': result = x1 / y1
    if op == '*': result = x1 * y1
    print('Result = ', result, '\n')                                        # Print the result then repeat from "while"