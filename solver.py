from sympy import Symbol, solve, symbols
from copy import deepcopy
from equation import Equation
from utils import remove_duplicates

g_equations = []
g_symbols = {}
g_knowns = {}
g_trace_paths = {}
g_graph = {}

def set_symbol(name, value = None):
    if value is not None:
        g_symbols[name] = value
    else:
        g_symbols[name] = symbols(name)

def set_equation(lhs, rhs):
    eq = Equation(lhs, rhs)
    g_equations.append(eq)

def get_all_symbols():
    return g_symbols

def get_hypo():
    gt = {}
    for key, value in g_symbols.items():
        if not isinstance(value, Symbol) :
            gt[str(key)] = value
    return gt

def init_knowns():
    global g_knowns
    if len(g_knowns) == 0:
        g_knowns = get_hypo()
    return g_knowns

def check_target_in_knowns(target):
    return str(target) in g_knowns.keys()

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

    if sol_symbol is None:
        return None, None
    
    sol_value = solve(new_eq, sol_symbol)[0]
    g_knowns[str(sol_symbol)] = sol_value

    #trace symbol
    g_trace_paths[str(sol_symbol)] = a_eq

    return sol_symbol, sol_value

def check_equation_exist(eq):
    for a_eq in g_equations:
        if a_eq.lhs == eq.lhs and a_eq.rhs == eq.rhs:
            return True

    return False

def check_symbol_exist(symbol):
    for a_symbol in g_symbols:
        if a_symbol == symbol:
            return True

    return False

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
    

def get_rel_equations(symbol):
    eqs = []
    for a_eq in g_equations:
        if a_eq in eqs:
            continue
        if symbol in a_eq.free_symbols:
            eqs.append(a_eq)
    return eqs

def get_rel_symbols(from_symbol, knowns = []):
    rel_symbols = []
    rel_eqs = get_rel_equations(from_symbol)
    for eq in rel_eqs:
        for rel_symbol in eq.free_symbols:
            if rel_symbol != from_symbol and not check_in_knowns(from_symbol, rel_symbol, knowns):
                rel_symbols.append(rel_symbol)
        
    # remove duplicates
    return remove_duplicates(rel_symbols)

def check_in_knowns(from_symbol, rel_symbol, knowns):
    for kn in knowns:
        if rel_symbol == kn[0] and (from_symbol == kn[1] or 'ROOT' == kn[1]):
            return True
    return False

def get_connect_equations(to_symbol, from_symbol):
    paths = []
    rel_eqs = get_rel_equations(from_symbol)
    for eq in rel_eqs:
        if to_symbol in eq.free_symbols:
            paths.append(eq)
    return paths

def solve_rel_symbol(rel_symbol, from_symbol, sol_symbols):
    rel_eqs = get_connect_equations(rel_symbol, from_symbol)
    for eq in rel_eqs:
        solve_equation(eq, rel_symbol, sol_symbols)

def solve_equation(eq, rel_symbol, sol_symbols):
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