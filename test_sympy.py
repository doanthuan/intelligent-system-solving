from sympy import Eq, solve, symbols
# import sympy.printing as printing
# delta__y_l = sym.symbols('Delta__y_l')
# print(printing.latex(delta__y_l))

a, b, c, b1, b2, d1 = symbols('a b c b1 b2 d1')
#Eq(goc_a, 60)
#Eq(goc_b, 50)
bt5 = Eq(a, 60)
bt6 = Eq(c, 50)
bt1 = Eq(a + b + c, 180)
# bt2 = Eq(b1 * 2, b)
# bt3 = Eq(b2 * 2, b)
# bt4 = Eq(a + b1 + d1, 180)
# bts = [bt1, bt2, bt3, bt4, bt5, bt6]
bts = [bt1, bt5, bt6]
kq = solve(bts, [a, b, c])
print(kq)
