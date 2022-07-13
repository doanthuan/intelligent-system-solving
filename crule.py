import inspect
import itertools
import json
from symtable import Symbol
from sympy import Eq
from ceq import Ceq
from line import Line
from log import Log
from cobj import Cobj
from relation import Relation
from angle import Angle
from triangle import Triangle
from utils import get_permutations


'''
RULES
'''      
# Rule nội tại
# tạo góc từ 2 cạnh
def rule_01(a: Line, b: Line):
    if a.is_connect(b):
        A, B, C = a.connect_points(b)
        Angle(A+B+C)

#ANGLES
# tạo tam giác từ góc và cạnh đối diện
def rule_02(A: Angle):
    for b in list(Cobj.lines.values()):
        if (A.name[0] == b.name[0] and A.name[2] == b.name[1]) or (A.name[0] == b.name[1] and A.name[2] == b.name[0]):
                tri_name = Cobj.tri_name(A.name)
                if not Cobj.triangle_exist(tri_name):
                    Triangle(tri_name)

# xét 2 góc bằng nhau
def rule_03(A: Angle, B: Angle):
    if A.is_belongs(B):
        A.set_equal(B)

# xét 2 góc kề -> tổng = góc lớn
def rule_04(A: Angle, B: Angle):
    if A.is_adjacent(B) and not A.is_complementary(B):
        adj_angle = A.get_adjacent_parent(B)
        Ceq(A.symb + B.symb, adj_angle.symb)
        Ceq.ieq(A.symb < adj_angle.symb)
        Ceq.ieq(B.symb < adj_angle.symb)

# góc tù
def rule_05(A: Angle):
    if Ceq.check_ieq(A.symb > 90):
        rel = A.set_obtuse()# góc tù
        if rel is not None:
            ieqs = Ceq.get_ieq_by_symb(A.symb)
            Log.trace_obj(rel, "rule_05", [ieqs[0]] )

# xét 2 góc kề bù -> tổng = 180
def rule_06(A: Angle, B: Angle):
    if A.is_complementary(B):
        Ceq(A.symb + B.symb, 180)



# sắp xếp thứ tự chân tia phân giác, đường cao trong tam giác
def rule_08(tri: Triangle):
    for from_v in tri.name:
        v1, v2 = tri.get_other_vertexs(from_v)
        to_vs = []
        if from_v in tri.heights.keys():
            to_v = tri.heights[from_v].name[1]
            Angle(from_v + to_v + v1, 90)
            Angle(v2 + to_v + from_v, 90)
            to_vs.append(to_v)

        if from_v in tri.bisectors.keys():
            to_v = tri.bisectors[from_v].name[1]
            Ceq(Angle(v1 + from_v + to_v).symb, Angle(v1 + from_v + v2).symb/2)
            Ceq(Angle(to_v + from_v + v2).symb, Angle(v1 + from_v + v2).symb/2)
            if not tri.bisectors[from_v].is_ray:
                to_vs.append(to_v)
        
        if len(to_vs) == 2 and Angle(from_v + v2 + v1).value is not None and Angle(from_v + v2 + v1).value < 45: # nếu góc bên trái nhỏ hơn 45 độ
            to_vs.reverse()
        if len(to_vs) >= 1:
            Line(v2 + v1).add_point(to_vs)

# tia phân giác tới giao điểm 3 tia
def rule_09(triangle: Triangle):
    if triangle.bisector_center is not None:
        for from_v in triangle.name:
            if from_v in triangle.bisectors.keys():
                triangle.bisectors[from_v].add_point(triangle.bisector_center)  


# Rule định lý
# 2 góc so le trong = nhau => 2 đoạn song song
def rule_10(A: Angle, B: Angle) -> Relation:
    rel = Relation("SO_LE_TRONG", A, B)
    eq = Eq(A.symb, B.symb)
    if Relation.exist(rel) and Cobj.equation_true(eq):
        new_rel = Relation.make("SONG_SONG", A.line1, B.line1)
        Log.trace_obj(new_rel, "rule_10", [rel, eq])

# xét 2 góc so le trong
def rule_11(A: Angle, B: Angle):
    if A.is_staggered(B):
        new_rel = Relation.make("SO_LE_TRONG", A, B)
        Log.trace_obj(new_rel, "rule_11", [A, B])
            

# định lý về góc tam giác nhỏ trong tam giác lớn
def rule_12(tri1: Triangle, tri2: Triangle):
    ps = tri1.part_of(tri2)
    if ps is not None:
        E = Angle(ps[1]+ps[2]+ps[0])
        A = Angle(ps[1]+ps[3]+ps[0])
        ieq = Ceq.ieq(A.symb < E.symb)
        if ieq is not None:
            log1 = f"{ps[3]+ps[0]+ps[1]} > {ps[2]+ps[0]+ps[1]}"
            log2 = f"{ps[0]+ps[1]+ps[3]} > {ps[0]+ps[1]+ps[2]}"
            log3 = f"TRIANGLE {ps[3]+ps[0]+ps[1]}: {ps[1]+ps[3]+ps[0]} + {ps[3]+ps[0]+ps[1]} + {ps[0]+ps[1]+ps[3]} = 180"
            log4 = f"TRIANGLE {ps[2]+ps[0]+ps[1]}: {ps[1]+ps[2]+ps[0]} + {ps[2]+ps[0]+ps[1]} + {ps[0]+ps[1]+ps[2]} = 180"
            
            Log.trace_obj(ieq, "rule_12", [log1, log2, log3, log4])


# 2 cạnh bằng nhau => tam giác cân, 3 cạnh => đều
def rule_13(a: Line, b: Line):
    if a.is_equal(b) and a.is_connect(b):
        C, A, B = a.connect_points(b)
        tri = Triangle(A+B+C)
        c =  Line(B+C)
        if c.value is not None and b.value == c.value:
            rel = tri.set_equilateral() # Tam giác đều
            Log.trace_obj(rel, "rule_13", ["3 cạnh bằng nhau"] )
        else:
            rel = tri.set_isosceles(A) # Tam giác cân
            Log.trace_obj(rel, "rule_13", ["2 cạnh bằng nhau"] )

# 2 góc bằng nhau => tam giác cân, 3 góc => đều
def rule_14(A: Angle, B: Angle):
    if A.is_equal(B) and A.is_triangle(B):
        C = Angle.third_angle(A, B)
        tri = Triangle(A.name)
        if C.value is not None and B.value == C.value:
            rel = tri.set_equilateral() # Tam giác đều
            Log.trace_obj(rel, "angle:rule_02", ["3 góc bằng nhau"] )
        else:
            rel = tri.set_isosceles(C.name[1]) # Tam giác cân
            Log.trace_obj(rel, "angle:rule_02", ["2 góc bằng nhau"] )




#RULE2: 2 tam giác bằng nhau (c-c-c)
def rule_15(A: Triangle):
    for B in list(Cobj.triangles.values()):
        if A.name == B.name:
            continue
        a = 1
        for j, ej in B.edges.items():
            j_v1, j_v2 = B.get_other_vertexs(j)
            if A.e1.is_equal(ej) and A.e2.is_equal(B.edges[j_v2]) and A.e3.is_equal(B.edges[j_v1]):
                rel = A.set_equal(B, j, j_v2, j_v1)
                Log.trace_obj(rel, "rule_15", [f"{A.e1}={ej} {A.e2}={B.edges[j_v2]} {A.e3}={B.edges[j_v1]}"] )
                break
            if A.e1.is_equal(ej) and A.e2.is_equal(B.edges[j_v1]) and A.e3.is_equal(B.edges[j_v2]):
                rel = A.set_equal(B, B.next_v(j), B.next_v(j_v1), B.next_v(j_v2))
                Log.trace_obj(rel, "rule_15", [f"{A.e1}={ej} {A.e2}={B.edges[j_v1]} {A.e3}={B.edges[j_v2]}"] )
                break

class Crule:
    #c_line, c_angle, c_triangle = 0, 0, 0

    cached = []

    rules = [rule_01, rule_02, rule_03, rule_04, rule_05, rule_06, rule_08, rule_09, rule_10, rule_11, rule_12, rule_13, rule_14, rule_15]
    # line_rules = [rule_01]
    # angle_rules = [rule_02, rule_03, rule_04, rule_05, rule_06 ]
    # triangle_rules = [ rule_08, rule_09 ]
    # common_rules = [rule_10, rule_11, rule_12, rule_13, rule_14]
    
    def run_one():
        
        # c_line = len(Cobj.lines)
        # c_angle = len(Cobj.angles)
        # c_triangle = len(Cobj.triangles)

        # change = False
        # # line rules
        # if c_line > Crule.c_line:
        #     Crule.c_line = c_line
        #     for rule_func in Crule.line_rules:
        #         Crule.apply_rule(rule_func)
        #     change = True

        # # angle rules
        # if c_angle > Crule.c_angle:
        #     Crule.c_angle = c_angle
        #     for rule_func in Crule.angle_rules:
        #         Crule.apply_rule(rule_func)
        #     change = True

        # # triangle rules
        # if c_triangle > Crule.c_triangle:
        #     Crule.c_triangle = c_triangle
        #     for rule_func in Crule.triangle_rules:
        #         Crule.apply_rule(rule_func)
        #     change = True

        # for rule_func in Crule.common_rules:
        #     Crule.apply_rule(rule_func)

        change = False
        g_count = Cobj.count()
        if g_count > Cobj.c_obj:
            Cobj.c_obj = g_count
            for rule_func in Crule.rules:
                Crule.apply_rule(rule_func)
            change = True

        return change

    def run():
        change = True
        rule_depth = 0
        while change and rule_depth < 5:
            change = Crule.run_one()
            rule_depth += 1

    def apply_rule(rule_func):
        func_args = Crule.get_rule_args(rule_func)
        list_args = get_permutations(func_args[0], len(func_args))
        for args in list_args:
            # args_str = [str(arg.__dict__) for arg in args]
            # item = rule_func.__name__ + ''.join(args_str)
            # if item in Crule.cached:
            #     continue
            rule_func(*args)
            #Crule.cached.append(item)

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


