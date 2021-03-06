from __future__ import annotations
from typing import List

from sympy import Eq, symbols
from ceq import Ceq
from cobj import Cobj
from log import Log
from point import Point
from utils import get_permutations

class Line:

    @staticmethod
    def is_points_in_line(points) -> bool:
        for line in Cobj.lines.values():
            if line.point_exist(points):
                return True
        return False
    
    @staticmethod
    def from_points(points) -> bool:
        line = Line(points)
        line.refresh()

    @staticmethod
    def is_triangle(a: Line, b: Line, c: Line):
        if not a.is_connect(b) or c.is_ray:
            return False
        
        if (
            (Cobj.line_exist(a.v1.name + b.v2.name) and Line(a.v1.name + b.v2.name).is_belongs_bi(c))
         or (Cobj.line_exist(a.v2.name + b.v1.name) and Line(a.v2.name + b.v1.name).is_belongs_bi(c))
         ):
            return True
        return False

    @staticmethod
    def triangle_name(a: Line, b: Line) -> str:
        if not a.is_connect(b):
            return False
        A, B, C = a.connect_points(b)
        return A + B + C

    def __new__(cls, points: str, value = None):
        #name = sort_name(name)
        name = points[0] + points[-1]
        line = Cobj.get_line(name)
        if line is not None:
            return line

        obj = object.__new__(cls)
        Cobj.lines[name] = obj
        return obj

    def __init__(self, points: str, value = None):
        if not hasattr(self, 'name') or value is not None or len(points) > len(self.points):
            name = points[0] + points[-1]
            self.name = name
            self.v1 = Point(name[0])
            
            self.is_ray = str(name[1]).islower()
            self.v2 = Point(name[1]) if not self.is_ray else name[1]
            
            self.value = value
            self.symb = symbols(name, positive=True)
            self.points = [str(p) for p in points]
            self.m_p = None
            self.rules()
    
    def rules(self):
        if self.value is not None:
            rule_01(self)

    def __str__(self):
        return f"{self.name}"

    def set_equal(self, line: Line):
        Ceq(self.symb, line.symb)
        if line.value is not None:
            self.set_value(line.value)
        elif self.value is not None:
            line.set_value(self.value)

        self.rules()

    def set_value(self, value):
        self.value = int(value)
        Cobj.symb(self.name, value)
        self.rules()

    def is_equal(self, line: Line):
        if self.value is not None and line.value is not None and self.value == line.value:
            return True
        if self.is_ident(line):
            return True
        return Ceq.eq_exist(Eq(self.symb, line.symb))

    def is_ident(self, line: Line) -> bool:
        if self.name == line.name:
            return True
        return False

    # def is_reverse(self, line) -> bool:
    #     if self.is_ray or line.is_ray:
    #         return False

    #     if (self.v1.name == line.v2.name and self.v2.name == line.v1.name):
    #         return True
    #     return False

    # def get_reverse(self) -> Line:
    #     for line in Cobj.lines.values():
    #         if self.is_reverse(line):
    #             return line

    def get_other(self, point):
        if str(point) == self.v1.name:
            return str(self.v2)
        else:
            return self.v1.name

    def is_belong(self, line: Line) -> bool:
        # c_points = self.get_common_points(line)
        # return len(c_points) == len(self.points)
        if len(self.points) > len(line.points):
            return False
        for idx, p in enumerate(line.points):
            if self.points == line.points[idx : idx + len(self.points)]:
                return True
        return False
    
    def is_belongs(self, line: Line) -> bool:
        return self.is_belong(line) or line.is_belong(self)

    def is_belongs_bi(self, line: Line) -> bool:
        c_points = self.get_common_points(line)
        return len(c_points) >= 2

    def get_common_points(self, line: Line) -> str:
        c_points = list(set(self.points).intersection(line.points))
        return c_points

    # def is_in_line(self, line: Line) -> bool:
    #     c_points = self.get_common_points(line)
    #     return len(c_points) >= 2

    def is_cont(self, line: Line) -> bool:

        # if self.is_ray or line.is_ray:
        #     return False
        
        if self.is_ident(line):
            return False

        #if self.v1.name == line.v2.name or self.v2.name == line.v1.name:
        c_points = self.get_common_points(line)
        if len(c_points) == 1:
            p1, p2, p3 = self.connect_points(line)
            return Line.is_points_in_line([p1, p2, p3])
        return False

    def is_connect(self, line: Line) -> bool:
        # c_points = self.get_common_points(line)
        # return len(c_points) == 1
        if self.is_ray or line.is_ray:
            return False

        if self.is_cont(line) or self.is_belongs_bi(line):
            return False
            
        if self.v1.name == line.v2.name or self.v2.name == line.v1.name:
            return True
        return False

    def point_exist(self, points):
        if type(points) == str or type(points) == Point:
            points = [points]
            
        # point_names = [str(p) for p in self.points]
        for a_p in points:
            if str(a_p) not in self.points:
                return False
        return True

    def add_point(self, points: List[str]):
        if type(points) == str:
            points = [points]

        root = self.get_root()
        points.reverse()
        for point in points:
            if self.point_exist(point): 
                continue
            for idx, p in enumerate(root.points):
                if p == self.v1.name:
                    root.points.insert(idx+1, point)

        self.refresh()

    def refresh(self):
        root = self.get_root()
        for i in range(0, len(root.points) - 1):
            for j in range(i+1, len(root.points)):
                mid_points = root.points[i:j+1]
                Line(''.join(mid_points))

    def get_root(self):
        root = self
        for line in Cobj.lines.values():
            if root.is_belong(line):
                root = line
        return root   

    def add_midpoint(self, midpoint: str):
        self.m_p = midpoint
        self.add_point(midpoint)
        Line(self.name[0]+midpoint).set_equal(Line(midpoint+self.name[1]))
        # => trung tuy???n tam gi??c
        tri = self.get_triangle()
        if tri is not None:
            from_v = tri.get_other_vertexs(self.name)
            tri.set_median(from_v, midpoint)
        
    def get_triangle(self):
        for p in Cobj.points.values():
            tri_name = str(p) + self.name
            if Cobj.triangle_exist(tri_name):
                return Cobj.get_triangle(tri_name)
        return None

    def connect_points(self, line: Line) -> str:
        # if not self.is_connect(line):
        #     return None
        c_points = self.get_common_points(line)
        if len(c_points) != 1:
            return False
        c_p = c_points[0]
        if c_p == str(self.v2):
            return self.get_other(c_p) , c_p , line.get_other(c_p)
        else:
            return line.get_other(c_p) , c_p , self.get_other(c_p)


# Rule n???i t???i
# t???o tam gi??c t??? 3 c???nh
# def rule_01(a: Line):
#     from triangle import Triangle
#     for b in Cobj.lines.values():
#         if a.is_ident(b): continue
#         for c in Cobj.lines.values():
#             if a.is_ident(c) or b.is_ident(c): continue
#             list_args = get_permutations([a,b,c], 3)
#             for arg in list_args:
#                 a1, b1, c1 = arg[0], arg[1], arg[2]
#                 if Line.is_triangle(a1, b1, c1):
#                     tri_name = Line.triangle_name(a1, b1)
#                     if not Cobj.triangle_exist(tri_name):
#                         Triangle(tri_name)


def rule_01(a: Line):
    if a.value is not None:
        for b in list(Cobj.lines.values()):
            if b.value is not None and b.value == a.value:
                Ceq(a.symb, b.symb)
                    


