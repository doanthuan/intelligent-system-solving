import inspect
import itertools
from symtable import Symbol
from sympy import Eq
from ceq import Ceq
from log import Log
from cobj import Cobj
from relation import Relation
from angle import Angle
from triangle import Triangle
from utils import get_permutations


'''
RULES
'''      
# Rule định lý
# 2 góc so le trong = nhau => 2 đoạn song song
def rule_10(A: Angle, B: Angle) -> Relation:
    rel = Relation("SO_LE_TRONG", A, B)
    eq = Eq(A.symb, B.symb)
    if Relation.exist(rel) and Cobj.equation_true(eq):
        new_rel = Relation.make("SONG_SONG", A.line1, B.line1)
        if new_rel is not None:
            Log.trace_rule(new_rel, "rule_10", [rel, eq])

# xét 2 góc so le trong
def rule_11(A: Angle, B: Angle):
    if A.is_staggered(B):
        new_rel = Relation.make("SO_LE_TRONG", A, B)
        if new_rel is not None:
            Log.trace_rule(new_rel, "rule_11", [A, B])

# định lý về góc tam giác nhỏ trong tam giác lớn
def rule_12(tri1: Triangle, tri2: Triangle):
    ps = tri1.part_of(tri2)
    if ps is not None:
        E = Angle(ps[1]+ps[2]+ps[0])
        A = Angle(ps[1]+ps[3]+ps[0])
        ieq = Ceq.ieq(A.symb < E.symb)
        if ieq is not None:
            A.run_rules(), E.run_rules()
            log1 = f"{ps[3]+ps[0]+ps[1]} > {ps[2]+ps[0]+ps[1]}"
            log2 = f"{ps[0]+ps[1]+ps[3]} > {ps[0]+ps[1]+ps[2]}"
            log3 = f"TRIANGLE {ps[3]+ps[0]+ps[1]}: {ps[1]+ps[3]+ps[0]} + {ps[3]+ps[0]+ps[1]} + {ps[0]+ps[1]+ps[3]} = 180"
            log4 = f"TRIANGLE {ps[2]+ps[0]+ps[1]}: {ps[1]+ps[2]+ps[0]} + {ps[2]+ps[0]+ps[1]} + {ps[0]+ps[1]+ps[2]} = 180"
            
            Log.trace_rule(ieq, "rule_12", [log1, log2, log3, log4])
        

class Crule:

    rules = [rule_10, rule_11, rule_12]
    
    def run():
        for rule_func in Crule.rules:
            Crule.apply_rule(rule_func)

    def init():
        while Cobj.rule_depth < 3:
            Cobj.rule_depth += 1
            Crule.run()

    def apply_rule(rule_func):
        func_args = Crule.get_rule_args(rule_func)
        list_args = get_permutations(func_args[0], len(func_args))
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
        return func_args


