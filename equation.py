from sympy import Eq, latex, Symbol

class Equation:
    def __init__(self, lhs, rhs, id=""):
        self.lhs = lhs
        self.rhs = rhs
        self.id = id
        self.eq = Eq(self.lhs, self.rhs)
        self.free_symbols = self.eq.free_symbols

    def get_latex(self):
        return latex(self.eq)
