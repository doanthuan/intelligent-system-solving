# from angle import Angle
# from line import Line
# from point import Point
# from triangle import Triangle


from sympy import Eq

class Ceq:

    eqs = []
    
    def __new__(cls, lhs, rhs, id=""):
        eq = Eq(lhs, rhs)
        Ceq.eqs.append(eq)
        return eq

    @staticmethod
    def eq(lhs, rhs):
        eq = Eq(lhs, rhs)
        Ceq.eqs.append(eq)

    @staticmethod
    def set_eq(eq: Eq):
        Ceq.eqs.append(eq)



