price = 'eggs $2, cheese $4'
print('Price before replacement: ', price)
price = price.replace('$', '£')         # Replace $ by £ in the string price
print('Price after replacement: ', price)


x ='###this Is A test???'
print ('x before replacement', x)
x = x.lstrip('#')                       # Remove left-hand leading '#' characters to get x = 'this Is A test???'
x = x.rstrip('? ')                      # Remove right-hand trailing '?' characters to get x = 'this Is A test'
x = x.lower()                           # Convert to lower-case to get x = 'this is a test'
print ('x after replacement', x)