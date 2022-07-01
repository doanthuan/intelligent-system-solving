import inspect
import itertools
from sympy import Eq
from ceq import Ceq
from cobj import Cobj
from cokb import Cokb
from crel import Crel
from line import Line
from angle import Angle
from triangle import Triangle

'''
RULES
'''

# Rule nội tại
# tạo tam giác từ 2 cạnh
def rule_01(a: Line, b: Line):
    if Triangle.is_triangle(a, b):
        Triangle.from_lines(a, b)

# xét 2 góc bằng nhau từ 2 cạnh
def rule_02(A: Angle, B: Angle):
    if A.equal(B):
        Ceq(A.symb, B.symb)

# xét 2 góc kề -> tổng = góc lớn
def rule_03(A: Angle, B: Angle):
    if A.is_adjacent(B):
        adj_angle = A.get_adjacent_angle(B)
        Ceq(A.symb + B.symb, adj_angle.symb)

# xét 2 góc kề bù -> tổng = 180
def rule_04(A: Angle, B: Angle):
    if A.is_complementary(B):
        Ceq(A.symb + B.symb, 180)

def rule_10(A: Angle, B: Angle) -> Crel:
    if Crel.relation_exist(Crel("SO_LE_TRONG", A, B)):
        if Cokb.equation_true(Eq(A.symb, B.symb)):
            pass

class Crule:

    rules = [rule_01, rule_02, rule_03, rule_04]

    @staticmethod
    def apply_rules():
        for rule_func in Crule.rules:
            Crule.apply_rule(rule_func)

    @staticmethod
    def apply_rule(rule_func):
        func_args = Crule.get_func_args(rule_func)
        list_args = Crule.get_combinations(func_args)
        for args in list_args:
            rule_func(*args)

    def get_func_args(rule_func):
        func_args = []
        specs = inspect.getfullargspec(rule_func)
        for arg in list(specs.annotations.values()):
            if 'Line' in str(arg):
                func_args.append(list(Cobj.lines.values()))
            if 'Angle' in str(arg):
                func_args.append(list(Cobj.angles.values()))
        return func_args

    def get_combinations(list_args):
        results = []
        for subset in itertools.combinations(list_args[0], len(list_args)):
            results.append(subset)
        return results