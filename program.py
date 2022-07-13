

from ceq import Ceq
from crule import Crule
from line import Line
from log import Log
from cobj import Cobj
from cokb import Cokb
from goal import Goal
from relation import Relation

from sympy import Eq
from solver_compare import SolverCompare

from triangle import Triangle
from angle import Angle

# C : khái niệm ( điểm, tia, đoạn thẳng, góc, tam giác...)

# H : quan hệ phân cấp ( góc nhọn, góc tù, tam giác cân, ...)

# R : quan hệ giữa các khái niệm ( song song, vuông góc, thẳng hàng...)

# Funcs: các hàm ( hàm tính khoảng cách, trung điểm, tính đối xứng...)

# Rules: các luật ( tính chất, mệnh đề, định lý)

class Program:

    def __init__(self):
        
        # Tập KL
        self.goals = []
        self.answers = []

        Cobj.reset_state()
    
    # Event functions
    def set_triangle(self, name):
        return Triangle(name)

    def set_triangle_equal(self, tri1_name, tri2_name):
        tri1 = Triangle(tri1_name)
        tri2 = Triangle(tri2_name)
        tri1.set_equal(tri2)

    # def set_angle(self, name, value):
    #     Angle(name, value)

    def set_angle(self, tri_name, angle, value):
        triangle = Cobj.get_triangle(tri_name)
        if triangle is None:
            raise Exception("Set Angle error. Could not find triangle")

        triangle.set_angle(angle, value)
    
    def unset_angle(self, name):
        Cobj.unset_angle(name)

    def set_edge(self, name, value):
        Line(name, value)

    def reset_state(self):
        Cobj.reset_state()

    def set_bisector_in(self, tri_name, from_v, to_v = None):
        triangle = Cobj.get_triangle(tri_name)
        if triangle is None:
            raise Exception("Set BISECTOR IN error. Could not find triangle")

        triangle.set_bisector_in(from_v, to_v)

    def set_bisector_center(self, tri_name, center):
        triangle = Cobj.get_triangle(tri_name)
        if triangle is None:
            raise Exception("Set BISECTOR IN error. Could not find triangle")

        triangle.set_bisector_center(center)

    def set_bisector_out(self, tri_name, from_v, ray_name):
        triangle = Cobj.get_triangle(tri_name)
        if triangle is None:
            raise Exception("Set BISECTOR OUT error. Could not find triangle")

        triangle.set_bisector_out(from_v, ray_name)

    def set_height(self, tri_name, from_v, to_v):
        triangle = Cobj.get_triangle(tri_name)
        if triangle is None:
            raise Exception("Set HEIGHT error. Could not find triangle")

        triangle.set_height(from_v, to_v)

    def set_ray(self, tri_name, from_v, m_v, to_v = None):
        triangle = Cobj.get_triangle(tri_name)
        if triangle is None:
            raise Exception("Set RAY error. Could not find triangle")

        # vẽ tia từ đỉnh qua điểm m, cắt đối diện tại to_v
        triangle.set_ray(from_v, m_v, to_v)

    def set_equation(self, equation: Eq):
        Ceq.set_eq(equation)

    def add_goal(self, goal_type, goal_data):
        goal = Goal(goal_type, goal_data)
        self.goals.append(goal)

    # Kiểm tra kết luận đã có trong tập sự kiện đã biết hay chưa
    def solve(self):

        Crule.run()

        for goal in self.goals:
            if goal.status is not True: # Chỉ xét những mục tiêu chưa tìm được
                goal_data = goal.goal_data
                if goal.goal_type == 1: # xác định 1 đối tượng
                    if goal_data[0] == "ANGLE":
                        if len(goal_data) != 2:
                            raise Exception("Goal DETERMINE ANGLE error. Goal data must have 2 arguments")

                        angle = Cobj.get_angle(goal_data[1])
                        logs = Cokb.solve(angle.symb)
                        self.answers.append(logs)
                        #Log.print_logs(logs)
                            
                if goal.goal_type == 2: # so sánh
                    if goal_data[0] == "ANGLE": # so sánh góc
                        if len(goal_data) != 3:
                            raise Exception("Goal COMPARE-ANGLE error. Goal data must have 3 arguments")

                        angle_1 = Cobj.get_angle(goal_data[1])
                        angle_2 = Cobj.get_angle(goal_data[2])

                        eqs = Cobj.subs_eqs_with_hypo()
                        solver = SolverCompare(Cobj.symbs, eqs)
                        success, result, logs = solver.solve_compare(angle_1.symb, angle_2.symb)
                        Log.print_logs(logs)
                        self.answers.append(logs)

                if goal.goal_type == 3: # chứng minh 1 mối quan hệ
                    logs = Cokb.solve(goal_data)
                    self.answers.append(logs)

                if goal.goal_type == 4: # tìm góc bằng góc
                    if goal_data[0] != "ANGLE" or len(goal_data) != 2:
                        raise Exception("Goal FIND-ANGLE-COMPARE error. Goal data must have 2 arguments")

                    angle = Cobj.get_angle(goal_data[1])
                    logs = Cokb.solve_find_compare(angle.symb)
                    self.answers.append(logs)

                # if goal.goal_type == 5: # chứng minh
                #     if goal_data[0] != "ANGLE" or len(goal_data) != 3:
                #         raise Exception("Goal PROVE ANGLE ATTRIBUTE error. Goal data must have 3 arguments")

                #     angle = Cobj.get_angle(goal_data[1])
                #     # if angle is None:
                #     #     Angle(goal_data[1])
                #     Cokb.prove(angle, goal_data[2])
                    



