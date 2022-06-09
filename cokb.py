from multiprocessing import connection
from symtable import Symbol
from equation import Equation
from event import Event
from goal import Goal
from rule import Rule

from triangle import Triangle
from sympy import simplify, solve, solveset, symbols, pprint

from utils import remove_duplicates, sort_name

from queue import Queue

from solver import check_equation_exist, check_symbol_exist, get_all_symbols, get_candidate_equations, get_connect_equations, get_rel_symbols, init_knowns, print_solution, set_symbol, solve_equation, solve_rel_symbol
from solver import g_equations, g_symbols


# C : khái niệm ( điểm, tia, đoạn thẳng, góc, tam giác...)

# H : quan hệ phân cấp ( góc nhọn, góc tù, tam giác cân, ...)

# R : quan hệ giữa các khái niệm ( song song, vuông góc, thẳng hàng...)

# Funcs: các hàm ( hàm tính khoảng cách, trung điểm, tính đối xứng...)

# Rules: các luật ( tính chất, mệnh đề, định lý)

class Cokb:

    def __init__(self):
        # Tập GT
        self.triangles = {}
        
        # Tập KL
        self.results = {}
        self.goals = []

    def add_triangle(self, triangle):
        if isinstance(triangle, str):
            self.triangles[''.join(sorted(triangle))] = Triangle(triangle)

        if isinstance(triangle, Triangle):
            self.triangles[''.join(sorted(triangle.name))] = triangle
            
        if isinstance(triangle, list):
            for a_tri in triangle:
                self.triangles[''.join(sorted(a_tri.name))] = a_tri

    def get_triangle(self, name):
         return self.triangles[''.join(sorted(name))]

    def get_angle(self, angel):
        triangle = self.triangles[sort_name(angel)]
        if triangle is None:
            raise Exception("Goal DETERMINE ANGLE error. Could not find triangle which have that angle")

        return triangle.angles[angel[1]]
    
    def set_triangle(self, name):
        if len(name) != 3:
            raise Exception("Set TRIANGLE error. Triangle's name must be 3 characters")

        self.add_triangle(name)

    def set_angle(self, symbol_name, symbol_value):
        triangle = self.triangles[sort_name(symbol_name)]
        if triangle is None:
            raise Exception("Set angle error. Could not find triangle")

        triangle.set_angle(symbol_name[1], symbol_value)
        
        #self.all_symbol[sort_name(symbol_name)] = symbol_value
        #set_symbol(sort_name(symbol_name), symbol_value)

    def set_bisector_in(self, triangle, from_v, to_v):
        triangle = self.triangles[sort_name(triangle)]
        if triangle is None:
            raise Exception("Set BISECTOR error. Could not find triangle")

        triangle1, triangle2 = triangle.set_bisector(from_v, to_v)
        self.add_triangle([triangle1, triangle2])

    def set_ray(self, triangle, from_v, to_v, m_v):
        triangle = self.triangles[sort_name(triangle)]
        if triangle is None:
            raise Exception("Set BISECTOR error. Could not find triangle")

        # vẽ tia từ góc cắt cạnh đối diện tại 1 điểm, nếu đi qua 1 điểm thì vẽ thêm 2 tia phân giác với 2 góc còn lại
        triangles = triangle.set_ray(from_v, to_v, m_v)
        self.add_triangle(triangles)

    def add_goal(self, goal_type, goal_data):
        goal = Goal(goal_type, goal_data)
        self.goals.append(goal)

    # Kiểm tra kết luận đã có trong tập sự kiện đã biết hay chưa
    def solve_goals(self):
        # chạy các luật nội tại của các c-objects để tìm các equations mới
        for triangle in self.triangles.values():
            triangle.run_rules()

        for goal in self.goals:
            if goal.status is not True: # Chỉ xét những mục tiêu chưa tìm được
                goal_data = goal.goal_data
                if goal.goal_type == 1: # xác định 1 đối tượng
                    if goal_data[0] == "ANGLE":
                        if len(goal_data) != 2:
                            raise Exception("Goal DETERMINE ANGLE error. Goal data must have 2 arguments")

                        target_symbol = self.get_angle(goal_data[1])

                        self.bfs2(target_symbol)
                            
                if goal.goal_type == 2: # so sánh
                    if goal_data[0] == "ANGLE": # so sánh góc
                        if len(goal_data) != 3:
                            raise Exception("Goal COMPARE ANGLE error. Goal data must have 3 arguments")

                        symbol_1 = self.get_angle(goal_data[1])
                        symbol_2 = self.get_angle(goal_data[2])

                        # if self.solve_compare(symbol_1, symbol_2):
                        #     goal.status = True
                        #     return True
                        # return False
                        sol_symbols = self.bfs1(symbol_1, symbol_2)
                        results = sol_symbols[str(symbol_2)]
                        for result in results:
                            x = simplify(symbol_1 - result)
                            print(f"x:{x}")
                            print("---------------------")
                            
                        return False

        return True # Tất cả mục tiêu đã tìm thấy

    def solve_compare(self, symbol_1, symbol_2):

        trace_symbols = self.trace_symbols(symbol_1, symbol_2)
        solutions = self.get_trace_paths(trace_symbols, symbol_2)

        # solve for each path
        for path_eqs in solutions:
            print("path_eqs:", path_eqs)
            path_symbols = self.get_path_symbols(path_eqs)
            print("path_symbols:", [symbol_1, symbol_2, *path_symbols])
            results = solve(path_eqs, [symbol_1, symbol_2, *path_symbols])
            print(results)

            symbol_1_res = results[symbol_1]
            symbol_2_res = results[symbol_2]
            x = simplify(symbol_1_res - symbol_2_res)
            print(f"x:{x}")
            print("---------------------")

            # if x == 0:
            #     print(f"{symbol_1} = {symbol_2_res}")
            #     return True
            # elif x.is_positive:
            #     print(f"{symbol_1} > {symbol_2}")
            #     return True
            # elif x.is_negative:
            #     print(f"{symbol_1} < {symbol_2}")
            #     return True

        return False

    def trace_symbols(self, start_symbol, target_symbol):

        knowns = [start_symbol]

        checking = Queue()
        checking.put(start_symbol)

        trace_symbols = {}
        trace_symbols[str(start_symbol)] = "ROOT"

        # duyet
        found = False
        while checking.qsize() > 0:
            checking_symbol = checking.get()
            rel_symbols = get_rel_symbols(checking_symbol, knowns)
            if len(rel_symbols) == 0:
                continue

            # goal reached
            if target_symbol in rel_symbols:
                print("FOUND TARGET")
                self.trace_symbol(trace_symbols, target_symbol, checking_symbol)
                found = True
                continue

            knowns.extend(rel_symbols)
            # store related symbols for next checking
            for a_symbol in rel_symbols:
                checking.put(a_symbol)
                self.trace_symbol(trace_symbols, a_symbol, checking_symbol)

        if not found:
            print("Could not find target")
            return {}

        return trace_symbols

    def bfs1(self, start_symbol, target_symbol):
        # khởi tạo tập known và tập checking

        global g_equations, g_symbols

        checking = Queue()
        checking.put(start_symbol)

        knowns = [(start_symbol, 'ROOT')]
        sol_symbols = {}

        # duyet
        found = False
        while checking.qsize() > 0:
            checking_symbol = checking.get()

            rel_symbols = get_rel_symbols(checking_symbol, knowns)
            if len(rel_symbols) == 0:
                continue

            # goal reached
            if target_symbol in rel_symbols:
                print("FOUND TARGET")
                solve_rel_symbol(target_symbol, checking_symbol, sol_symbols)
                knowns.append((target_symbol, checking_symbol))
                print(sol_symbols[str(target_symbol)])
                found = True
                continue

            for rel_symbol in rel_symbols:
                checking.put(rel_symbol)
                solve_rel_symbol(rel_symbol, checking_symbol, sol_symbols)
                knowns.append((rel_symbol, checking_symbol))
                

        if not found:
            print("Could not find target")
            return {}

        return sol_symbols

    
    
    def get_trace_paths(self, trace_symbols, cur_symbol):
        if len(trace_symbols) == 0:
            return []
        current_paths = []
        
        if trace_symbols[str(cur_symbol)] == "ROOT": # current symbol is start_symbol
            return []
        else:

            parent_symbols = trace_symbols[str(cur_symbol)]

            for a_parent in parent_symbols:
                eqs = get_connect_equations(a_parent, cur_symbol)
                for a_eq in eqs:
                    child_paths = self.get_trace_paths(trace_symbols, a_parent)
                    if len(child_paths) > 0:
                        for a_path in child_paths:
                            a_path.append(a_eq.eq)
                            current_paths.append(a_path)
                    else:
                        current_paths.append([a_eq.eq])

            return current_paths

    def get_path_symbols(self, path_eqs):
        # get path symbols
        path_symbols = []
        for eq in path_eqs:
            symlist = [a_symbol for a_symbol in eq.free_symbols]
            path_symbols.extend(symlist)
        return remove_duplicates(path_symbols)
    
    def trace_symbol(self, trace_path, a_symbol, parent_symbol):
        if str(a_symbol) in trace_path:
            trace_path[str(a_symbol)].append(parent_symbol)
        else:
            trace_path[str(a_symbol)] = [parent_symbol]

    # def get_connect_equations(self, from_symbol, to_symbol):
    #     paths = []
    #     rel_eqs = self.get_rel_equations(from_symbol)
    #     for eq in rel_eqs:
    #         if to_symbol in eq.free_symbols:
    #             paths.append(eq)
    #     return paths

    # def get_rel_equations(self, symbol):
    #     eqs = []
    #     for a_eq in self.all_eq:
    #         if a_eq in eqs:
    #             continue
    #         if symbol in a_eq.free_symbols:
    #             eqs.append(a_eq)
    #     return eqs

    # def get_rel_symbols(self, symbol, knowns = []):
    #     rel_symbols = []
    #     rel_eqs = self.get_rel_equations(symbol)
    #     for eq in rel_eqs:
    #         symlist = [a_symbol for a_symbol in eq.free_symbols if (a_symbol != symbol and a_symbol not in knowns)]
    #         rel_symbols.extend(symlist)
    #     # remove duplicates
    #     return remove_duplicates(rel_symbols)

    # def load_equations_and_symbols(self):
    #     for triangle in self.triangles.values():
    #         for eq in triangle.equations:
    #             # check equation exists
    #             if not check_equation_exist(eq):
    #                 self.all_eq.append(eq.get_eq())

    #         for a_symbol in triangle.symbols:
    #             # check symbol exists
    #             if not check_symbol_exist(a_symbol):
    #                 #self.all_symbol[str(a_symbol)] = a_symbol
    #                 self.all_symbol.append(a_symbol)

    # def solve_symbol(self, sol_symbols, from_symbol, a_symbol):
    #     rel_eqs = get_connect_equations(from_symbol, a_symbol)
    #     for eq in rel_eqs:

    #         # solve an equation
    #         for a_sym in eq.free_symbols:
    #             if str(a_sym) in sol_symbols.keys():
    #                 eq = eq.subs(a_sym, sol_symbols[str(a_sym)]) 

    #         result = solve(eq,[a_symbol])[0]

    #         if str(a_symbol) in sol_symbols:
    #             sol_symbols[str(a_symbol)].append(result)
    #         else:
    #             sol_symbols[str(a_symbol)] = [result]

    def bfs2(self, target):

        # khởi tạo tập known từ giả thuyết
        knowns = init_knowns()

        # # get goals
        # targets = [ str(self.get_angle(goal.goal_data[1])) for goal in self.goals if goal.goal_type == 1]
        
        sol_symbols = {}

        # duyet
        step = 1
        while step < 100:

            # check if all targets are found
            if str(target) in knowns.keys():
                print_solution(target)
                return True
            
            # tìm những equation tìm năng
            rel_eqs = get_candidate_equations()
            if len(rel_eqs) == 0:
                return False

            # tìm những biến mới và đưa vào tập knowns
            for a_eq in rel_eqs:
                sol_symbol, sol_value = solve_equation(a_eq)
                if sol_symbol is not None:
                    sol_symbols[str(sol_symbol)] = sol_value

            step += 1

        return sol_symbols









