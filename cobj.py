from __future__ import annotations
from copy import copy
from typing import List
from unittest import result

# from angle import Angle
# from line import Line
# from point import Point
# from triangle import Triangle

from sympy import  Eq, Symbol, solve, symbols

from utils import next_alpha

class Cobj:
    
    triangles = {}
    angles = {}
    lines = {}
    points = {}

    symbs = {}
    eqs = []
    ieqs = []
    relations = []

    hypo = {}
    knowns = {}
    c_obj = 0
    
    def symb(name, value = None, positive=True):
        # if type(value) in [int, float]:
        #     if name in Cobj.symbs.keys():
        #         # update all equations with new value
        #         a_symbol = Cobj.symbs[name]
        #         for i, a_eq in enumerate(Cobj.eqs):
        #             Cobj.eqs[i] = a_eq.subs(a_symbol, value)

        #     Cobj.symbs[name] = value
        # elif name not in Cobj.symbs.keys():
        #     Cobj.symbs[name] = symbols(name, positive=positive)

        if name not in Cobj.symbs.keys():
            Cobj.symbs[name] = symbols(name, positive=positive)
        if type(value) in [int, float]:
            Cobj.hypo[name] = value
            Cobj.knowns[name] = value
        
        return Cobj.symbs[name]

    def reset_state():
        Cobj.triangles = {}
        Cobj.angles = {}
        Cobj.lines = {}
        Cobj.points = {}

        Cobj.symbs = {}
        Cobj.eqs = []
        Cobj.ieqs = []
        Cobj.relations = []

        Cobj.hypo = {}
        Cobj.knowns = {}

        Cobj.c_obj = 0

    def count():
        return (len(Cobj.triangles) + len(Cobj.angles) + len(Cobj.lines) + len(Cobj.points) + len(Cobj.symbs)
        + len(Cobj.eqs) + len(Cobj.ieqs) + len(Cobj.relations) + len(Cobj.hypo) + len(Cobj.knowns))
    
    def get_triangle(name):
        tri_name = None
        for a_name in Cobj.triangles.keys():
            if name[0] in a_name and name[1] in a_name and name[2] in a_name:
                tri_name = a_name

        if tri_name is not None:
            return Cobj.triangles[tri_name]

    
    def triangle_exist(name: str):
        triangle = Cobj.get_triangle(name)
        return triangle is not None

    def tri_name(name):
        min_value = min(name)
        min_index = name.index(min_value)
        result = name[min_index] + name[(min_index+1)%3] + name[(min_index+2)%3]
        return result
        #return sort_name(name)

    def is_in_triangle(p_name: str):
        for tri in Cobj.triangles.values():
            if hasattr(tri, "points") and p_name in tri.points.keys():
                return True
        return False

    
    def get_angle(name: str):
        angle_name = Cobj.get_angle_name(name)
        return Cobj.angles[angle_name]

    
    def get_angle_name(name):
        triangle = Cobj.get_triangle(name)
        if triangle is not None:
            angle_name = triangle.angle_name(name[1])
        else:
            angle_name = name
        return angle_name
    
    def set_angle(angle):
        if not Cobj.angle_exist(angle.name):
            Cobj.angles[angle.name] = angle

    
    def angle_exist(name: str) -> bool:
        angle_name = Cobj.get_angle_name(name)
        return angle_name in Cobj.angles.keys()

    def unset_angle(name):
        angle = Cobj.get_angle(name)
        angle.value = None
        angle.symb = symbols(name, positive=True)

    def get_line(name: str) -> str:
        name_op = name[-1]+name[0]
        if name in Cobj.lines.keys():
            return Cobj.lines[name]
        if name_op in Cobj.lines.keys():
            return Cobj.lines[name_op]

    def line_exist(name: str) -> bool:
        return Cobj.get_line(name) is not None
        

    def get_rd_ray():
        c = "x"
        while Cobj.ray_exist(c):
            c = next_alpha(c)
        return c

    def ray_exist(name):
        for line in Cobj.lines.values():
            if line.name[1] == name:
                return True
        return False

    def init_hypo():
        # if len(Cobj.hypo) == 0:
        #     for key, value in Cobj.symbs.items():
        #         if not isinstance(value, Symbol) :
        #             Cobj.hypo[key] = value
        #             Cobj.knowns[key] = value
        for key, value in Cobj.hypo.items():
            if not isinstance(value, Symbol) :
                Cobj.knowns[key] = value
        return Cobj.knowns
    
    
    def get_unknown():
        unknows = {}
        for key, a_symbol in Cobj.symbs.items():
            if key not in Cobj.knowns.keys():
                unknows[key] = a_symbol
        return unknows

    
    def count_known(eq: Eq) -> int:
        count = 0
        for a_symbol in eq.free_symbols:
            if str(a_symbol) in Cobj.knowns.keys():
                count += 1
        return count

    
    def count_unknown(eq: Eq) -> int:
        count = 0
        for a_symbol in eq.free_symbols:
            if str(a_symbol) not in Cobj.knowns.keys():
                count += 1
        return count

    
    def subs_eqs_with_hypo():
        equations = []
        for a_eq in Cobj.eqs:
            new_eq = a_eq
            for a_symbol in a_eq.free_symbols:
                if str(a_symbol) in Cobj.knowns.keys():
                    new_eq = new_eq.subs(a_symbol, Cobj.knowns[str(a_symbol)])
                
            equations.append(new_eq)

        eqs = [eq for eq in equations if eq != True and eq != False]
        return eqs

    def sub_ieq_with_knowns(ieqs):
        new_ieqs = []
        for ieq in ieqs:
            new_ieq = copy(ieq)
            for a_symbol in ieq.free_symbols:
                if str(a_symbol) in Cobj.knowns.keys():
                    new_ieq = new_ieq.subs(a_symbol, Cobj.knowns[str(a_symbol)])
                    if new_ieq != True and new_ieq != False:
                        new_ieqs.append(new_ieq)
            
        return new_ieqs

    def get_simple_equations() -> List[Eq]:
        simple_eqs = []
        for a_eq in Cobj.eqs:
            if Cobj.count_known(a_eq) == len(a_eq.free_symbols) - 1:
                simple_eqs.append(a_eq)

        return simple_eqs

    def equation_true(equation: Eq) -> bool:
        new_eq = copy(equation)
        for a_symbol in equation.free_symbols:
            if str(a_symbol) in Cobj.knowns.keys():
                new_eq = new_eq.subs(a_symbol, Cobj.knowns[str(a_symbol)])
        return new_eq == True

    def not_in_hypo(symbs) -> List[str]:
        results = []
        if type(symbs) == str:
            symbs = [symbs]
        for a_symb in symbs:
            if str(a_symb) not in Cobj.hypo.keys():
                results.append(str(a_symb))
        return results

    def get_rel_equations(symb):
        eqs= []
        for a_eq in Cobj.eqs:
            if symb in a_eq.free_symbols and a_eq != True and a_eq != False:
                eqs.append(a_eq)
                continue
        return eqs
    