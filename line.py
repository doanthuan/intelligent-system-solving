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

    @staticmethod
    def get_connect_points(a, b, c) -> str:
        if a.is_connect(b) and b.is_connect(c) and c.is_connect(a):
            B = a.get_connect_point(b)
            C = b.get_connect_point(c)
            A = c.get_connect_point(a)
            return B,C,A

    @staticmethod
    def is_triangle(a, b, c):
        if a.is_connect(b) and b.is_connect(c) and c.is_connect(a):
            A,B,C = Line.get_connect_points(a,c,b)
            if A != B and A != C and B != C:
                return True
        return False

    @staticmethod
    def is_belongs(line1, line2) -> bool:
        if line1.is_belong(line2) or line2.is_belong(line1):
            return True
        return False

    def __new__(cls, name, value = None):
        name = sort_name(name)
        if value is not None or name not in Cobj.lines.keys():
            obj = object.__new__(cls)
            obj.name = name
            obj.v1 = Point(name[0])
            obj.v2 = Point(name[1])
            obj.value = value
            obj.symb = symbols(name, positive=True)
            obj.points = [obj.v1, obj.v2]
            Cobj.lines[name] = obj
        return Cobj.lines[name]

    def equal(self, line) -> bool:
        if (self.v1.name == line.v1.name and self.v2.name == line.v2.name) or (self.v1.name == line.v2.name and self.v2.name == line.v1.name):
            return True
        return False

    def is_belong(self, obj) -> bool:
        if self.equal(obj):
            return True
        
        point_names = [str(p) for p in obj.points]
        for a_point in self.points:
            if str(a_point) not in point_names:
                return False
        return True

    def add_point(self, point):
        if type(point) == str:
            point = Point(point)
        self.points.append(point)

    def is_connect(self, line) -> bool:
        if self.is_belong(line) or line.is_belong(self):
            return False

        if (
           (self.v1.name == line.v1.name and self.v2.name != line.v2.name) 
        or (self.v1.name == line.v2.name and self.v2.name != line.v1.name)
        or (self.v2.name == line.v1.name and self.v1.name != line.v2.name)
        or (self.v2.name == line.v2.name and self.v1.name != line.v1.name)
        ):
            return True
        return False

    def get_connect_point(self, line) -> str:
        if (self.v1.name == line.v1.name and self.v2.name != line.v2.name) or (self.v1.name == line.v2.name and self.v2.name != line.v1.name):
            return self.v1.name

        if (self.v2.name == line.v1.name and self.v1.name != line.v2.name) or (self.v2.name == line.v2.name and self.v1.name != line.v1.name):
            return self.v2.name

    def __str__(self):
        return f"{self.name}"