from multiprocessing import connection
from equation import Equation
from event import Event
from goal import Goal
from rule import Rule
from triangle import Triangle
from sympy import false, simplify, solve, solveset, symbols, pprint

from utils import angle, remove_duplicates, sort_name, trace_symbol

from queue import Queue


# C : khái niệm ( điểm, tia, đoạn thẳng, góc, tam giác...)

# H : quan hệ phân cấp ( góc nhọn, góc tù, tam giác cân, ...)

# R : quan hệ giữa các khái niệm ( song song, vuông góc, thẳng hàng...)

# Funcs: các hàm ( hàm tính khoảng cách, trung điểm, tính đối xứng...)

# Rules: các luật ( tính chất, mệnh đề, định lý)

class Cokb:

    def __init__(self):
        # Tập GT
        self.triangles = {}
        self.all_eq = []
        self.all_symbol = []
        
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

    def get_angle_symbol(self, angel):
        triangle = self.triangles[sort_name(angel)]
        if triangle is None:
            raise Exception("Goal DETERMINE ANGLE error. Could not find triangle which have that angle")

        return triangle.angles[angel[1]]
    
    def set_triangle(self, name):
        if len(name) != 3:
            raise Exception("Event TRIANGLE error. Triangle's name must be 3 characters")

        self.add_triangle(name)

    def set_angle(self, symbol_name, symbol_value):
        if type(symbol_value) == int or type(symbol_value) == float:
            self.all_symbol[symbol_name] = symbol_value
        else:
            eq = Equation(self.all_symbol[symbol_name], symbol_value)
            self.all_eq.append(eq)

    def set_bisector_in(self, triangle, from_v, to_v):
        triangle = self.triangles[sort_name(triangle)]
        if triangle is None:
            raise Exception("Event BISECTOR error. Could not find triangle")

        triangle1, triangle2 = triangle.set_bisector(from_v, to_v)
        self.add_triangle([triangle1, triangle2])

    def set_ray(self, triangle, from_v, to_v, m_v):
        triangle = self.triangles[sort_name(triangle)]
        if triangle is None:
            raise Exception("Event BISECTOR error. Could not find triangle")

        # vẽ tia từ góc cắt cạnh đối diện tại 1 điểm, nếu đi qua 1 điểm thì vẽ thêm 2 tia phân giác với 2 góc còn lại
        triangles = triangle.set_ray(from_v, to_v, m_v)
        self.add_triangle(triangles)

    
    # @staticmethod
    # def apply_event(obj_type, obj_data):
    #     if obj_type == "TRIANGLE":
    #         if len(obj_data) != 3:
    #             raise Exception("Event TRIANGLE error. Triangle's name must be 3 characters")

    #         return Triangle(obj_data)

    #     if obj_type == "ANGLE":
    #         if len(obj_data) != 2:
    #             raise Exception("Event ANGLE error. Object data must have 2 arguments")

    #         triangle = self.triangles[sort_name(obj_data[0])]
    #         if triangle is None:
    #             raise Exception("Event ANGLE error. Could not find triangle")
            
    #         triangle.set_angle(obj_data[0][1], obj_data[1])
    #         angle(obj_data[0], obj_data[1])

    #         return Equation(self.angles[vertex_name], obj_data[1])

    #     if obj_type == "BISECTOR_IN":# tia phân giác trong từ 1 đỉnh, nếu cắt cạnh đối diện sẽ phát sinh 2 đối tượng tam giác mới
    #         if len(obj_data) != 3:
    #             raise Exception("Event BISECTOR error. Object data must have 3 arguments")

    #         triangle = self.triangles[sort_name(obj_data[0])]
    #         if triangle is None:
    #             raise Exception("Event BISECTOR error. Could not find triangle")

    #         from_vertex = obj_data[1]
    #         to_vertex = obj_data[2]

    #         triangle1, triangle2 = triangle.set_bisector(from_vertex, to_vertex)
    #         self.add_triangle([triangle1, triangle2])

    #     if obj_type == "RAY":
    #         if len(obj_data) < 3:
    #             raise Exception("Event BISECTOR error. Object data must have 2 or 3 arguments")

    #         triangle = self.triangles[sort_name(obj_data[0])]
    #         if triangle is None:
    #             raise Exception("Event BISECTOR error. Could not find triangle")

    #         # vẽ tia từ góc cắt cạnh đối diện tại 1 điểm, nếu đi qua 1 điểm thì vẽ thêm 2 tia phân giác với 2 góc còn lại
    #         triangles = triangle.set_ray(*obj_data[1:])
    #         self.add_triangle(triangles)
    
            
    def add_event(self, obj_type, obj_data):
        event = Event(obj_type, obj_data)
        self.gt_events.append(event)

    def add_goal(self, goal_type, goal_data):
        goal = Goal(goal_type, goal_data)
        self.goals.append(goal)

    def suy_dien_tien(self):
        
        # áp vào danh sách các sự kiện giả thiết
        for event in self.gt_events:
            # func_name = "apply_event_"+ str(event.event_type)
            # func = getattr(self, func_name)
            # func(*event.event_data)
            self.apply_event(event.obj_type, event.obj_data)

        step = 1
        found = False
        while step < 3:
            print(f"step {step}")

            # áp dụng các luật đối với các sự kiện đã có để tìm các sự kiện mới
            for triangle in self.triangles.values():
                triangle.run_rules()

            if self.check_finish_goals() == True: # Đã tìm thấy lời giải
                found = True
                print("STOP")
                # In lời giải
                break
            
            step += 1


    # Kiểm tra kết luận đã có trong tập sự kiện đã biết hay chưa
    def check_finish_goals(self):
        for goal in self.goals:
            if goal.status is not True: # Chỉ xét những mục tiêu chưa tìm được
                goal_data = goal.goal_data
                if goal.goal_type == 1: # xác định 1 đối tượng
                    if goal_data[0] == "ANGLE":
                        if len(goal_data) != 2:
                            raise Exception("Goal DETERMINE ANGLE error. Goal data must have 2 arguments")

                        target_symbol = self.get_angle_symbol(goal_data[1])

                        # load all equations,symbols and solve
                        self.load_equations_and_symbols()
                        results = solve(self.all_eq, self.all_symbol)
                        self.merge_results(results)

                        if self.check_symbol_in_result(target_symbol):
                            # FOUND
                            print(str(target_symbol) + ":" + str(self.results[target_symbol]))
                            goal.status = True
                        else:
                            return False
                            
                if goal.goal_type == 2: # so sánh
                    if goal_data[0] == "ANGLE": # so sánh góc
                        if len(goal_data) != 3:
                            raise Exception("Goal COMPARE ANGLE error. Goal data must have 3 arguments")

                        symbol_1 = self.get_angle_symbol(goal_data[1])
                        symbol_2 = self.get_angle_symbol(goal_data[2])
                        
                        # load all equations,symbols and solve
                        self.load_equations_and_symbols()

                        solutions = self.find_solutions(symbol_1, symbol_2)

                        if self.solve_compare(solutions, symbol_1, symbol_2):
                            goal.status = True
                            return True
                        return False

        return True # Tất cả mục tiêu đã tìm thấy


    def find_solutions(self, symbol_1, symbol_2):
        trace_symbols = self.bfs(symbol_1, symbol_2)
        if len(trace_symbols) == 0:
            print("CAN NOT FOUND SOLUTIONS")
            return False
        solutions =self.get_trace_path(trace_symbols, symbol_2)
        return solutions

    def solve_compare(self, solutions, symbol_1, symbol_2):
        # solve for each path
        for path_eqs in solutions:
            print("path_eq:", path_eqs)
            path_symbols = self.get_path_symbols(path_eqs)
            print("path_symbols:", path_symbols)
            results = solve(path_eqs, [symbol_1, symbol_2, *path_symbols])
            print(results)

            symbol_1_res = results[symbol_1]
            symbol_2_res = results[symbol_2]
            x = simplify(symbol_1_res - symbol_2_res)
            print(f"x:{x}")

            if x == 0:
                print(f"{symbol_1} = {symbol_2_res}")
                return True
            elif x.is_positive:
                print(f"{symbol_1} > {symbol_2}")
                return True
            elif x.is_negative:
                print(f"{symbol_1} < {symbol_2}")
                return True

        return False

    # thuật giải lan truyền
    def bfs(self, start_symbol, target_symbol):
        # khởi tạo tập known và tập checking
        knowns = [start_symbol]

        checking = Queue()
        checking.put(start_symbol)

        trace_symbols = {}
        trace_symbols[str(start_symbol)] = "ROOT"

        # duyet
        found = False
        while checking.qsize() > 0:
            checking_symbol = checking.get()
            rel_symbols = self.get_rel_symbols(checking_symbol, knowns)
            if len(rel_symbols) == 0:
                continue

            # goal reached
            if target_symbol in rel_symbols:
                print("FOUND TARGET")
                trace_symbol(trace_symbols, target_symbol, checking_symbol)
                found = True
                continue
                
                # return True, path_eqs, path_symbols
            else:
                knowns.extend(rel_symbols)

            # store related symbols for next checking
            for a_symbol in rel_symbols:
                checking.put(a_symbol)
                trace_symbol(trace_symbols, a_symbol, checking_symbol)

        if not found:
            print("Could not find target")
            return {}

        return trace_symbols
    
    def get_trace_path(self, trace_symbols, cur_symbol):
        current_paths = []
        
        if trace_symbols[str(cur_symbol)] == "ROOT": # current symbol is start_symbol
            return []
        else:

            parent_symbol = trace_symbols[str(cur_symbol)]
            if not isinstance(parent_symbol, list):
                parent_symbol = [parent_symbol]

            for a_symbol in parent_symbol:
                eqs = self.get_connect_equations(a_symbol, cur_symbol)
                for a_eq in eqs:
                    child_paths = self.get_trace_path(trace_symbols, a_symbol)
                    if len(child_paths) > 0:
                        for a_path in child_paths:
                            a_path.append(a_eq)
                            current_paths.append(a_path)
                    else:
                        new_path = []
                        new_path.append(a_eq)
                        current_paths.append(new_path)

            return current_paths
                


    def get_path_symbols(self, path_eqs):
        # get path symbols
        path_symbols = []
        for eq in path_eqs:
            symlist = [a_symbol for a_symbol in eq.free_symbols]
            path_symbols.extend(symlist)
        return remove_duplicates(path_symbols)

    def get_connect_equations(self, from_symbol, to_symbol):
        paths = []
        rel_eqs = self.get_rel_equations(from_symbol)
        for eq in rel_eqs:
            if to_symbol in eq.free_symbols:
                paths.append(eq)
        return paths

    def get_rel_equations(self, symbol):
        eqs = []
        for a_eq in self.all_eq:
            if a_eq in eqs:
                continue
            if symbol in a_eq.free_symbols:
                eqs.append(a_eq)
        return eqs

    def get_rel_symbols(self, symbol, knowns = []):
        rel_symbols = []
        rel_eqs = self.get_rel_equations(symbol)
        for eq in rel_eqs:
            symlist = [a_symbol for a_symbol in eq.free_symbols if (a_symbol != symbol and a_symbol not in knowns)]
            rel_symbols.extend(symlist)
        # remove duplicates
        return remove_duplicates(rel_symbols)

    def load_equations_and_symbols(self):
        for triangle in self.triangles.values():
            for eq in triangle.equations:
                # check equation exists
                if not self.check_equation_exist(eq):
                    self.all_eq.append(eq.get_eq())

            for a_symbol in triangle.symbols:
                # check symbol exists
                if not self.check_symbol_exist(a_symbol):
                    self.all_symbol.append(a_symbol)

    def check_equation_exist(self, eq):
        for a_eq in self.all_eq:
            if a_eq.lhs == eq.lhs and a_eq.rhs == eq.rhs:
                return True

        return False

    def check_symbol_exist(self, symbol):
        for a_symbol in self.all_symbol:
            if a_symbol == symbol:
                return True

        return False

    def merge_results(self, results):
        if len(results) > 0:
            new_results = {**results, **self.results}
            self.results = new_results

    def check_symbol_in_result(self, symbol):
        if symbol in self.results.keys():
            return True
        return False

            
