Sequence =['W','R','R','W','R','W','W','W','W','R','W','W','R','R','R']
numRed = 0
maxRed = 3
count = 0
while numRed != maxRed:
 token = Sequence[count]
 if token == 'R':
  numRed = numRed + 1
 else: numRed = 0
 print('count', count,'token',token,'numRed',numRed)
 count = count + 1
print('Three reds found starting at location', count - 3)