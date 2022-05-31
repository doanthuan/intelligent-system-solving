from unittest import result
from event import Event
from goal import Goal
from triangle import Triangle
from sympy import simplify, solve

from utils import sort_name

# C : khái niệm ( điểm, tia, đoạn thẳng, góc, tam giác...)

# H : quan hệ phân cấp ( góc nhọn, góc tù, tam giác cân, ...)

# R : quan hệ giữa các khái niệm ( song song, vuông góc, thẳng hàng...)

# Funcs: các hàm ( hàm tính khoảng cách, trung điểm, tính đối xứng...)

# Rules: các luật ( tính chất, mệnh đề, định lý)
        

class Cokb:

    def __init__(self):
        # Tập GT
        self.gt_events = []
        self.triangles = {}
        
        # Tập KL
        self.goals = []

        # Tập sympy
        self.equations = []
        self.symbols = []
        self.results = {}

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


    # Sự kiện về thông tin loại đối tượng
    # def apply_event_1(self, obj_type, obj_name):
    #     if obj_type == "TRIANGLE":
    #         self.add_triangle(obj_name)

    # Sự kiện về tính xác định của một đối tượng hay của một thuộc tính của đối tượng thông qua biểu thức hằng
    # def apply_event_3(self, obj_type, obj_name, attr_type, attr_data, value):
    #     if obj_type == "TRIANGLE":
    #         triangle = self.get_triangle(obj_name)
    #         if attr_type == "ANGLE":
    #             triangle.set_angle(attr_data, value)

    # Sự kiện về tính xác định của một đối tượng hay của một thuộc tính của đối tượng
    def apply_event(self, obj_type, obj_data):
        if obj_type == "TRIANGLE":
            if len(obj_data) != 3:
                raise Exception("Event TRIANGLE error. Triangle's name must be 3 characters")

            self.add_triangle(obj_data)

        if obj_type == "ANGLE":
            if len(obj_data) != 2:
                raise Exception("Event ANGLE error. Object data must have 2 arguments")

            triangle = self.triangles[sort_name(obj_data[0])]
            if triangle is None:
                raise Exception("Event ANGLE error. Could not find triangle")
            
            triangle.set_angle(obj_data[0][1], obj_data[1])

        if obj_type == "BISECTOR":# vẽ tia phân giác phát sinh 2 đối tượng tam giác mới
            if len(obj_data) != 3:
                raise Exception("Event BISECTOR error. Object data must have 3 arguments")

            triangle = self.triangles[sort_name(obj_data[0])]
            if triangle is None:
                raise Exception("Event BISECTOR error. Could not find triangle")

            from_vertex = obj_data[1]
            to_vertex = obj_data[2]

            triangle1, triangle2 = triangle.set_bisector(from_vertex, to_vertex)
            self.add_triangle([triangle1, triangle2])

        if obj_type == "RAY":
            if len(obj_data) < 3:
                raise Exception("Event BISECTOR error. Object data must have 2 or 3 arguments")

            triangle = self.triangles[sort_name(obj_data[0])]
            if triangle is None:
                raise Exception("Event BISECTOR error. Could not find triangle")

            # vẽ tia từ góc cắt cạnh đối diện tại 1 điểm, nếu đi qua 1 điểm thì vẽ thêm 2 tia phân giác với 2 góc còn lại
            triangles = triangle.set_ray(*obj_data[1:])
            self.add_triangle(triangles)
            
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
        while step < 200:

            if self.check_finish_goals() == True: # Đã tìm thấy lời giải
                found = True
                print("FOUND")
                # In lời giải
                break

            # áp dụng các luật đối với các sự kiện đã có để tìm các sự kiện mới
            for key, triangle in self.triangles.items():
                triangle.run_rules()
            
            step += 1


    # Kiểm tra kết luận đã có trong tập sự kiện đã biết hay chưa
    def check_finish_goals(self):
        for goal in self.goals:
            if goal.status is not True: # Chỉ xét những mục tiêu chưa tìm được
                goal_data = goal.goal_data
                if goal.goal_type == 1: # xác định 1 đối tượng
                    if goal_data[0] == "TRIANGLE" and goal_data[1] is not None: # đối tượng mục tiêu là tam giác
                        triangle_name = ''.join(sorted(goal_data[1]))
                        triangle = self.triangles[triangle_name]
                        if triangle is None: # Không tìm được mục tiêu
                            return False

                        if goal_data[2] == "ANGLE" and goal_data[3] is not None: # tìm góc trong tam giác
                            vertex = triangle.vertexs[goal_data[3]]

                            # load all equations and symbols
                            self.load_equations_and_symbols()
                            
                            results = solve(self.equations, self.symbols)
                            self.merge_results(results)

                            if self.check_symbol_in_result(vertex):
                                # FOUND
                                print(str(vertex) + ":" + str(self.results[vertex]))
                                goal.status = True
                            else:
                                return False
                            

        return True # Tất cả mục tiêu đã tìm thấy

    def load_equations_and_symbols(self):
        for triangle in self.triangles.values():
            for eq in triangle.equations:
                # check equation exists
                if not self.check_equation_exist(eq):
                    self.equations.append(eq.get_eq())

            for a_symbol in triangle.symbols:
                # check symbol exists
                if not self.check_symbol_exist(a_symbol):
                    self.symbols.append(a_symbol)

    def check_equation_exist(self, eq):
        for a_eq in self.equations:
            if a_eq.lhs == eq.lhs and a_eq.rhs == eq.rhs:
                return True

        return False

    def check_symbol_exist(self, symbol):
        for a_symbol in self.symbols:
            if a_symbol == symbol:
                return True

        return False

    def merge_results(self, results):
        new_results = {**results, **self.results}
        self.results = new_results

    def check_symbol_in_result(self, symbol):
        if symbol in self.results.keys():
            return True
        return False

            

