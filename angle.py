from __future__ import annotations
from copy import copy, deepcopy
from typing import List

from sympy import Eq, Symbol, symbols
from ceq import Ceq
from cobj import Cobj
from line import Line
from log import Log
from relation import Relation





class Angle(object):

    @staticmethod
    def third_angle(angle1: Angle, angle2: Angle):
        if angle1.line2.is_ident(angle2.line1) and angle1.name[0] == angle2.name[2]:
            return Angle(angle2.name[1]+angle2.name[2]+angle1.name[1])
        if angle2.line2.is_ident(angle1.line1) and angle2.name[0] == angle1.name[2]:
            return Angle(angle1.name[1]+angle1.name[2]+angle2.name[1])

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
        name = Cobj.get_angle_name(name)
        if not hasattr(self, 'name') or value is not None:
            self.name = name
            self.line1 = Line(name[0]+name[1])
            self.line2 = Line(name[1]+name[2])
            self.symb = Cobj.symb(self.ident_symb(), value)
            self.value = value
            self.attrs = None
            self.rules()

    def rules(self):
        if self.value is not None:
            rule_01(self)

    def is_triangle(self, angle2: Angle):
        if self.line2.is_ident(angle2.line1) and self.name[0] == angle2.name[2]:
            return True
        if angle2.line2.is_ident(self.line1) and angle2.name[0] == self.name[2]:
            return True

            
    def __str__(self):
        return f"GOC {self.name}"


    def is_ident(self, angle) -> bool:
        return self.name == angle.name

    def is_belong(self, angle: Angle) -> bool:
        if self.line1.is_belong(angle.line1) and self.line2.is_belong(angle.line2):
            return True
        return False

    def is_belongs(self, angle: Angle) -> bool:
        if self.line1.is_belongs_bi(angle.line1) and self.line2.is_belongs_bi(angle.line2):
            return True
        return False

    def ident_symb(self):
        for angle in Cobj.angles.values():
            if self.name == angle.name:
                continue
            if self.is_belong(angle):
                return angle.name
            if angle.is_belong(self):
                return self.name
        return self.name
    
    def set_equal(self, angle: Angle):
        eq = Ceq(self.symb, angle.symb)
        if angle.value is not None:
            self.set_value(angle.value)
        elif self.value is not None:
            angle.set_value(self.value)

        self.rules()
        return eq
            

    def set_value(self, value):
        if value is not None:
            value = int(str(value))
            self.value = value
            Cobj.symb(self.ident_symb(), value)
            if self.value > 90:
                self.set_obtuse()
            self.rules()

    def is_equal(self, line: Angle):
        if self.value is not None and line.value is not None and self.value == line.value:
            return True
        return Ceq.eq_exist(Eq(self.symb, line.symb))

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

    def check_ieq(symb, expr):
        ieqs = Ceq.get_ieq_by_symb(symb)
        if len(ieqs) == 0:
            return False

        new_ieqs = Cobj.sub_ieq_with_knowns(ieqs)
        for new_ieq in new_ieqs:
            if new_ieq.equals(expr):
                return True
        return False

    def set_obtuse(self):
        self.attrs = "GOC_TU"
        return Relation.make("GOC_TU", self)


'''
RULES Nội Tại
'''
# 2 góc bằng nhau => tam giác cân, 3 góc => đều
def rule_01(A: Angle):
    if A.value is not None:
        for B in Cobj.angles.values():
            if B.value is not None and B.value == A.value:
                Ceq(A.symb, B.symb)
