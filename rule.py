from sympy import Eq
from equation import Equation
from relation import Relation


class IfStm:
    def __init__(self, cond_list: list, operator = "AND") -> None:
        self.cond_list = cond_list
        self.operator = operator

    def print():
        pass

class Rule:
    def __init__(self, args: list, if_stm: IfStm, then_stm: list, id="") -> None:
        self.args = args
        self.if_stm = if_stm
        self.then_stm = then_stm
        self.id = id

    def __str__(self):
        obj1 = self.args[0]
        obj2 = self.args[1]
        for stm in self.if_stm.cond_list:
            if isinstance(stm, Relation):
                rel = Relation(stm.name, obj1, obj2)
                print(rel)
                
            if isinstance(stm, Eq):
                eq = Eq(obj1, obj2)
                print(eq)
                