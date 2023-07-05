p = 1022
q = "{0:b}".format(p)
print('p in decimal is',p, "and in binary, it's",q)

p1, p2 = 26, 2033
q1 = "{0:16b}".format(p1)
q2 = "{0:16b}".format(p2)
print('p1 is',q1, '\nand p2 is',q2)

p1, p2 = 26, 2033
q1 = "{0:016b}".format(p1)
q2 = "{0:016b}".format(p2)
print('p1 is',q1, '\nand p2 is',q2)