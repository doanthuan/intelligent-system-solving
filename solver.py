from inspect import _void
from platform import release
from queue import Queue
from typing import List, Union
from sympy import  Eq, Equality, Symbol, solve, symbols
from copy import copy, deepcopy

import sympy
from angle import Angle
from line import Line
from equation import Equation
from relation import Relation
from rule import IfStm, Rule
from utils import flat_list, remove_duplicates

# Tập C
g_angles = {}
g_lines = {}

g_equations = []

g_symbols = {}
g_hypo = {}
g_knowns = {}

g_trace_paths = {}

def symb(name, value = None):
    global g_equations, g_symbols
    if value is not None:
        if type(value) in [int, float] and name in g_symbols.keys():
            # update all equations with new value
            a_symbol = g_symbols[name]
            for i, g_eq in enumerate(g_equations):
                g_equations[i] = g_eq.subs(a_symbol, value)

        g_symbols[name] = value
        #load_graph()
    elif name not in g_symbols.keys():
        g_symbols[name] = symbols(name, positive=True)
        #load_graph()
    
    return g_symbols[name]

def angle(name, value = None):
    if value is not None or name not in g_angles.keys():
        angle = Angle(name, value)
        g_angles[name] = angle
        g_lines[angle.line1.name] = angle.line1
        g_lines[angle.line2.name] = angle.line2
    return symb(name, value)
    #return g_angles[name]

def line(name, value = None):
    if value is not None or name not in g_lines.keys():
        line = Line(name, value)
        g_lines[name] = line
    return symb(name, value)

def get_angle_obj(name):
    if name in g_angles.keys():
        return g_angles[name]

def set_equation(equation: Eq):
    global g_equations
    g_equations.append(equation)
    #load_graph()

def eq(lhs, rhs):
    global g_equations
    eq = Eq(lhs, rhs)
    g_equations.append(eq)
    #load_graph()

def get_hypo():
    global g_hypo
    if len(g_hypo) == 0:
        for key, value in g_symbols.items():
            if not isinstance(value, Symbol) :
                g_hypo[str(key)] = value
    return g_hypo

def get_known():
    global g_knowns, g_hypo
    if len(g_knowns) == 0:
        g_hypo = get_hypo()
        g_knowns = deepcopy(g_hypo)
    return g_knowns

def get_unknown():
    knowns = get_known()
    unknows = {}
    for key, a_symbol in g_symbols.items():
        if key not in knowns.keys():
            unknows[key] = a_symbol
    return unknows

def count_known(eq: Eq) -> int:
    count = 0
    for a_symbol in eq.free_symbols:
        if str(a_symbol) in g_knowns.keys():
            count += 1
    return count

def count_unknown(eq: Eq) -> int:
    count = 0
    for a_symbol in eq.free_symbols:
        if str(a_symbol) not in g_knowns.keys():
            count += 1
    return count

def get_all_symbols():
    return g_symbols

def get_eqs_with_hypo():
    equations = []
    for g_eq in g_equations:
        new_eq = g_eq
        for a_symbol in g_eq.free_symbols:
            if str(a_symbol) in g_knowns.keys():
                new_eq = new_eq.subs(a_symbol, g_knowns[str(a_symbol)])
            
        equations.append(new_eq)

    eqs = [eq for eq in equations if eq is not True]
    return eqs

def get_simple_equations() -> List[Eq]:
    simple_eqs = []
    for a_eq in g_equations:
        if count_known(a_eq) == len(a_eq.free_symbols) - 1:
            simple_eqs.append(a_eq)

    return simple_eqs

def solve_unknown():
    unknowns = get_unknown()
    eqs = get_eqs_with_hypo()
    if len(eqs) < len(unknowns):
        return False # num var > num eq -> can not solve

    result = solve(eqs, list(unknowns.values()))
    if len(result) > 0:
        for sol_symbol, value in result.items():
            g_knowns[str(sol_symbol)] = value
            g_trace_paths[str(sol_symbol)] = eqs
        return True
    else:
        return False

def solve_equation(a_eq):
    sol_symbol = None
    #new_eq = deepcopy(a_eq)
    new_eq = copy(a_eq)
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

    # g_symbols[str(sol_symbol)] = sol_value[0]
    g_knowns[str(sol_symbol)] = sol_value[0]

    #trace symbol
    g_trace_paths[str(sol_symbol)] = a_eq

    return sol_symbol, sol_value[0]

def is_in_hypo(a_symbol) -> bool:
    hypo = get_hypo()
    return str(a_symbol) in hypo.keys()

def print_trace_paths(cur_symb):

    if cur_symb not in g_trace_paths.keys():
        return

    eq = g_trace_paths[cur_symb]
    if isinstance(eq, Eq):
        for a_symbol in eq.free_symbols:
                if str(a_symbol) != cur_symb and not is_in_hypo(a_symbol):
                    print_trace_paths(str(a_symbol))
        print(f"{eq} => {cur_symb} =  {g_knowns[str(cur_symb)]}")

    elif isinstance(eq, list):
        print("From multiple equations:")
        for a_eq in eq:
            print(f"{a_eq}")
        print(f" => {cur_symb} =  {g_knowns[str(cur_symb)]}")

def print_solution(target):
    print("\n---TARGET---")
    print(f"{str(target)}:{g_knowns[str(target)]}")
    print("---HYPO:---")
    hypo = get_hypo()
    for key, value in hypo.items():
        print(f"{key}:{value}")
    print("---SOLUTION---")
    print_trace_paths(str(target))

def print_logs(logs):
    while len(logs) > 0:
        texts = logs.pop(0)
        print(texts)
    

def bfs(target = None):

    # khởi tạo tập known từ giả thuyết
    knowns = get_known()

    # duyet
    step = 1
    while step < 100:

        # check if all targets are found
        if target is not None and str(target) in knowns.keys():
            print_solution(target)
            return True
        
        # tìm những equation giải được ngay
        rel_eqs = get_simple_equations()
        if len(rel_eqs) == 0 and target is not None:
            # not found -> try to solve unknown with all related equations
            if not solve_unknown():
                return False
        else:    
            for a_eq in rel_eqs:
                solve_equation(a_eq)

        step += 1  

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

        rel_symbols = get_rel_symbols(checking_symbol, queue[:index])
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
                    c_path.append((a_eq, cur_symbol))
                    current_paths.append(c_path)
            else:
                current_paths.append([(a_eq, cur_symbol)])

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
    logs = []
    for step in path:
        eq = step[0]
        sol_symbol = step[1]
        logs.append(f"From {eq}")

        # substitute solved symbol
        for a_sym in eq.free_symbols:
            if str(a_sym) in sol_symbols.keys():
                eq = eq.subs(a_sym, sol_symbols[str(a_sym)]) 
                logs.append(f"replace {a_sym} = {sol_symbols[str(a_sym)]}")
        
        #result = solve_eq(eq, [sol_symbol])
        if eq == True:
            continue

        result = solve(eq, [sol_symbol])
        sol_symbols[str(sol_symbol)] = result[0]

        logs.append(f"=> {sol_symbol} = {result[0]}")

    return sol_symbols, logs


# Rules
# 1. Tiên đề Euclid Nếu 2 góc so le trong mà bằng nhau => 2 đoạn thẳng song song
A, B = Angle("xAB"), Angle("yBA")
rule_01 = Rule(
    [A, B],
    IfStm([Relation("SO_LE_TRONG", A, B), Eq(A, B)]),
    [Relation("SONG_SONG", A.line1, B.line1)],
    "01"
)

# 2. 3 đoạn thẳng khép kín => tạo thành tam giác
a, b, c = Line("AB"), Line("BC"), Line("CA")
rule_01 = Rule(
    [a, b, c],
    IfStm([Relation("SO_LE_TRONG", A, B), Eq(A, B)]),
    [Relation("SONG_SONG", A.line1, B.line1)],
    "01"
)


g_rules = {}
g_rules[rule_01.id] = rule_01

g_relations = []
g_trace_rels = []

def rule_01(A: Angle, B: Angle) -> Relation:
    if relation_exist(Relation("SO_LE_TRONG", A, B)) and equation_true(Eq(A.name, B.name)):
        pass

def add_relation(relation: Union[List[Relation], Relation]) -> _void:
    if isinstance(relation, list):
        for rel in relation:
            g_relations.append(relation)
    elif isinstance(relation, Relation):
        g_relations.append(relation)

def relation_exist(relation: Relation) -> bool:
    for rel in g_relations:
        if relation.equal(rel):
            return True

    return False

def equation_true(equation: Eq) -> bool:
    for a_symbol in equation.free_symbols:
        if str(a_symbol) not in g_knowns.keys():
            return False

    return True

def apply_rules():
    for rule in g_rules.values():
        apply_rule(rule)
        
def apply_rule(rule: Rule):
    if isinstance(rule.args[0], Angle) and isinstance(rule.args[1], Angle):
        g_angles_list = list(g_angles.values())
        for i in range(len(g_angles_list)):
            for j in range(i+1, len(g_angles_list)):
                angle1 = g_angles_list[i]
                angle2 = g_angles_list[j]
                result, trace_rels, trace_paths = check_if_stm(rule.if_stm, angle1, angle2)
                if result is True:
                    #apply then
                    for stm in rule.then_stm:
                        if isinstance(stm, Relation):
                            if isinstance(stm.left, Line) and isinstance(stm.right, Line):
                                new_rel = Relation(stm.name, angle1.line1, angle2.line1)
                                add_relation(new_rel)
                                
                                g_trace_rels.append((new_rel, rule.id, trace_rels, trace_paths))
                    

def print_trace_rels(relation: Relation):
    found = False
    for trace_rel_obj in g_trace_rels:
        new_rel, rule_id, trace_rels, trace_paths = trace_rel_obj
        if relation.equal(new_rel):
            for rel in trace_rels:
                print_trace_rels(rel)
            for a_path in trace_paths:
                print_trace_paths(a_path[0])
                print(f" => {a_path[1]}")

            print(f"Applied rule {rule_id} => {relation}")
            found = True
    
    if not found: # not found in trace, from hypo
        print(f"we have: {relation}")

            
def check_if_stm(if_stm: IfStm, obj1, obj2) -> bool:
    results = [False] * len(if_stm.cond_list)
    trace_rels = []
    trace_paths = []
    for idx, stm in enumerate(if_stm.cond_list):
        if isinstance(stm, Relation):
            rel = Relation(stm.name, obj1, obj2)
            if relation_exist(rel):
                results[idx] = True
                trace_rels.append(rel)
            
        if isinstance(stm, Eq):
            eq = Eq(g_symbols[obj1.name], g_symbols[obj2.name])
            if equation_true(eq):
                results[idx] = True
                if not is_in_hypo(obj1.name):
                    trace_paths.append((obj1.name, Eq(symbols(obj1.name), symbols(obj2.name))))
                if not is_in_hypo(obj2.name):
                    trace_paths.append((obj2.name, Eq(symbols(obj1.name), symbols(obj2.name))))

    
    if if_stm.operator == "AND":
        result = (False not in results)
    else:
        result = (True in results)
    return result, trace_rels, trace_paths