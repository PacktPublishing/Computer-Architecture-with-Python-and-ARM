# Simple algorithm to detect consecutive tokens
maxRed = int(input("How many red tokens are you looking for? "))
go = 1
numRed = 0
while go == 1:
 y = input("Which token is it? Red or white? ")
 if y == 'w': numRed = 0
 else: numRed = numRed + 1
 if numRed == maxRed: go = 0
print(maxRed, "Reds found")