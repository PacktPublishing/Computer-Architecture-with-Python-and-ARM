def adder(P,Q):                     # Adder function
    R = P + Q
    return (R)                      # Return the sum R
def subtractor(P,Q):                # Subtractor function
    global R                        # Make R global
    R = P - Q                       # No need to return a value
A, B = 7, 2                         # Note Python's multiple assignment
C = adder(A,B)                      # Do addition
subtractor(A,B)                     # Do subtraction (just call the function)
print('Sum =', C, 'Diff = ',R)