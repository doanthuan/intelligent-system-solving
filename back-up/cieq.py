# from angle import Angle
# from line import Line
# from point import Point
# from triangle import Triangle

from cobj import Cobj
from sympy import Eq

class Cieq:
    
    def __new__(cls, expr):
        if Cieq.expr_exist(expr):
            return Cieq.get(expr)
            
        obj = object.__new__(cls)
        Cobj.ieqs.append(obj)

    def __init__(self, expr):
        self.expr = expr

    @staticmethod
    def ieq(expr):
        if not Cieq.ieq_exist(expr):
            Cobj.ieqs.append(expr)

    @staticmethod
    def expr_exist(expr):
        for a_ieq in Cobj.ieqs:
            if expr == a_ieq.expr:
                return True
        return False

    @staticmethod
    def get(expr):
        for a_ieq in Cobj.ieqs:
            if expr == a_ieq.expr:
                return a_ieq


