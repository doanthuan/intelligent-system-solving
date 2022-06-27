from sympy import Eq, solve, symbols, solveset, simplify, S, solve_rational_inequalities, solve_poly_inequality, Poly, Symbol
# import sympy.printing as printing
# delta__y_l = sym.symbols('Delta__y_l')
# print(printing.latex(delta__y_l))

# a, b, c, b1, b2, d1 = symbols('a b c b1 b2 d1')
# a = 60
# c = 50
# bt1 = Eq(a + b + c, 180)
# bt2 = Eq(b1 * 2, b)
# bt3 = Eq(b2 * 2, b)
# bt4 = Eq(a + b1 + d1, 180)
# bts = [bt1, bt2, bt3, bt4]
# #bts = [bt1, bt5, bt6]
# kq = solve(bts, [b,b1, b2, d1])
# print(kq)

# a1, b1, m1, m2 = symbols('a1 b1 m1 m2', positive=True)

# eq1 = Eq(a1 + b1 + m1 , 180)
# eq2 = Eq(m1 + m2 , 180)
# kq = solve([eq1, eq2], [ b1, m2])
# print(kq)
# b1 = kq[b1]
# m2 = kq[m2]
# x1 = b1 - m2
# x2 = simplify(x1)
# print(x2.is_negative)
# BAC, ABC, ACB, BAK, ABK, AKB, CBK, BCK, BKC, KAM, AKM, AMK, BAM, ABM, AMB, CBM, BCM, BMC, KCM, CKM, CMK, CAM, ACM, AMC = symbols('BAC ABC ACB BAK ABK AKB CBK BCK BKC KAM AKM AMK BAM ABM AMB CBM BCM BMC KCM CKM CMK CAM ACM AMC', positive=True)

# path_eq = [Eq(AMB + AMK, 180), Eq(ABM + AMB + BAM, 180), Eq(ABM, ABK)]
# path_symbols = [AMK, ABK, AMB, ABK, BAM, AMK, ABM]

# kq = solve(Eq(AMB + AMK, 180), [AMB])
# print(kq)
# AMB = kq[0]

# kq = solve(Eq(ABM + AMB + BAM, 180), [ABM])
# print(kq)
# ABM = kq[0]

# kq = solve( Eq(ABM, ABK), [ABK])
# print(kq)
# ABK = kq[0]
# x = AMK - ABK
# print(x)
# quit()

AMK, KAM, MKA = symbols('AMK KAM MKA', positive=True)
eqs = Eq(AMK + KAM + MKA, 180)
kq = solve(eqs, [MKA])
print(kq)
quit()


BAC, ABC, ACB, BAK, AKB, CBK, BCK, BKC, KAM, AKM, BAM, ABM, AMB, CBM, BCM, BMC, KCM, CKM, CMK, CAM, ACM, AMC = symbols('BAC, ABC, ACB, BAK, AKB, CBK, BCK, BKC, KAM, AKM, BAM, ABM, AMB, CBM, BCM, BMC, KCM, CKM, CMK, CAM, ACM, AMC', positive=True)
ABK, AMK = symbols('AMK ABK', positive=True)
all_eqs = [Eq(AKB + BKC, 180), Eq(ABK + CBK, ABC), Eq(AMC, AMK + CMK), Eq(ABC + ACB + BAC, 180), Eq(BAK, BAC), Eq(AMB + AMK, 180), Eq(BAM + KAM, BAK), Eq(ABK + AKB + BAK, 180), Eq(BCK, ACB), Eq(BMC + CMK, 180), Eq(BCM 
+ KCM, BCK), Eq(BCK + BKC + CBK, 180), Eq(AKM, AKB), Eq(AKM + AMK + KAM, 180), Eq(ABM, ABK), Eq(ABM + AMB + BAM, 180), Eq(CBM, CBK), Eq(BCM + BMC + CBM, 180), Eq(CKM, BKC), Eq(CKM + CMK + KCM, 180), Eq(CAM, KAM), Eq(ACM, KCM), Eq(ACM + AMC + CAM, 180)]

# eqs = [Eq(AKB + BKC, 180), Eq(ABK + CBK, ABC), Eq(AMC, AMK + CMK), Eq(BAK, BAC), Eq(AMB + AMK, 180), Eq(BAM + KAM, BAK), Eq(BCK, ACB), Eq(BMC + CMK, 180), Eq(BCM + KCM, BCK), Eq(AKM, AKB), Eq(ABM, ABK), Eq(CBM, CBK), Eq(CKM, BKC), 
# Eq(CAM, KAM), Eq(ACM, KCM), Eq(ABC + ACB + BAC, 180), Eq(ABK + AKB + BAK, 180), Eq(BCK + BKC + CBK, 180), Eq(AKM + AMK + KAM, 180), Eq(ABM + AMB + BAM, 180), Eq(BCM + BMC + CBM, 180), Eq(CKM + CMK + KCM, 180), Eq(ACM + AMC + 
# CAM, 180)]

# kq = solve(eqs, [BAC, ABC, ACB, BAK, AKB, CBK, BCK, BKC, KAM, AKM, BAM, ABM, AMB, CBM, BCM, BMC, KCM, CKM, CMK, CAM, ACM, AMC, AMK, ABK])
# print(kq)
# quit()

#kq = solve(eqs, [ AMK, ABK, AMB, ABC,  BAK, AKB, CBK,  KAM, AKM, AMB, CMK, AMC])
# kq = solve(eqs, [ AMK, ABK, AMB, ABC,  BAK, AKB, CBK,  KAM, AKM, AMB, CMK, AMC])
# print(kq)

# step 1: solve with AMB
# eqs = [Eq(AMB + AMK, 180), Eq(ABM + AMB + BAM, 180)]
# kq = solve(eqs, [AMB, AMK, ABM, BAM])
# print(kq)

# eq = Eq(AMB + ABC + 10, AMK + 20)
# print(eq.lhs.free_symbols)
# print(eq.rhs.free_symbols)

# AMB_1 = solve(Eq(AMB + AMK, 180), [AMB])[0]
# print(AMB_1)


# AMB_2 = solve(Eq(ABK + AMB + BAM, 180), [AMB])[0]
# print(AMB_2)

# ABK = solve(Eq(AMB_1, AMB_2), [ABK])[0]
# print(ABK)

# print(simplify(ABK-AMK))

#BAC, ABC, ACB, BAK, ABK, AKB, CBK, BCK, BKC, KAM, AKM, AMK, BAM, ABM, AMB, CBM, BCM, BMC, KCM, CKM, CMK, CAM, ACM, AMC = symbols('BAC ABC ACB BAK ABK AKB CBK BCK BKC KAM AKM AMK BAM ABM AMB CBM BCM BMC KCM CKM CMK CAM ACM AMC', positive=True)
rel_eqs = [Eq(AMB + AMK, 180), Eq(ABM + AMB + BAM, 180), Eq(ABM, ABK)]

kq = solve(rel_eqs, [AMK, ABK, BAM, AMK, ABK, ABM, AMB])
print(kq)

# AMK = kq[AMK]
# ABK = kq[ABK]
# x =simplify(AMK-ABK)
# print(x)

# kq = solve_rational_inequalities([( (AMK,ABK), '>')], [ AMK, ABK, ABM, BAM, AMB])
# print(kq)

# if AMK in kq.keys():
#     AMK = kq[AMK]

# if ABK in kq.keys():
#     ABK = kq[ABK]
# elif ABK in kq.values():
#     for key, value in kq.items():
#         # print(f"{key}:{value}")
#         if ABK == value:
#             ABK = key

# kq = solveset(AMK-ABK > 0, [AMK, ABK], S.Reals)
# print(kq)
# eqx = Eq(ABK, ABM)
# x = (simplify(AMK-ABK))
# print(x)

