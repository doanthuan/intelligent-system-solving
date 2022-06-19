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
from rule import IfStm, Rule
from utils import flat_list, remove_duplicates

# Tập C
g_angles = {}

g_equations = []
g_symbols = {}
g_hypo = {}
g_knowns = {}

g_trace_paths = {}

def symb(name, value = None):
    global g_equations, g_symbols
    if value is not None:
        if not isinstance(value, Symbol):
            # update all equations with new value
            a_symbol = g_symbols[name]
            rel_eqs = get_rel_equations(g_symbols[name])
            for eq in rel_eqs:
                eq.eq = eq.eq.subs(a_symbol, value) 

        g_symbols[name] = value
    elif name not in g_symbols.keys():
        g_symbols[name] = symbols(name, positive=True)

    load_graph()
    return g_symbols[name]

def angle(name, value = None):
    
    if value is not None:
        g_angles[name] = Angle(name, value)
    elif name not in g_angles.keys():
        g_angles[name] = Angle(name)
    return symb(name, value)

def eq(lhs, rhs):
    global g_equations
    eq = Equation(lhs, rhs)
    g_equations.append(eq)
    load_graph()

def get_all_symbols():
    return g_symbols

def get_hypo():
    global g_hypo
    if len(g_hypo) == 0:
        for key, value in g_symbols.items():
            if not isinstance(value, Symbol) :
                g_hypo[str(key)] = value
    return g_hypo

def init_knowns():
    global g_knowns, g_hypo
    if len(g_knowns) == 0:
        g_hypo = get_hypo()
        g_knowns = deepcopy(g_hypo)
    return g_knowns

def get_candidate_equations():
    candidate_eqs = []
    for a_eq in g_equations:
        if count_knowns_symbol(a_eq.free_symbols) == len(a_eq.free_symbols) - 1:
            candidate_eqs.append(a_eq)

    return candidate_eqs

def count_knowns_symbol(symbols):
    count = 0
    for a_symbol in symbols:
        if str(a_symbol) in g_knowns.keys():
            count += 1
    return count

def solve_equation(a_eq):
    sol_symbol = None
    new_eq = deepcopy(a_eq.eq)
    for a_symbol in a_eq.free_symbols:
        if str(a_symbol) in g_knowns.keys():
            new_eq = new_eq.subs(a_symbol, g_knowns[str(a_symbol)]) 
        else:
            sol_symbol = a_symbol
        # if str(a_symbol) not in g_knowns.keys():
        #     sol_symbol = a_symbol

    if sol_symbol is None:
        return None, None

    sol_value = solve(new_eq, sol_symbol)
    if len(sol_value) == 0:
        return None, None

    #symb(str(sol_symbol), sol_value[0])
    g_symbols[str(sol_symbol)] = sol_value[0]
    g_knowns[str(sol_symbol)] = sol_value[0]

    #trace symbol
    g_trace_paths[str(sol_symbol)] = a_eq

    return sol_symbol, sol_value[0]

def check_symbol_hypo(a_symbol):
    hypo = get_hypo()
    return str(a_symbol) in hypo.keys()

def print_trace_paths(cur_symbol):
    if cur_symbol not in g_trace_paths.keys():
        return
    
    eq = g_trace_paths[cur_symbol]
    # get solved symbols
    for a_symbol in eq.free_symbols:
        if str(a_symbol) != cur_symbol and not check_symbol_hypo(a_symbol):
            print_trace_paths(str(a_symbol))

    print(f"{eq.eq} => {cur_symbol}")

def print_solution(target):
    print("\n---TARGET---")
    print(f"{str(target)}:{g_knowns[str(target)]}")
    print("---HYPO:---")
    hypo = get_hypo()
    for key, value in hypo.items():
        print(f"{key}:{value}")
    print("---SOLUTION---")
    print_trace_paths(str(target))
    

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
            
            #g_graph[symbol_row][symbol_col] = [a_eq for a_eq in g_equations if set([symbol_row, symbol_col]).issubset(a_eq.free_symbols)]


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


'''
SOLVE COMPARE 1
'''

def trace_symbols(start_symbol, target_symbol):

    queue = [start_symbol]

    trace_symbols = {}
    trace_symbols[str(start_symbol)] = "ROOT"

    # duyet
    found = False
    index = 0
    while index < len(queue):
        checking_symbol = queue[index]
        index += 1

        rel_symbols = get_rel_symbols(checking_symbol, queue)
        if len(rel_symbols) == 0:
            continue

        # goal reached
        if target_symbol in rel_symbols:
            print("FOUND TARGET")
            trace_symbol(target_symbol, checking_symbol, trace_symbols)
            found = True
            continue

        # store related symbols for next checking
        for a_symbol in rel_symbols:
            if a_symbol not in queue:
                queue.append(a_symbol)

            trace_symbol(a_symbol, checking_symbol, trace_symbols)

    if not found:
        print("Could not find target")
        return {}

    return trace_symbols

def trace_symbol( a_symbol, parent_symbol, trace_symbols):
    if str(a_symbol) in trace_symbols:
        trace_symbols[str(a_symbol)].append(parent_symbol)
    else:
        trace_symbols[str(a_symbol)] = [parent_symbol]

def get_trace_paths(trace_symbols, cur_symbol):
    if len(trace_symbols) == 0 or trace_symbols[str(cur_symbol)] == "ROOT":
        return []

    current_paths = []
    parent_symbols = trace_symbols[str(cur_symbol)]
    for a_parent in parent_symbols:
        eqs = get_connect_equations(a_parent, cur_symbol)
        for a_eq in eqs:
            child_paths = get_trace_paths(trace_symbols, a_parent)
            if len(child_paths) > 0:
                for c_path in child_paths:
                    c_path.append((a_eq.eq, cur_symbol))
                    current_paths.append(c_path)
            else:
                current_paths.append([(a_eq.eq, cur_symbol)])

    return current_paths

def get_path_symbols(path):
    # get path symbols
    path_symbols = []
    for step in path:
        eq = step[0]
        symlist = [a_symbol for a_symbol in eq.free_symbols]
        path_symbols.extend(symlist)
    return remove_duplicates(path_symbols)

def get_path_eqs(path):
    return [step[0] for step in path]

def solve_path(path):
    # get path symbols
    sol_symbols = {}
    for step in path:
        eq = step[0]
        sol_symbol = step[1]
        print(f"From {eq}")

        # substitute solved symbol
        for a_sym in eq.free_symbols:
            if str(a_sym) in sol_symbols.keys():
                eq = eq.subs(a_sym, sol_symbols[str(a_sym)]) 
                print(f"replace {a_sym} = {sol_symbols[str(a_sym)]}")
        
        result = solve(eq, [sol_symbol])
        sol_symbols[str(sol_symbol)] = result[0]

        print(f"=> {sol_symbol} = {result[0]}")

    return sol_symbols
    


# Rules
# 1. Tiên đề Euclid Nếu 2 góc so le trong mà bằng nhau => 2 đoạn thẳng song song
A, B = Angle("xAB"), Angle("yBA")
rule_01 = Rule(
    [A, B],
    IfStm([Relation("SO_LE_TRONG", A, B), Equation(A, B)]),
    [Relation("SONG_SONG", A.line1, B.line1)],
    "01"
)

g_rules = [rule_01]
g_relations = {}

def rule_01(A: Angle, B: Angle) -> Relation:
    if relation_exist(Relation("SO_LE_TRONG", A, B)) and equation_exist(Equation(A.name, B.name)):
        pass


def add_relation(relation: Relation) -> _void:
    g_relations[relation.name] = relation

def relation_exist(relation: Relation) -> bool:
    for rel in g_relations:
        if (
            (rel.name == relation.name and rel.left == relation.left and rel.right == relation.right) or
            (rel.name == relation.name and rel.left == relation.right and rel.right == relation.left)
        ):
            return True

    return False

def equation_exist(equation: Equation):
    for eq in g_equations:
        if (
            (eq.lhs == equation.lhs and eq.rhs == equation.rhs) or
            (eq.lhs == equation.rhs and eq.rhs == equation.lhs)
        ):
            return True

    return False

def apply_rules():
    for rule in g_rules:
        apply_rule(rule)
        
def apply_rule(rule: Rule):
    if isinstance(rule.args[0], Angle) and isinstance(rule.args[1], Angle):
        g_angles_list = g_angles.values()
        for i in range(len(g_angles_list)):
            for j in range(i, len(g_angles_list)):
                angle1 = g_angles_list[i], angle2 = g_angles_list[j]
                if check_if_stm(rule.if_stm, angle1, angle2):
                    #apply then
                    for stm in rule.then_stm:
                        if isinstance(stm, Relation):
                            if isinstance(stm.left, Line) and isinstance(stm.right, Line):
                                new_rel = Relation(stm.name, angle1.line1, angle2.line1)
                                add_relation(new_rel)

            
def check_if_stm(if_stm: IfStm, obj1, obj2) -> bool:
    results = [False] * len(if_stm.cond_list)
    for idx, stm in enumerate(if_stm.cond_list):
        if isinstance(stm, Relation):
            rel = Relation(stm.name, obj1, obj2)
            if relation_exist(rel):
                results[idx] = True
            
        if isinstance(stm, Equation):
            eq = Equation(g_symbols[obj1.name], g_symbols[obj2.name])
            if equation_exist(eq):
                results[idx] = True

    if if_stm.operator == "AND":
        return False not in results
    else:
        return True in results