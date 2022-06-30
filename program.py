
from angle import Angle
from cobj import Cobj
from cokb import Cokb
from crule import Crule
from equation import Equation
from goal import Goal
from crel import Crel

from sympy import simplify

from triangle import Triangle


# C : khái niệm ( điểm, tia, đoạn thẳng, góc, tam giác...)

# H : quan hệ phân cấp ( góc nhọn, góc tù, tam giác cân, ...)

# R : quan hệ giữa các khái niệm ( song song, vuông góc, thẳng hàng...)

# Funcs: các hàm ( hàm tính khoảng cách, trung điểm, tính đối xứng...)

# Rules: các luật ( tính chất, mệnh đề, định lý)

class Program:

    def __init__(self):
        
        # Tập KL
        self.goals = []

    # def get_angle(self, angel_name):
    #     triangle = Cobj.get_triangle(angel_name)
    #     if triangle is None:
    #         raise Exception("Could not find triangle which have that angle")

    #     return triangle.angles[angel_name[1]]

    # def add_triangle(self, triangle):
    #     if isinstance(triangle, str):
    #         tri = Triangle(triangle)
    #         self.triangles[tri.name] = tri

    #     if isinstance(triangle, Triangle):
    #         self.triangles[triangle.name] = triangle
            
    #     if isinstance(triangle, list):
    #         for a_tri in triangle:
    #             self.triangles[a_tri.name] = a_tri
    
    # Event functions
    def set_triangle(self, name):
        if len(name) != 3:
            raise Exception("Set TRIANGLE error. Triangle's name must be 3 characters")
        
        Triangle(name)

    def set_angle(self, symbol_name, symbol_value):
        Angle(symbol_name, symbol_value)

    def set_bisector_in(self, tri_name, from_v, to_v):
        triangle = Cobj.get_triangle(tri_name)
        if triangle is None:
            raise Exception("Set BISECTOR error. Could not find triangle")

        triangle.set_bisector_in(from_v, to_v)

    def set_bisector_out(self, triangle, from_v, ray_name):
        triangle = self.triangles[Triangle.tri_name(triangle)]
        if triangle is None:
            raise Exception("Set BISECTOR error. Could not find triangle")

        triangle.set_bisector_out(from_v, ray_name)

    def set_height(self, triangle, from_v, to_v):
        triangle = self.triangles[Triangle.tri_name(triangle)]
        if triangle is None:
            raise Exception("Set HEIGHT error. Could not find triangle")

        triangle1, triangle2 = triangle.set_height(from_v, to_v)
        self.add_triangle([triangle1, triangle2])

    def set_ray(self, triangle, from_v, to_v, m_v):
        triangle = self.triangles[Triangle.tri_name(triangle)]
        if triangle is None:
            raise Exception("Set BISECTOR error. Could not find triangle")

        # vẽ tia từ góc cắt cạnh đối diện tại 1 điểm, nếu đi qua 1 điểm thì vẽ thêm 2 tia phân giác với 2 góc còn lại
        triangles = triangle.set_ray(from_v, to_v, m_v)
        self.add_triangle(triangles)

    def set_equation(self, equation: Equation):
        Cobj.set_eq(equation.eq)

    def add_goal(self, goal_type, goal_data):
        goal = Goal(goal_type, goal_data)
        self.goals.append(goal)

    # Kiểm tra kết luận đã có trong tập sự kiện đã biết hay chưa
    def solve_goals(self):

        Crule.apply_rules()

        for goal in self.goals:
            if goal.status is not True: # Chỉ xét những mục tiêu chưa tìm được
                goal_data = goal.goal_data
                if goal.goal_type == 1: # xác định 1 đối tượng
                    if goal_data[0] == "ANGLE":
                        if len(goal_data) != 2:
                            raise Exception("Goal DETERMINE ANGLE error. Goal data must have 2 arguments")

                        target_angle = Cobj.get_angle(goal_data[1])

                        Cokb.bfs(target_angle.symb)
                            
                if goal.goal_type == 2: # so sánh
                    if goal_data[0] == "ANGLE": # so sánh góc
                        if len(goal_data) != 3:
                            raise Exception("Goal COMPARE-ANGLE error. Goal data must have 3 arguments")

                        symbol_1 = self.get_angle(goal_data[1])
                        symbol_2 = self.get_angle(goal_data[2])

                        success, logs = self.solve_compare(symbol_1, symbol_2)
                        print_logs(logs)

                if goal.goal_type == 3: # chứng minh 1 mối quan hệ
                    if isinstance(goal_data, Crel):
                        self.solve_relation(goal_data)

                if goal.goal_type == 4: # tìm góc bằng góc
                    if goal_data[0] != "ANGLE" or len(goal_data) != 2:
                        raise Exception("Goal FIND-ANGLE-COMPARE error. Goal data must have 2 arguments")

                    target_symbol = self.get_angle(goal_data[1])
                    self.solve_find_compare(target_symbol)


    def solve_compare(self, symbol_1, symbol_2):

        load_graph()

        traced_symbols = trace_symbols(symbol_1, symbol_2)
        paths = get_trace_paths(traced_symbols, symbol_2)

        # solve for each path
        for path in paths:
            results, logs = solve_path(path)

            logs.append(("\nPath:", path))

            x = simplify(symbol_1 - results[str(symbol_2)])
            
            result_str = f"{symbol_1}-{symbol_2} = {x} ==> "
            if x == 0:
                result_str += f"{symbol_1} = {symbol_2}"
                logs.append(result_str)
                return 0, logs
            elif x.is_positive:
                result_str += f"{symbol_1} < {symbol_2}"
                logs.append(result_str)
                return 1, logs
            elif x.is_negative:
                result_str += f"{symbol_1} > {symbol_2}"
                logs.append(result_str)
                return -1, logs
        
        return False, ["Can not compare!"]


    def solve_relation(self, relation: Crel) -> bool:

        bfs()

        # duyet
        step = 1
        while step < 100:

            apply_rules()

            # check if all targets are found
            if relation_exist(relation):
                print("FOUND")
                # print trace rules
                print_trace_rels(relation)
                return True

            step += 1  

        return False


    def solve_find_compare(self, target_symbol):
        unknown_symbols = get_unknown()
        for a_symbol in unknown_symbols.values():
            if str(a_symbol) != str(target_symbol):
                result, logs = self.solve_compare(a_symbol, target_symbol)
                if type(result) == int and result == 0:
                    print("FOUND")
                    print_logs(logs)
                    break


