from __future__ import annotations
from typing import List, Set

from sympy import symbols
from cobj import Cobj
from point import Point
from utils import sort_name


class Line:
    # def __init__(self, name: str, value = None):
    #     name = sort_name(name)
    #     if value is not None or name not in Cobj.lines.keys():
    #         self.name = name
    #         self.v1 = Point(name[0])
    #         self.v2 = Point(name[1])
    #         self.value = value
    #         self.symb = symbols(name, positive=True)
    #         self.points = [self.v1, self.v2]
    #         Cobj.lines[name] = self
    #     self = Cobj.lines[name]

    # @staticmethod
    # def get_connect_points(a: Line, b: Line, c: Line) -> Set[str]:
    #     if a.is_connect(b) and b.is_connect(c) and c.is_connect(a):
    #         C = b.get_connect_point(c)
    #         return a.v1.name, a.v2.name, C
    #     return ()

    # @staticmethod
    # def get_common_points(a: Line, b: Line, c: Line) -> List[str]:
    #     c_points = list(set(a.points) & set(b.points) & set(c.points))
    #     return c_points


    @staticmethod
    def is_points_in_line(points) -> bool:
        for line in Cobj.lines.values():
            if line.point_exist(points):
                return True
        return False

    def __new__(cls, name, value = None):
        #name = sort_name(name)
        if value is not None or name not in Cobj.lines.keys():
            obj = object.__new__(cls)
            obj.name = name
            obj.v1 = Point(name[0])
            obj.v2 = Point(name[1])
            obj.value = value
            obj.symb = symbols(name, positive=True)
            obj.points = [obj.v1.name, obj.v2.name]
            Cobj.lines[name] = obj
        return Cobj.lines[name]

    def __str__(self):
        return f"{self.name}"

    def identical(self, line: Line) -> bool:
        if (self.v1.name == line.v1.name and self.v2.name == line.v2.name) or (self.v1.name == line.v2.name and self.v2.name == line.v1.name):
            return True
        return False

    def get_other_point(self, point):
        if str(point) == self.v1.name:
            return self.v2.name
        else:
            return self.v1.name

    def is_belong(self, line: Line) -> bool:
        c_points = self.get_common_points(line)
        return len(c_points) == len(self.points)
    
    def is_belongs(self, line: Line) -> bool:
        c_points = self.get_common_points(line)
        return len(c_points) >= 2

    def is_adjacent(self, line: Line) -> bool:
        # c_points = self.get_common_points(line)
        # if len(c_points) != 1:
        #     return False
        # c_point = c_points[0]

        # p1 = self.get_other_point(c_point)
        # p2 = line.get_other_point(c_point)
        if self.v1.name == line.v2.name or self.v2.name == line.v1.name:
            p1, p2, p3 = self.get_points(line)
            return Line.is_points_in_line([p1, p2, p3])
        return False

    def point_exist(self, points):
        if type(points) == str or type(points) == Point:
            points = [points]
            
        # point_names = [str(p) for p in self.points]
        for a_p in points:
            if str(a_p) not in self.points:
                return False
        return True

    def add_point(self, point):
        if self.point_exist(point):
            return
            
        self.points.append(str(point))

        Line(self.v1.name + point)
        Line(point + self.v2.name)

    def is_connect(self, line: Line) -> bool:
        # c_points = self.get_common_points(line)
        # return len(c_points) == 1
        if self.is_adjacent(line) or self.is_belongs(line):
            return False
        if self.v1.name == line.v2.name or self.v2.name == line.v1.name:
            return True
        return False

    def get_points(self, line: Line) -> str:
        # if not self.is_connect(line):
        #     return None
        if self.v1.name == line.v2.name:
            return line.v1.name, self.v1.name, self.v2.name
        if self.v2.name == line.v1.name:
            return self.v1.name, self.v2.name, line.v2.name
        return None

    def get_common_points(self, line: Line) -> str:
        c_points = list(set(self.points).intersection(line.points))
        return c_points

