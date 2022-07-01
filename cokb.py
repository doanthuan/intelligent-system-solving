from inspect import _void
from queue import Queue
from typing import List, Union
from sympy import  Eq, Symbol, solve, symbols
from copy import copy, deepcopy

from ceq import Ceq
from cobj import Cobj
from utils import flat_list, remove_duplicates

class Cokb:
    
    hypo = {}
    knowns = {}

    trace_paths = {}
    trace_rels = []

    @staticmethod
    def init_hypo():
        if len(Cokb.hypo) == 0:
            for key, value in Cobj.symbs.items():
                if not isinstance(value, Symbol) :
                    Cokb.hypo[key] = value
                    Cokb.knowns[key] = value
        return Cokb.knowns
    
    @staticmethod
    def get_unknown():
        unknows = {}
        for key, a_symbol in Cobj.symbs.items():
            if key not in Cokb.knowns.keys():
                unknows[key] = a_symbol
        return unknows

    @staticmethod
    def count_known(eq: Eq) -> int:
        count = 0
        for a_symbol in eq.free_symbols:
            if str(a_symbol) in Cokb.knowns.keys():
                count += 1
        return count

    @staticmethod
    def count_unknown(eq: Eq) -> int:
        count = 0
        for a_symbol in eq.free_symbols:
            if str(a_symbol) not in Cokb.knowns.keys():
                count += 1
        return count

    @staticmethod
    def subs_eqs_with_hypo():
        equations = []
        for a_eq in Ceq.eqs:
            new_eq = a_eq
            for a_symbol in a_eq.free_symbols:
                if str(a_symbol) in Cokb.knowns.keys():
                    new_eq = new_eq.subs(a_symbol, Cokb.knowns[str(a_symbol)])
                
            equations.append(new_eq)

        eqs = [eq for eq in equations if eq is not True]
        return eqs

    @staticmethod
    def get_simple_equations() -> List[Eq]:
        simple_eqs = []
        for a_eq in Ceq.eqs:
            if Cokb.count_known(a_eq) == len(a_eq.free_symbols) - 1:
                simple_eqs.append(a_eq)

        return simple_eqs

    @staticmethod
    def solve_unknown():
        unknowns = Cokb.get_unknown()
        eqs = Cokb.subs_eqs_with_hypo()
        if len(eqs) < len(unknowns):
            return False # num var > num eq -> can not solve

        result = solve(eqs, list(unknowns.values()))
        if len(result) > 0:
            for sol_symbol, value in result.items():
                Cokb.knowns[str(sol_symbol)] = value
                Cokb.trace_paths[str(sol_symbol)] = eqs
            return True
        else:
            return False

    @staticmethod
    def solve_equation(a_eq):
        sol_symbol = None
        #new_eq = deepcopy(a_eq)
        new_eq = copy(a_eq)
        for a_symbol in a_eq.free_symbols:
            if str(a_symbol) in Cokb.knowns.keys():
                new_eq = new_eq.subs(a_symbol, Cokb.knowns[str(a_symbol)]) 
            else:
                sol_symbol = a_symbol
            # if str(a_symbol) not in Cokb.knowns.keys():
            #     sol_symbol = a_symbol

        if sol_symbol is None:
            return None, None

        sol_value = solve(new_eq, sol_symbol)
        if len(sol_value) == 0:
            return None, None

        Cokb.knowns[str(sol_symbol)] = sol_value[0]

        #trace symbol
        Cokb.trace_paths[str(sol_symbol)] = a_eq

        return sol_symbol, sol_value[0]

    @staticmethod
    def is_in_hypo(a_symbol) -> bool:
        return str(a_symbol) in Cokb.hypo.keys()

    @staticmethod
    def equation_true(equation: Eq) -> bool:
        for a_symbol in equation.free_symbols:
            if str(a_symbol) not in Cokb.knowns.keys():
                return False
        return True

    @staticmethod
    def print_trace_paths(cur_symb):

        if cur_symb not in Cokb.trace_paths.keys():
            return

        eq = Cokb.trace_paths[cur_symb]
        if isinstance(eq, Eq):
            for a_symbol in eq.free_symbols:
                    if str(a_symbol) != cur_symb and str(a_symbol) not in Cokb.hypo.keys():
                        Cokb.print_trace_paths(str(a_symbol))
            print(f"{eq} => {cur_symb} =  {Cokb.knowns[str(cur_symb)]}")

        elif isinstance(eq, list):
            print("From multiple equations:")
            for a_eq in eq:
                print(f"{a_eq}")
            print(f" => {cur_symb} =  {Cokb.knowns[str(cur_symb)]}")

    @staticmethod
    def print_solution(target):
        print("\n---TARGET---")
        print(f"{str(target)}:{Cokb.knowns[str(target)]}")
        print("---HYPO:---")
        
        for key, value in Cokb.hypo.items():
            print(f"{key}:{value}")
        print("---SOLUTION---")
        Cokb.print_trace_paths(str(target))

    @staticmethod
    def print_logs(logs):
        while len(logs) > 0:
            texts = logs.pop(0)
            print(texts)
        
    @staticmethod
    def bfs(target = None):

        # khởi tạo tập known từ giả thuyết
        Cokb.init_hypo()

        # duyet
        step = 1
        while step < 100:

            # check if all targets are found
            if target is not None and str(target) in Cokb.knowns.keys():
                Cokb.print_solution(target)
                return True
            
            # tìm những equation giải được ngay
            rel_eqs = Cokb.get_simple_equations()
            if len(rel_eqs) == 0 and target is not None:
                # not found -> try to solve unknown with all related equations
                if not Cokb.solve_unknown():
                    return False
            else:    
                for a_eq in rel_eqs:
                    Cokb.solve_equation(a_eq)

            step += 1  

    
    
