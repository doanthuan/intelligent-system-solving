from sympy import Symbol, symbols
from cobj import Cobj
from line import Line

class Angle:
    def __new__(cls, name, value = None):
        #obj = Symbol.__new__(cls, name, positive=True)

        name = Cobj.get_angle_name(name)

        if value is not None or name not in Cobj.angles.keys():
            obj = object.__new__(cls)
            obj.name = name
            obj.value = value
            obj.line1 = Line(name[1]+name[0])
            obj.line2 = Line(name[1]+name[2])
            obj.symb = Cobj.symb(name, value)
            Cobj.angles[name] = obj
        return Cobj.angles[name]

    # def __init__(self, name, value = None):
    #     self.name = name
    #     self.value = value
    #     # self.line1 = Cobj.line(name[1]+name[0])
    #     # self.line2 = Cobj.line(name[1]+name[2])
    #     self.symb = Symbol(name, positive=True)

    def identical(self, angle) -> bool:
        if self.name == angle.name:
            if self.value is not None and angle.value is not None:
                return self.value == angle.value
            return True

        return False

    def equal(self, angle) -> bool:
        if (
            (Line.is_belongs(self.line1, angle.line1) and Line.is_belongs(self.line2, angle.line2)) or
            (Line.is_belongs(self.line1, angle.line2) and Line.is_belongs(self.line2, angle.line1))
        ):
            return True

        return False

    def __str__(self):
        return f"{self.name}"

        
