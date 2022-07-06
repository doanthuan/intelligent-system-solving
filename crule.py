import inspect
import itertools
from symtable import Symbol
from sympy import Eq
from ceq import Ceq
from log import Log
from cobj import Cobj
from relation import Relation
from line import Line
from angle import Angle
from triangle import Triangle

'''
RULES
'''

# Rule nội tại
# tạo tam giác từ 3 cạnh
def rule_01(a: Line, b: Line, c: Line):
    if Triangle.is_triangle(a, b, c):
        tri_name = Triangle.from_lines(a, b)
        if not Cobj.triangle_exist(tri_name):
            Triangle(tri_name)

# xét 2 góc kề bù -> tổng = 180
def rule_04(A: Angle, B: Angle):
    if A.is_complementary(B):
        Ceq(A.symb + B.symb, 180)
        

# vẽ tia phân giác tới giao điểm 3 tia
def rule_06(triangle: Triangle):
    if triangle.bisector_center is not None:
        for from_v in triangle.vertexs:
            if from_v in triangle.bisectors.keys():
                triangle.bisectors[from_v].add_point(triangle.bisector_center)


# # luật về góc
# def rule_07(A: Symbol,B: Symbol,C: Symbol, I: Symbol, B2: Symbol, C2: Symbol):
#     eq1 = Eq(A + B + C , 180)
#     eq2 = Eq(I + B2 + C2 , 180)
#     ieq1 = B2 < B
#     ieq2 = C2 < C
#     if Ceq.eq_exist(eq1) and Ceq.eq_exist(eq2) and Ceq.ieq_exist(ieq1) and Ceq.ieq_exist(ieq2):
#         Ceq.ieq(A < I)

# # luật về góc
# def rule_07(eq1: Eq, eq2: Eq, ieq1: Cieq, ieq2: Cieq):
#     eq1 = Eq(A + B + C , 180)
#     eq2 = Eq(I + B2 + C2 , 180)
#     ieq1 = B2 < B
#     ieq2 = C2 < C
#     if Ceq.eq_exist(eq1) and Ceq.eq_exist(eq2) and Ceq.ieq_exist(ieq1) and Ceq.ieq_exist(ieq2):
#         Ceq.ieq(A < I)

# góc tù
# def rule_08(angle: Angle):
#     if angle.value > 90 or angle.symb:
#         for from_v in triangle.points:
#             if from_v in triangle.bisectors.keys():
#                 triangle.bisectors[from_v].add_point(triangle.bisector_center)

# def rule_07(B: Angle, B2: Angle, C: Angle, C2: Angle):
#     if Angle.is_triangle(B, C) and Angle.is_triangle(B2, C2) and B.is_adjacent_parent(B2) and C.is_adjacent_parent(C2):
#         A = Angle.third_angle(B, C)
#         E = Angle.third_angle(B2, C2)
#         Ceq.ieq(A.symb < E.symb)


# Rule định lý
# 2 góc so le trong = nhau => 2 đoạn song song
def rule_10(A: Angle, B: Angle) -> Relation:
    rel = Relation("SO_LE_TRONG", A, B)
    eq = Eq(A.symb, B.symb)
    if Relation.exist(rel) and Cobj.equation_true(eq):
        new_rel = Relation.make("SONG_SONG", A.line1, B.line1)
        if new_rel is not None:
            Log.trace_rels.append((new_rel, "rule_10", [rel, eq]))

# xét 2 góc so le trong
def rule_11(A: Angle, B: Angle):
    if A.is_staggered(B):
        new_rel = Relation.make("SO_LE_TRONG", A, B)
        if new_rel is not None:
            Log.trace_rels.append((new_rel, "rule_05", [A, B]))

class Crule:

    rules = [rule_01, rule_04, rule_06, rule_10, rule_11]
    
    def run():
        for rule_func in Crule.rules:
            Crule.apply_rule(rule_func)

    def init():
        while Cobj.rule_depth < 3:
            Cobj.rule_depth += 1
            Crule.run()

    def apply_rule(rule_func):
        func_args = Crule.get_rule_args(rule_func)
        list_args = Crule.get_permutations(func_args)
        for args in list_args:
            rule_func(*args)

    def get_rule_args(rule_func):
        func_args = []
        specs = inspect.getfullargspec(rule_func)
        for arg in list(specs.annotations.values()):
            if 'Line' in str(arg):
                func_args.append(list(Cobj.lines.values()))
            if 'Angle' in str(arg):
                func_args.append(list(Cobj.angles.values()))
            if 'Triangle' in str(arg):
                func_args.append(list(Cobj.triangles.values()))
            # if 'Symbol' in str(arg):
            #     func_args.append(list(Cobj.symbs.values()))
        return func_args

    def get_combinations(list_args):
        results = []
        for subset in itertools.combinations(list_args[0], len(list_args)):
            results.append(subset)
        return results

    def get_permutations(list_args):
        results = []
        for subset in itertools.permutations(list_args[0], len(list_args)):
            results.append(subset)
        return results

