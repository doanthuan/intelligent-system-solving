from inspect import _void
from platform import release
from queue import Queue
from unittest import result
from sympy import N, Symbol, solve, symbols
from copy import copy, deepcopy

import sympy
from angle import Angle
from equation import Equation
from line import Line
from relation import Relation
from ruleobj import IfStm, Rule
from utils import flat_list, remove_duplicates

# Tập C
g_angles = {}

g_equations = []
g_symbols = {}
g_hypo = {}
g_knowns = {}

g_trace_paths = {}

'''
SOLVE COMPARE
'''
g_graph = {}
def load_graph():
    global g_graph
    g_graph = {}
    for symbol_row in g_symbols.keys():
        g_graph[symbol_row] = {}
        for symbol_col in g_symbols.keys():
            if symbol_col == symbol_row:
                continue
            #g_graph[symbol_row][symbol_col] = []
            for a_eq in g_equations:
                free_symbols_str = [str(a_sym) for a_sym in a_eq.free_symbols]
                if symbol_row in free_symbols_str and symbol_col in free_symbols_str:
                    if symbol_col not in g_graph[symbol_row]:
                        g_graph[symbol_row][symbol_col] = []
                    g_graph[symbol_row][symbol_col].append(a_eq)
            


# def get_rel_equations(symbol):
#     eqs = []
#     for a_eq in g_equations:
#         if a_eq in eqs:
#             continue
#         if symbol in a_eq.free_symbols:
#             eqs.append(a_eq)
#     return eqs

# def get_rel_symbols(from_symbol, knowns = []):
#     rel_symbols = []
#     rel_eqs = get_rel_equations_ex(from_symbol)
#     for eq in rel_eqs:
#         for rel_symbol in eq.free_symbols:
#             if rel_symbol != from_symbol and not check_in_knowns(rel_symbol, eq, knowns):
#                 rel_symbols.append(rel_symbol)
        
#     # remove duplicates
#     return remove_duplicates(rel_symbols)

# def get_connect_equations(to_symbol, from_symbol):
#     paths = []
#     rel_eqs = get_rel_equations(from_symbol)
#     for eq in rel_eqs:
#         if to_symbol in eq.free_symbols:
#             paths.append(eq)
#     return paths


def get_rel_equations(symbol):
    return flat_list(g_graph[str(symbol)].values())

def get_rel_symbols(from_symbol, knowns = []):
    results = []
    for symbol in g_graph[str(from_symbol)].keys():
        if isinstance(g_symbols[symbol], Symbol) and not check_in_knowns(symbol, g_graph[str(from_symbol)][symbol][0], knowns):
            results.append(g_symbols[symbol])
    return results

def get_connect_equations(to_symbol, from_symbol):
    if str(to_symbol) in g_graph[str(from_symbol)].keys():
        return g_graph[str(from_symbol)][str(to_symbol)]
    return []

def check_in_knowns(rel_symbol, eq, knowns):
    for kn in knowns:
        if type(kn) == list:
            if rel_symbol == kn[0] and (eq == kn[1] or 'ROOT' == kn[1]):
                return True
    
    if type(rel_symbol) == str:
        knowns_str = [str(kn) for kn in knowns]
        return rel_symbol in knowns_str
    else:
        return rel_symbol in knowns


def solve_rel_symbol(rel_symbol, from_symbol, sol_symbols, knowns):
    rel_eqs = get_connect_equations(rel_symbol, from_symbol)
    for eq in rel_eqs:
        solve_equation_symbol(eq, rel_symbol, sol_symbols)
        knowns.append((rel_symbol, eq))

def solve_equation_symbol(eq, rel_symbol, sol_symbols):
    # subs with all posible solved symbols
    sol_eqs = get_eq_subs(0, eq.eq, rel_symbol, list(eq.free_symbols), sol_symbols)
    for a_eq in sol_eqs:        
        result = solve(a_eq,[rel_symbol])
        add_result(sol_symbols, rel_symbol, result)

def add_result(sol_symbols, a_symbol, result):
    if result == True or len(result) == 0:
        return

    if str(a_symbol) not in sol_symbols:
        sol_symbols[str(a_symbol)] = [result[0]]
    else:
        results = sol_symbols[str(a_symbol)]
        results.append(result[0])
        results = remove_duplicates(results)
        sol_symbols[str(a_symbol)] = results


def get_eq_subs(index, cur_eq, rel_symbol, eq_symbols, sol_symbols):
    new_eqs = []
    a_sym = eq_symbols[index]
    if str(a_sym) in sol_symbols.keys() and a_sym != rel_symbol:
        solutions = sol_symbols[str(a_sym)]
        for sol in solutions:
            new_eq = deepcopy(cur_eq)
            new_eq = new_eq.subs(a_sym, sol) 
            if index < len(eq_symbols) -1:
                new_eqs_subs = get_eq_subs(index+1, new_eq, rel_symbol, eq_symbols, sol_symbols)
                new_eqs.extend(new_eqs_subs)
            else:
                new_eqs.append(new_eq)
    else:
        new_eq = deepcopy(cur_eq)
        if index < len(eq_symbols) -1:
            new_eqs_subs = get_eq_subs(index+1, new_eq, rel_symbol, eq_symbols, sol_symbols)
            new_eqs.extend(new_eqs_subs)
        else:
            new_eqs.append(new_eq)
    return new_eqs

