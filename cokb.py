from inspect import _void
from queue import Queue
from typing import List, Union
from sympy import  Eq, Symbol, solve, symbols
from copy import copy, deepcopy

from ceq import Ceq
from log import Log
from cobj import Cobj
from crule import Crule
from relation import Relation
from solver_compare import SolverCompare
from utils import flat_list, remove_duplicates
from angle import Angle


class Cokb:
       
    def solve_unknown():
        unknowns = list(Cobj.get_unknown().values())
        eqs = Cobj.subs_eqs_with_hypo()
        if len(eqs) < len(unknowns):
            return False # num var > num eq -> can not solve

        result = solve(eqs, unknowns)
        if len(result) > 0:
            for sol_symbol, value in result.items():
                Cobj.knowns[str(sol_symbol)] = value
                Log.trace_symbols[str(sol_symbol)] = Cobj.get_rel_equations(sol_symbol)
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
        Log.trace_symbols[str(sol_symbol)] = a_eq

        return sol_symbol, sol_value[0]

    # lan truyền
    def bfs():
        Log.reset()
        step = 1
        while step < 5:

            Crule.run()
            
            # tìm những equation giải được ngay
            rel_eqs = Cobj.get_simple_equations()
            if len(rel_eqs) == 0:
               Cokb.solve_unknown()
               return                    
            for a_eq in rel_eqs:
                Cokb.solve_equation(a_eq)

            step += 1

    def solve(target):
        Cokb.bfs()

        if isinstance(target, Symbol) and str(target) in Cobj.knowns.keys():
            Log.print_solution(target, False)
            return Log.logs

        if isinstance(target, Relation) and Relation.exist(target):
            Log.print_trace_objs(target)
            return Log.logs

        if isinstance(target, Eq) and Cobj.equation_true(target):
            Log.log(f"TARGET: {target}")
            for a_symbol in target.free_symbols:
                Log.print_trace_symbols(a_symbol)
            return Log.logs

        return []

    def solve_find_compare(target, ret = False):
        results = {}
        eqs = Cobj.subs_eqs_with_hypo()
        solver = SolverCompare(Cobj.symbs, eqs)

        unknown_symbols = Cobj.get_unknown()
        for a_symbol in unknown_symbols.values():
            if str(a_symbol) == str(target):
                continue
            if Cobj.angle_exist(str(target)) and Angle(str(target)).is_belongs(Angle(str(a_symbol))):
                continue

            success, result, logs = solver.solve_compare(a_symbol, target)
            if success:
                if not ret:
                    print("FOUND")
                    Log.print_logs(logs)
                    return logs
                else:
                    results[str(a_symbol)] = result

        return results
