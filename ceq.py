# from angle import Angle
# from line import Line
# from point import Point
# from triangle import Triangle


from sympy import Eq

class Ceq:

    eqs = []
    
    def __new__(cls, lhs, rhs, id=""):
        eq = Eq(lhs, rhs)
        if not Ceq.eq_exist(eq):
            Ceq.eqs.append(eq)
        return eq

    @staticmethod
    def eq(lhs, rhs):
        eq = Eq(lhs, rhs)
        Ceq.eqs.append(eq)

    @staticmethod
    def set_eq(eq: Eq):
        Ceq.eqs.append(eq)

    @staticmethod
    def eq_exist(eq: Eq):
        for a_eq in Ceq.eqs:
            if a_eq.lhs == eq.lhs and a_eq.rhs == eq.rhs:
                return True
        return False



