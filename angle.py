from __future__ import annotations
from copy import copy, deepcopy
from typing import List

from sympy import Symbol, symbols
from ceq import Ceq
from cobj import Cobj
from line import Line
from log import Log
from relation import Relation




class Angle(object):

    def __new__(cls, name, value = None):
        #obj = Symbol.__new__(cls, name, positive=True)

        if len(name) != 3:
            raise Exception("Create Angle Error. Angle name must be 3 characters")

        name = Cobj.get_angle_name(name)

        if name not in Cobj.angles.keys():
            obj = object.__new__(cls)
            Cobj.angles[name] = obj
        return Cobj.angles[name]

    def __init__(self, name, value = None):
        if not hasattr(self, 'name') or value is not None:
            self.name = name
            self.line1 = Line(name[0]+name[1])
            self.line2 = Line(name[1]+name[2])
            self.symb = Cobj.symb(self.ident_symb(), value)
            self.value = value
            self.run_rules()

    def run_rules(self):
        #self.line1.run_rules()
        #self.line2.run_rules()
        rule_01(self)
        rule_02(self)
        rule_03(self)
        rule_04(self)
        rule_05(self)

    @staticmethod
    def is_triangle(angle1: Angle, angle2: Angle):
        if angle1.line2.is_ident(angle2.line1) and angle1.name[0] == angle2.name[2]:
            return True
        if angle2.line2.is_ident(angle1.line1) and angle2.name[0] == angle1.name[2]:
            return True

    @staticmethod
    def third_angle(angle1: Angle, angle2: Angle):
        if angle1.line2.is_ident(angle2.line1) and angle1.name[0] == angle2.name[2]:
            return Angle(angle2.name[1]+angle2.name[2]+angle1.name[1])
        if angle2.line2.is_ident(angle1.line1) and angle2.name[0] == angle1.name[2]:
            return Angle(angle1.name[1]+angle1.name[2]+angle2.name[1])

            
    def __str__(self):
        return f"{self.name}"


    def is_ident(self, angle) -> bool:
        return self.name == angle.name
    

    def is_belongs(self, angle: Angle) -> bool:
        if self.line1.is_belongs_bi(angle.line1) and self.line2.is_belongs_bi(angle.line2):
            return True
        return False

    def ident_symb(self):
        for angle in Cobj.angles.values():
            if self.name == angle.name:
                continue
            if self.is_belongs(angle):
                return angle.name
        return self.name
    
    def set_equal(self, angle: Angle):
        if angle.value is not None:
            self.set_value(angle.value)
        elif self.value is not None:
            angle.set_value(self.value)
        else:
            Ceq(self.symb, angle.symb)

    def set_value(self, value):
        self.value = value
        Cobj.symb(self.name, value)

    # góc kề
    def is_adjacent(self, angle) -> bool:
        if self.name[1] != angle.name[1] or self.is_belongs(angle):
            return False

        if Cobj.is_in_triangle(self.name[1]):
            return False

        if ((self.line2.is_belongs_bi(angle.line1) and not self.line1.is_belongs_bi(angle.line2))
        or (self.line1.is_belongs_bi(angle.line2) and not self.line2.is_belongs_bi(angle.line1))):
            return True

        return False
        

    def get_adjacent_parent(self, angle: Angle) -> Angle:
        if not self.is_adjacent(angle) and self.is_complementary(angle):
            return False

        if self.line2.is_belongs_bi(angle.line1):
            name = self.name[0] + self.name[1] + angle.name[2]
            return Angle(name)
        if angle.line2.is_belongs_bi(self.line1):
            name = angle.name[0] + angle.name[1] + self.name[2]
            return Angle(name)

    def is_adjacent_parent(self, angle: Angle) -> bool:
        if self.name[1] != angle.name[1]:
            return False

        if (self.line2.is_belongs_bi(angle.line2) or self.line1.is_belongs_bi(angle.line1)) and Ceq.ieq_exist(self.symb > angle.symb):
            return True

    # góc kề bù
    def is_complementary(self, angle) -> bool:
        if not self.is_adjacent(angle):
            return False
        
        if self.line1.is_cont(angle.line2) or self.line2.is_cont(angle.line1):
            return True

        return False

    # góc so le trong
    def is_staggered(self, angle) -> bool:
        if self.name[1] == angle.name[1]:
            return False

        if self.line1.is_ident(angle.line1) or self.line2.is_ident(angle.line2):
            return True
        return False




'''
RULES Nội Tại
'''

# tạo tam giác từ góc và cạnh đối diện
def rule_01(A: Angle):
    from triangle import Triangle
    for b in list(Cobj.lines.values()):
        if (A.name[0] == b.name[0] and A.name[2] == b.name[1]) or (A.name[0] == b.name[1] and A.name[2] == b.name[0]):
                tri_name = Cobj.tri_name(A.name)
                if not Cobj.triangle_exist(tri_name):
                    Triangle(tri_name)

# xét 2 góc bằng nhau từ 2 cạnh
def rule_02(A: Angle):
    for B in list(Cobj.angles.values()):
        if A.is_belongs(B):
            A.set_equal(B)

# xét 2 góc kề -> tổng = góc lớn
def rule_03(A: Angle):
    for B in list(Cobj.angles.values()):
        if A.is_adjacent(B) and not A.is_complementary(B):
            adj_angle = A.get_adjacent_parent(B)
            Ceq(A.symb + B.symb, adj_angle.symb)
            Ceq.ieq(A.symb < adj_angle.symb)
            Ceq.ieq(B.symb < adj_angle.symb)

# góc tù
def rule_04(A: Angle):
    if A.value is not None and A.value > 90:
        Relation.make("GOC_TU", A)
        return

    ieq = Ceq.get_ieq_by_symb(A.symb)
    if ieq is not None:
        new_ieq = Cobj.sub_ieq_with_knowns(ieq)
        if new_ieq != True and new_ieq != False and new_ieq.equals(A.symb > 90):
            rel = Relation.make("GOC_TU", A)
            if rel is not None:
                Log.trace_rule(rel, "rule_04", [ieq] )

# xét 2 góc kề bù -> tổng = 180
def rule_05(A: Angle):
    for B in list(Cobj.angles.values()):
        if A.is_complementary(B):
            Ceq(A.symb + B.symb, 180)