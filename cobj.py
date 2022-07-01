from __future__ import annotations

# from angle import Angle
# from line import Line
# from point import Point
# from triangle import Triangle

from sympy import  symbols

from ceq import Ceq

class Cobj:
    
    triangles = {}
    angles = {}
    lines = {}
    points = {}

    symbs = {}

    @staticmethod
    def symb(name, value = None, positive=True):
        if type(value) in [int, float]:
            if name in Cobj.symbs.keys():
                # update all equations with new value
                a_symbol = Cobj.symbs[name]
                for i, a_eq in enumerate(Ceq.eqs):
                    Ceq.eqs[i] = a_eq.subs(a_symbol, value)

            Cobj.symbs[name] = value
        elif name not in Cobj.symbs.keys():
            Cobj.symbs[name] = symbols(name, positive=positive)
        
        return Cobj.symbs[name]    

    @staticmethod
    def get_triangle(name):
        tri_name = Cobj.get_triangle_name(name)
        if tri_name is not None:
            return Cobj.triangles[tri_name]

    @staticmethod
    def get_triangle_name(name):
        for a_name in Cobj.triangles.keys():
            if name[0] in a_name and name[1] in a_name and name[2] in a_name:
                return a_name

    @staticmethod
    def get_angle(name: str):
        angle_name = Cobj.get_angle_name(name)
        return Cobj.angles[angle_name]

    @staticmethod
    def get_angle_name(name):
        triangle = Cobj.get_triangle(name)
        if triangle is not None:
            angle_name = triangle.angle_name(name[1])
        else:
            angle_name = name
        return angle_name

    @staticmethod
    def set_angle(angle):
        if not Cobj.angle_exist(angle.name):
            Cobj.angles[angle.name] = angle

    @staticmethod
    def angle_exist(name: str):
        angle_name = Cobj.get_angle_name(name)
        return angle_name in Cobj.angles.keys()

