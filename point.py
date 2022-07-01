from sympy import Symbol
from cobj import Cobj


class Point:

    def __new__(cls, name):
        if name not in Cobj.points.keys():
            obj = object.__new__(cls)
            obj.name = name
            Cobj.points[name] = obj
        return Cobj.points[name]

    # def __init__(self, name: str):
    #     self.name = name

    def is_belong(self, line) -> bool:
        if self.name in line.belongs:
            return True

    def __str__(self):
        return f"{self.name}"