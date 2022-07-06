from sympy import Eq, StrictGreaterThan, StrictLessThan, Unequality, reduce_inequalities, solve, symbols, solveset, simplify, S, solve_rational_inequalities, solve_poly_inequality, Poly, Symbol
from sympy.solvers.inequalities import solve_poly_inequalities
from sympy.solvers.inequalities import reduce_rational_inequalities
x = symbols('x')
A, B, C, E, B1, B2, C1, C2 = symbols('A B C E B1 B2 C1 C2')
#eq1 = Eq(A, 90)
eq2 = Eq(A + B + C, 180)
eq3 = Eq(E + B2 + C2, 180)
exp1 = B > B2
exp2 = C > C2
eq4 = Eq(B, 90)
#eq3 = Poly()
#kq = solve([eq2,eq3,exp1,exp2],[E])
print(type(exp1))
exp3 = Unequality()
exp3.equals()

eq2 = Eq(A + B , E + C)
exp3 = B > C
kq = simplify([eq2, exp3], [A,B,E,C])
print(kq)
#kq = reduce_inequalities(exp1, eq1, [B])
#kq = reduce_rational_inequalities([[exp1, eq4]], [B2])
#print(kq)

# kq = solve_rational_inequalities([
#     (Poly(-x + 1, x), '>=')
#     ])
#kq = solve_poly_inequality(Poly(x**2 - 1, x, domain='ZZ'), '!=')
#print(kq)

#print(kq)
