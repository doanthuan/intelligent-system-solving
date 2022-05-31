from sympy import *

x, y, z, a, b, c, S = symbols('x,y,z,a,b,c,S')
canhA, canhB, canhC, gocA, gocB, gocC, dientichS = symbols('canhA,canhB,canhC,gocA,gocB,gocC,dienTichS')

init_printing()

s1 = FiniteSet(x + 1, y, z)
s2 = FiniteSet(1 + x, y)
eq1 = Eq(x + y, y + x)

set1 = set([canhA, canhB, canhC])
set2 = set([canhC])
print(set1)
print(set2)
set3 = set1.intersection(set2)

b1 = FiniteSet(canhA, canhB, canhC)._contains(canhB)

m = symbols("m")

pt = sqrt(m ** 2 - 1)

sosanh = Eq(pt, 0.1)

print(solve(Eq(pt, 2)))

print(b1)
