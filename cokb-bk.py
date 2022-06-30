from angle import Angle
from equation import Equation
from event import Event
from goal import Goal
from crel import Crel
from ruleobj import Rule

from triangle import Triangle
from sympy import simplify, solve, solveset, symbols, pprint

from utils import remove_duplicates, sort_name

from queue import Queue

from cokb import apply_rules, get_simple_equations, get_rel_symbols, get_rel_symbols, get_trace_paths, get_known, print_solution, relation_exist, solve_equation, solve_path, solve_rel_symbol, trace_symbols
from cokb import g_equations, g_symbols, g_graph


# C : khái niệm ( điểm, tia, đoạn thẳng, góc, tam giác...)

# H : quan hệ phân cấp ( góc nhọn, góc tù, tam giác cân, ...)

# R : quan hệ giữa các khái niệm ( song song, vuông góc, thẳng hàng...)

# Funcs: các hàm ( hàm tính khoảng cách, trung điểm, tính đối xứng...)

# Rules: các luật ( tính chất, mệnh đề, định lý)

class Cokb:

    def __init__(self):
        # Tập C
        self.triangles = {}
        
        # Tập KL
        self.goals = []

    def get_angle(self, angel):
        triangle = self.triangles[sort_name(angel)]
        if triangle is None:
            raise Exception("Could not find triangle which have that angle")

        return triangle.angles[angel[1]]

    def add_triangle(self, triangle):
        if isinstance(triangle, str):
            self.triangles[''.join(sorted(triangle))] = Triangle(triangle)

        if isinstance(triangle, Triangle):
            self.triangles[''.join(sorted(triangle.name))] = triangle
            
        if isinstance(triangle, list):
            for a_tri in triangle:
                self.triangles[''.join(sorted(a_tri.name))] = a_tri
    
    # Event functions
    def set_triangle(self, name):
        if len(name) != 3:
            raise Exception("Set TRIANGLE error. Triangle's name must be 3 characters")

        self.add_triangle(name)

    def set_angle(self, symbol_name, symbol_value):
        triangle = self.triangles[sort_name(symbol_name)]
        if triangle is None:
            raise Exception("Set angle error. Could not find triangle")

        triangle.set_angle(symbol_name[1], symbol_value)
        
    def set_angle_out(self, symbol_name, vertex, ray_name = None):
        triangle = self.triangles[sort_name(symbol_name)]
        if triangle is None:
            raise Exception("Set angle error. Could not find triangle")

        triangle.set_angle_out(vertex, ray_name)

    def set_bisector_in(self, triangle, from_v, to_v):
        triangle = self.triangles[sort_name(triangle)]
        if triangle is None:
            raise Exception("Set BISECTOR error. Could not find triangle")

        triangle1, triangle2 = triangle.set_bisector_in(from_v, to_v)
        self.add_triangle([triangle1, triangle2])

    def set_bisector_out(self, triangle, from_v, ray_name):
        triangle = self.triangles[sort_name(triangle)]
        if triangle is None:
            raise Exception("Set BISECTOR error. Could not find triangle")

        triangle.set_bisector_out(from_v, ray_name)

    def set_height(self, triangle, from_v, to_v):
        triangle = self.triangles[sort_name(triangle)]
        if triangle is None:
            raise Exception("Set HEIGHT error. Could not find triangle")

        triangle1, triangle2 = triangle.set_height(from_v, to_v)
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

        for goal in self.goals:
            if goal.status is not True: # Chỉ xét những mục tiêu chưa tìm được
                goal_data = goal.goal_data
                if goal.goal_type == 1: # xác định 1 đối tượng
                    if goal_data[0] == "ANGLE":
                        if len(goal_data) != 2:
                            raise Exception("Goal DETERMINE ANGLE error. Goal data must have 2 arguments")

                        target_symbol = self.get_angle(goal_data[1])

                        self.bfs(target_symbol)
                            
                if goal.goal_type == 2: # so sánh
                    if goal_data[0] == "ANGLE": # so sánh góc
                        if len(goal_data) != 3:
                            raise Exception("Goal COMPARE ANGLE error. Goal data must have 3 arguments")

                        symbol_1 = self.get_angle(goal_data[1])
                        symbol_2 = self.get_angle(goal_data[2])

                        self.solve_compare(symbol_1, symbol_2)

                if goal.goal_type == 3: # chứng minh 1 mối quan hệ
                    if isinstance(goal_data, Crel):

                        self.solve_relation(goal_data)

    def bfs(self, target):

        # khởi tạo tập known từ giả thuyết
        knowns = get_known()

        # # get goals
        # targets = [ str(self.get_angle(goal.goal_data[1])) for goal in self.goals if goal.goal_type == 1]

        # duyet
        step = 1
        while step < 100:

            # check if all targets are found
            if str(target) in knowns.keys():
                print_solution(target)
                return True
            
            # tìm những equation tìm năng
            rel_eqs = get_simple_equations()
            if len(rel_eqs) == 0:
                return False

            for a_eq in rel_eqs:
                solve_equation(a_eq)

            step += 1  

    def bfs_compare(self, start_symbol, target_symbol):
        # khởi tạo tập known và tập checking

        queue = []
        queue.append(start_symbol)

        knowns = [(start_symbol, 'ROOT')]
        sol_symbols = {}

        # duyet
        found = False
        index = 0
        while index < len(queue):
            checking_symbol = queue[index]
            index += 1

            rel_symbols = get_rel_symbols(checking_symbol, knowns)
            if len(rel_symbols) == 0:
                continue

            # goal reached
            if target_symbol in rel_symbols:
                print(f"FOUND TARGET FROM {checking_symbol}")
                solve_rel_symbol(target_symbol, checking_symbol, sol_symbols, knowns)
                print(f"{str(target_symbol)}=", sol_symbols[str(target_symbol)])
                found = True
                continue

            for rel_symbol in rel_symbols:
                if rel_symbol not in queue:
                    queue.append(rel_symbol)
                solve_rel_symbol(rel_symbol, checking_symbol, sol_symbols, knowns)
                
        if not found:
            print("Could not find target")
            return False

        results = sol_symbols[str(target_symbol)]
        for result in results:
            x = simplify(start_symbol - result)
            print(f"x:{x}")
            print("---------------------")
            if x == 0:
                print(f"{start_symbol} = {target_symbol}")
                return True
            elif x.is_positive:
                print(f"{start_symbol} > {target_symbol}")
                return True
            elif x.is_negative:
                print(f"{start_symbol} < {target_symbol}")
                return True

        return False

    def solve_compare(self, symbol_1, symbol_2):

        traced_symbols = trace_symbols(symbol_1, symbol_2)
        paths = get_trace_paths(traced_symbols, symbol_2)

        # solve for each path
        for path in paths:
            print("\nPath:", path)

            results = solve_path(path)

            x = simplify(symbol_1 - results[str(symbol_2)])
            
            result_str = f"{symbol_1}-{symbol_2} = {x} ==> "
            if x == 0:
                result_str += f"{symbol_1} = {symbol_2}"
                print(result_str)
                return True
            elif x.is_positive:
                result_str += f"{symbol_1} < {symbol_2}"
                print(result_str)
                return True
            elif x.is_negative:
                result_str += f"{symbol_1} > {symbol_2}"
                print(result_str)
                return True

        return False


    def solve_relation(self, relation: Crel) -> bool:

        # duyet
        step = 1
        while step < 100:

            apply_rules()

            # check if all targets are found
            if relation_exist(relation):
                print("FOUND")
                return True

            step += 1  

        return False





