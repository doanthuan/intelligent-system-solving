from sympy import Symbol, symbols
from line import Line

class Angle(Symbol):
    def __new__(cls, name, value = None):
        #self = Symbol.__new__(self, name,  positive=True)
        obj = Symbol.__new__(cls, name, positive=True)
        obj.name = name
        obj.value = value
        obj.line1 = Line(name[1]+name[0])
        obj.line2 = Line(name[1]+name[2])
        return obj

    # def __init__(self, name, value = None):
    #     self.name = name
    #     self.value = value
    #     self.line1 = Line(name[1], name[0])
    #     self.line2 = Line(name[1], name[2])

    def equal(self, angle) -> bool:
        if self.name == angle.name:
            if self.value is not None and angle.value is not None:
                return self.value == angle.value
            return True

        return False

    def __str__(self):
        return f"{self.name}"

        
