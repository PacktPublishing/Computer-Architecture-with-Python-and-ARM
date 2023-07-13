prefixes = {'UK':44, 'USA':1, 'Germany':49, 'France':33}
while True:                     # Infinite loop
 x = input('Country? ')         # Ask for the country
 y = prefixes.get(x)            # Look up the prefix
 if y == None:                  # If None print error message
    print('Prefix not found')
    break                       # And exit the loop
 else: print('Prefix = ',y)
print('Program terminated')