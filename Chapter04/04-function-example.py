def fun_1():                                                # A dummy function
 p = 3                                                      # p is local to fun_1 and set to 3
 global q                                                   # q is global and visible everywhere
 print('In fun_1 p =',p)                                    # Print p in fun_1
 print('In fun_1 q =',q)                                    # Print q in fun_1
 q = q + 1                                                  # q is changed in this function
 p = p + 1                                                  # p is changed in this function
 r = 5
 return()                                                   # You don't need a return
p = 5                                                       # p is defined in the body
q = 10                                                      # q is defined in the body
print('In body: p =',p, 'q =',q )                           # Print current values of p and q
fun_1()                                                     # Call fun_1 and see what happens to p and q
print('In body after fun_1 q =',q, 'after fun_1 p = ',p)