from __future__ import annotations
from typing import List

from sympy import Symbol, symbols
from cobj import Cobj
from line import Line

class Angle:

    def from_lines(a: Line, b: Line):
        p1, cp, p2 = a.get_points(b)
        return Angle(p1+cp+p2)

    def __new__(cls, name, value = None):
        #obj = Symbol.__new__(cls, name, positive=True)

        if len(name) != 3:
            raise Exception("Create Angle Error. Angle name must be 3 characters")

        name = Cobj.get_angle_name(name)

        if value is not None or name not in Cobj.angles.keys():
            obj = object.__new__(cls)
            obj.name = name
            obj.value = value
            obj.line1 = Line(name[0]+name[1])
            obj.line2 = Line(name[1]+name[2])
            obj.symb = Cobj.symb(name, value)
            Cobj.angles[name] = obj
        return Cobj.angles[name]

    def __str__(self):
        return f"{self.name}"


    def identical(self, angle) -> bool:
        if self.name == angle.name:
            if self.value is not None and angle.value is not None:
                return self.value == angle.value
            return True

        return False

    def equal(self, angle) -> bool:
        c_lines = self.get_common_lines(angle)
        return len(c_lines) == 2

    def get_common_lines(self, angle) -> List[Line]:
        results = []
        if self.line1.is_belongs(angle.line1) or self.line1.is_belongs(angle.line2):
            results.append(self.line1)
        if self.line2.is_belongs(angle.line1) or self.line2.is_belongs(angle.line2):
            results.append(self.line2)
        return results

    def get_diff_lines(self, angle) -> List[Line]:
        results = []
        if not self.line1.is_belongs(angle.line1) or not self.line1.is_belongs(angle.line2):
            results.append(self.line1)
        if not self.line2.is_belongs(angle.line1) or not self.line2.is_belongs(angle.line2):
            results.append(self.line2)
            
        return results

    def is_adjacent(self, angle) -> bool:
        if self.name[1] != angle.name[1]:
            return False
        
        if self.equal(angle):
            return False

        if self.line2.is_belongs(angle.line1) or self.line1.is_belongs(angle.line2):
            return True

        return False
        

    def get_adjacent_angle(self, angle: Angle) -> Angle:
        if not self.is_adjacent(angle):
            return None

        if self.line2.is_belongs(angle.line1):
            line1 = self.line1
            line2 = angle.line2
        if self.line1.is_belongs(angle.line2):
            line1 = self.line2
            line2 = angle.line1
        
        return Angle.from_lines(line1, line2)

    def is_complementary(self, angle) -> bool:
        if not self.is_adjacent(angle):
            return False
        
        if self.line1.is_adjacent(angle.line1) or self.line1.is_adjacent(angle.line2) or self.line2.is_adjacent(angle.line1) or self.line2.is_adjacent(angle.line2):
            return True

        return False



        
