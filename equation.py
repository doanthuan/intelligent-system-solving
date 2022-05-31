from sympy import Eq, latex, Symbol

class Equation:
    def __init__(self, lhs, rhs, id=""):
        self.lhs = lhs
        self.rhs = rhs
        self.id = id

    def get_eq(self):
        return Eq(self.lhs, self.rhs)

    def get_latex(self):
        return latex(self.get_eq())
