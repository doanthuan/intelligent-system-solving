
from angle import Angle
from ceq import Ceq
from clog import Clog
from cobj import Cobj
from cokb import Cokb
from crule import Crule
from equation import Equation
from goal import Goal
from relation import Relation

from sympy import Eq, simplify
from line import Line
from solver_compare import SolverCompare

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
    
    # Event functions
    def set_triangle(self, name):
        Triangle(name)

    def set_angle(self, symbol_name, symbol_value):
        Angle(symbol_name, symbol_value)

    def set_bisector_in(self, tri_name, from_v, to_v):
        triangle = Cobj.get_triangle(tri_name)
        if triangle is None:
            raise Exception("Set BISECTOR IN error. Could not find triangle")

        triangle.set_bisector_in(from_v, to_v)

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

    def set_ray(self, tri_name, from_v, to_v, m_v):
        triangle = Cobj.get_triangle(tri_name)
        if triangle is None:
            raise Exception("Set BISECTOR error. Could not find triangle")

        # vẽ tia từ góc cắt cạnh đối diện tại 1 điểm, nếu đi qua 1 điểm thì vẽ thêm 2 tia phân giác với 2 góc còn lại
        triangle.set_ray(from_v, to_v, m_v)

    def set_equation(self, equation: Eq):
        Ceq.set_eq(equation)

    def add_goal(self, goal_type, goal_data):
        goal = Goal(goal_type, goal_data)
        self.goals.append(goal)

    # Kiểm tra kết luận đã có trong tập sự kiện đã biết hay chưa
    def solve_goals(self):

        Cobj.init_hypo()
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

                        angle_1 = Cobj.get_angle(goal_data[1])
                        angle_2 = Cobj.get_angle(goal_data[2])

                        solver = SolverCompare(Cobj.symbs, Cobj.eqs)

                        success, logs = solver.solve_compare(angle_1.symb, angle_2.symb)
                        Clog.print_logs(logs)

                if goal.goal_type == 3: # chứng minh 1 mối quan hệ
                    if isinstance(goal_data, Relation):
                        Cokb.solve_relation(goal_data)

                if goal.goal_type == 4: # tìm góc bằng góc
                    if goal_data[0] != "ANGLE" or len(goal_data) != 2:
                        raise Exception("Goal FIND-ANGLE-COMPARE error. Goal data must have 2 arguments")

                    target_symbol = Cobj.get_angle(goal_data[1])
                    Cokb.solve_find_compare(target_symbol.symb)




