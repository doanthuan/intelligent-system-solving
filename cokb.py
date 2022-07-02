from inspect import _void
from queue import Queue
from typing import List, Union
from sympy import  Eq, Symbol, solve, symbols
from copy import copy, deepcopy
from angle import Angle

from ceq import Ceq
from clog import Clog
from cobj import Cobj
from crule import Crule
from relation import Relation
from solver_compare import SolverCompare
from utils import flat_list, remove_duplicates

class Cokb:
       
    def solve_unknown():
        unknowns = Cobj.get_unknown()
        eqs = Cobj.subs_eqs_with_hypo()
        if len(eqs) < len(unknowns):
            return False # num var > num eq -> can not solve

        result = solve(eqs, list(unknowns.values()))
        if len(result) > 0:
            for sol_symbol, value in result.items():
                Cobj.knowns[str(sol_symbol)] = value
                Clog.trace_paths[str(sol_symbol)] = eqs
            return True
        else:
            return False
    
    def solve_equation(a_eq):
        sol_symbol = None
        new_eq = copy(a_eq)
        for a_symbol in a_eq.free_symbols:
            if str(a_symbol) in Cobj.knowns.keys():
                new_eq = new_eq.subs(a_symbol, Cobj.knowns[str(a_symbol)]) 
            else:
                sol_symbol = a_symbol

        if sol_symbol is None:
            return None, None

        sol_value = solve(new_eq, sol_symbol)
        if len(sol_value) == 0:
            return None, None

        Cobj.knowns[str(sol_symbol)] = sol_value[0]

        #trace symbol
        Clog.trace_paths[str(sol_symbol)] = a_eq

        return sol_symbol, sol_value[0]

    
    def bfs(target = None):


        # duyet
        step = 1
        while step < 100:

            # check if all targets are found
            if target is not None and str(target) in Cobj.knowns.keys():
                Clog.print_solution(target)
                return True
            
            # tìm những equation giải được ngay
            rel_eqs = Cobj.get_simple_equations()
            if len(rel_eqs) == 0 and target is not None:
                # not found -> try to solve unknown with all related equations
                if not Cokb.solve_unknown():
                    return False
            else:    
                for a_eq in rel_eqs:
                    Cokb.solve_equation(a_eq)

            step += 1  

    
    def solve_relation(relation: Relation) -> bool:

        Cokb.bfs()

        # duyet
        step = 1
        while step < 10:

            Crule.apply_rules()

            # check if all targets are found
            if Relation.relation_exist(relation):
                print("FOUND")
                # print trace rules
                Clog.print_trace_rels(relation)
                return True

            step += 1  

        return False


    def solve_find_compare(target_symbol):
        solver = SolverCompare(Cobj.symbs, Cobj.eqs)

        unknown_symbols = Cobj.get_unknown()
        for a_symbol in unknown_symbols.values():
            if str(a_symbol) == str(target_symbol):
                continue
            if Cobj.angle_exist(str(target_symbol)) and Angle(str(target_symbol)).equal(Angle(str(a_symbol))):
                continue

            success, logs = solver.solve_compare(a_symbol, target_symbol)

            if type(success) == int and success == 0:
                print("FOUND")
                Clog.print_logs(logs)
                break