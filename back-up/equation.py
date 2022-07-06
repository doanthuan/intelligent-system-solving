from sympy import Eq, latex, Symbol, symbols

class Equation:
    def __init__(self, lhs, rhs, id=""):
        self.lhs = lhs
        self.rhs = rhs
        self.id = id
        #new_eq = Eq(self.lhs, self.rhs)
        # for a_symbol in new_eq.free_symbols:
        #     new_eq = new_eq.subs(a_symbol, symbols(str(a_symbol)))
        self.eq = Eq(self.lhs, self.rhs)
        
        #self.free_symbols = self.eq.free_symbols

    def __str__(self):
        return f"{self.lhs} = {self.rhs}"

    def __repr__(self):
        return f"{self.lhs} = {self.rhs}"

    def get_latex(self):
        return latex(self.eq)
