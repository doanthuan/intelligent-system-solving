from sympy import Symbol, solve, simplify
from ceq import Ceq
from utils import flat_list, remove_duplicates

class SolverProve:
    
    def __init__(self, symbs, eqs):
        self.symbs = symbs
        self.eqs = eqs
        self.graph = self.load_graph()

    def load_graph(self):
        graph = {}
        for symbol_row in self.symbs.keys():
            graph[symbol_row] = {}
            for symbol_col in self.symbs.keys():
                if symbol_col == symbol_row:
                    continue
                #g_graph[symbol_row][symbol_col] = []
                for a_eq in self.eqs:
                    free_symbols_str = [str(a_sym) for a_sym in a_eq.free_symbols]
                    if symbol_row in free_symbols_str and symbol_col in free_symbols_str:
                        if symbol_col not in graph[symbol_row]:
                            graph[symbol_row][symbol_col] = []
                        graph[symbol_row][symbol_col].append(a_eq)

        return graph

    def get_rel_equations(self, symbol):
        return flat_list(self.graph[str(symbol)].values())

    def get_rel_symbols(self, from_symbol, knowns = []):
        results = []
        for a_symbol in self.graph[str(from_symbol)].keys():
            if isinstance(self.symbs[str(a_symbol)], Symbol) and not self.check_in_knowns(a_symbol, self.graph[str(from_symbol)][a_symbol][0], knowns):
                results.append(self.symbs[str(a_symbol)])
        return results

    def get_connect_equations(self, to_symbol, from_symbol):
        if str(to_symbol) in self.graph[str(from_symbol)].keys():
            return self.graph[str(from_symbol)][str(to_symbol)]
        return []

    def check_in_knowns(self, rel_symbol, eq, knowns):
        for kn in knowns:
            if type(kn) == list:
                if rel_symbol == kn[0] and (eq == kn[1] or 'ROOT' == kn[1]):
                    return True
        
        if type(rel_symbol) == str:
            knowns_str = [str(kn) for kn in knowns]
            return rel_symbol in knowns_str
        else:
            return rel_symbol in knowns

    def trace_symbols(self, start_symbol, target_symbol):

        queue = [start_symbol]

        trace_symbols = {}
        trace_symbols[str(start_symbol)] = "ROOT"

        # duyet
        found = False
        index = 0
        while index < len(queue):
            checking_symbol = queue[index]
            index += 1

            rel_symbols = self.get_rel_symbols(checking_symbol, queue[:index])
            if len(rel_symbols) == 0:
                continue

            # goal reached
            if target_symbol in rel_symbols:
                print("trace_symbols: FOUND TARGET")
                self.trace_symbol(target_symbol, checking_symbol, trace_symbols)
                found = True
                continue

            # store related symbols for next checking
            for a_symbol in rel_symbols:
                if a_symbol not in queue:
                    queue.append(a_symbol)

                self.trace_symbol(a_symbol, checking_symbol, trace_symbols)

        if not found:
            print("Could not find target")
            return {}

        return trace_symbols

    def trace_symbol(self, a_symbol, parent_symbol, trace_symbols):
        if str(a_symbol) in trace_symbols:
            trace_symbols[str(a_symbol)].append(parent_symbol)
        else:
            trace_symbols[str(a_symbol)] = [parent_symbol]

    def get_trace_paths(self, trace_symbols, cur_symbol):
        if len(trace_symbols) == 0 or trace_symbols[str(cur_symbol)] == "ROOT":
            return []

        current_paths = []
        parent_symbols = trace_symbols[str(cur_symbol)]
        for a_parent in parent_symbols:
            eqs = self.get_connect_equations(a_parent, cur_symbol)
            for a_eq in eqs:
                child_paths = self.get_trace_paths(trace_symbols, a_parent)
                if len(child_paths) > 0:
                    for c_path in child_paths:
                        c_path.append((a_eq, cur_symbol))
                        current_paths.append(c_path)
                else:
                    current_paths.append([(a_eq, cur_symbol)])

        return current_paths

    def get_path_symbols(self, path):
        # get path symbols
        path_symbols = []
        for step in path:
            eq = step[0]
            symlist = [a_symbol for a_symbol in eq.free_symbols]
            path_symbols.extend(symlist)
        return remove_duplicates(path_symbols)

    def get_path_eqs(self, path):
        return [step[0] for step in path]

    def solve_path(self, path):
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
            if len(result) > 0:
                sol_symbols[str(sol_symbol)] = result[0]
                logs.append(f"=> {sol_symbol} = {result[0]}")

        return sol_symbols, logs

    def solve_compare(self, symbol_1, symbol_2):

        #load_graph()

        traced_symbols = self.trace_symbols(symbol_1, symbol_2)
        paths = self.get_trace_paths(traced_symbols, symbol_2)

        # solve for each path
        for path in paths:
            results, logs = self.solve_path(path)

            logs.append(("\nPath:", path))

            x = simplify(symbol_1 - results[str(symbol_2)])
            
            result_str = f"{symbol_1}-{symbol_2} = {x} ==> "
            if x == 0:
                result_str += f"{symbol_1} = {symbol_2}"
                logs.append(result_str)
                return True, 0, logs
            elif x.is_positive:
                result_str += f"{symbol_1} > {symbol_2}"
                logs.append(result_str)
                return True, 1, logs
            elif x.is_negative:
                result_str += f"{symbol_1} < {symbol_2}"
                logs.append(result_str)
                return True, -1, logs
        
        return False, None, ["Can not compare!"]