import sympy as sp
import random

def matrix_groups():

    matrix_groups = 5


    display_group = 2

    for i in range(0, matrix_groups):

        a,b,c,d = random.random(), random.random(), random.random(), random.random()
        e,f,g,h = random.random(), random.random(), random.random(), random.random()

        A = sp.Matrix([[a, b], [c, d]])
        B = sp.Matrix([[e, f], [g, h]])

        #inverse
        A_inv = A.inv()
        B_inv = B.inv()

        #combination
        A_inv_B_inv = A_inv * B_inv
        

        AB = A*B
        AB_inv = AB.inv()
        print("A", A, "\n", "B", B, "\n", "AB: ", AB, "\n", "AB_inv:", AB_inv, "\n", "A_inv_B_inv:", A_inv_B_inv)





a,b,c,d = sp.symbols('a b c d')
e,f,g,h = sp.symbols('e f g h')

A = sp.Matrix([[a, b], [c, d]])
#B = sp.Matrix([[e, f], [g, h]])

#inverse

#A_inv = sp.Matrix([[(1/a) + (c*b)/(((a**2)*d) - (a*b*c)), (-b/(a*d)) + (1/c)],
                   #[ (-c)/(a*d) + (1/b) , (1/d) - (a/(c*b))]])
#B_inv = B.inv()

#display a_inv in a readable format
#sp.pprint(A.inv())

A = sp.Matrix([[1, -1], [1, 1]])
A_inv = sp.Matrix([[1,1],[-1, 1]])


A = sp.Matrix([[2, 0, 2], [1, 1,2], [-1, 0, -1]])

A = sp.Matrix([[1316.1316, 1317.1316], [-1315.1316, -1316.1316]])
print(A*A)

""" print( sp.latex( A ))
print( sp.latex( B ))

print( sp.latex( A_inv ))
print( sp.latex( B_inv )) """
#print(sp.latex(AB*(B_inv*A_inv)))
#print( sp.latex( (B_inv*A_inv) ))



##a_inv = (1/a)  * ( 1+ ((-c/a) * ( (-b)/(d - ((c/a)*b) ) ) ) )
#b_inv = (1/a)  * (( (-b)/(d - ((c/a)*b) ) ))
##c_inv = (-c/a) * (1/( (-b)/(d - ((c/a)*b) ) ))
#d_inv = (1/( (-b)/(d - ((c/a)*b) ) ))
#print(sp.latex(mode))

#A_inv = sp.Matrix([[a_inv, b_inv], [c_inv, d_inv]])

#print(sp.latex(A_inv))

#print(A*A_inv)

#combination

#A_inv_B_inv = A_inv * B_inv

#print(A_inv_B_inv[0].simplify())