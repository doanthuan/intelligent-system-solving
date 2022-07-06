# from angle import Angle
# from line import Line
# from point import Point
# from triangle import Triangle

from cobj import Cobj
from sympy import Eq

class Ceq:
    
    def __new__(cls, lhs, rhs, save=True):
        eq = Eq(lhs, rhs)
        Ceq.set_eq(eq)
        return eq

    def eq(lhs, rhs):
        eq = Eq(lhs, rhs)
        Ceq.set_eq(eq)

    def ieq(expr):
        if not Ceq.ieq_exist(expr):
            Cobj.ieqs.append(expr)

    def set_eq(eq: Eq):
        if eq == True or eq == False:
            return
        if not Ceq.eq_exist(eq):
            Cobj.eqs.append(eq)

    def eq_exist(eq: Eq):
        for a_eq in Cobj.eqs:
            if a_eq.lhs == eq.lhs and a_eq.rhs == eq.rhs:
                return True
        return False

    def ieq_exist(expr):
        for ieq in Cobj.ieqs:
            if ieq == True or ieq == False:
                continue
            if ieq.equals(expr):
                return True
        return False

    def get_ieq_by_symb(a_symbol):
        for ieq in Cobj.ieqs:
            if a_symbol in ieq.free_symbols:
                return ieq


