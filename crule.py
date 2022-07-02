import inspect
import itertools
from sympy import Eq
from ceq import Ceq
from clog import Clog
from cobj import Cobj
from relation import Relation
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
        
# xét 2 góc so le trong
def rule_05(A: Angle, B: Angle):
    if A.is_staggered(B):
        new_rel = Relation.make("SO_LE_TRONG", A, B)
        Clog.trace_rels.append((new_rel, "rule_05", [A, B]))

# Rule định lý
def rule_10(A: Angle, B: Angle) -> Relation:
    rel = Relation("SO_LE_TRONG", A, B)
    eq = Eq(A.symb, B.symb)
    if Relation.relation_exist(rel) and Cobj.equation_true(eq):
        new_rel = Relation.make("SONG_SONG", A.line1, B.line1)
        Clog.trace_rels.append((new_rel, "rule_10", [rel, eq]))

class Crule:

    rules = [rule_01, rule_02, rule_03, rule_04, rule_05, rule_10]

    def apply_rules():
        for rule_func in Crule.rules:
            Crule.apply_rule(rule_func)

    def apply_rule(rule_func):
        func_args = Crule.get_rule_args(rule_func)
        list_args = Crule.get_combinations(func_args)
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
        return func_args

    def get_combinations(list_args):
        results = []
        for subset in itertools.combinations(list_args[0], len(list_args)):
            results.append(subset)
        return results

    def trace_rel1(new_rel, rule_id, rel, eq):
        symbs = Cobj.not_in_hypo(eq.free_symbols)
        trace_paths = []
        for a_symb in symbs:
            trace_paths.append((a_symb, eq))
        Cobj.trace_rels.append((new_rel, rule_id, [rel], trace_paths))
