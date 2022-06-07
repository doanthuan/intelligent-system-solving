from typing import Tuple, Type, NewType

from sympy import symbols, Eq, Rational
from equation import Equation
from rule import Rule
from utils import sort_name
from vertex import Vertex

# Attributes: A,B,C,a,b,c,S,p,R

# F: tập các phương trình, quan hệ tính toán, sự kiện vốn có của tam giác. Vd: A+B+C=180, A > 0, B > 0, a + b > C...

# Rules: A=b <=> a=b; a**2 + b**2 + c**2 => A=90; ...

class Triangle:

    # rules

    def __init__(self, name = "ABC"):

        name = sort_name(name)
        self.name = name

        self.equations = []
        self.symbols = []

        # 3 angles
        angles = {}
        angles[name[0]] = symbols(self.get_angle_name(name[0]), positive=True)
        angles[name[1]] = symbols(self.get_angle_name(name[1]), positive=True)
        angles[name[2]] = symbols(self.get_angle_name(name[2]), positive=True)
        self.angles = angles
        self.symbols.extend([angles[name[0]], angles[name[1]], angles[name[2]]])
    
    def get_angle_name(self, vertex):
        vertex1, vertex2 = self.get_other_vertices(vertex)
        vertexs = sort_name(vertex1 + vertex2)
        return vertexs[0] + vertex + vertexs[1]

    def get_other_vertices(self, vertex_name):
        if len(vertex_name) == 1:
            i_vertex = self.name.index(vertex_name)
            i_left = i_vertex - 1
            i_right = i_vertex + 1
            if i_right > 2:
                i_right = 0
            return self.name[i_left], self.name[i_right]
        
        if len(vertex_name) == 2:
            for c_name in self.name:
                if c_name not in vertex_name:
                    return c_name

    def set_angle(self, vertex_name, angle):
        if type(angle) == int or type(angle) == float:
            self.angles[vertex_name] = angle
        else:
            eq = Equation(self.angles[vertex_name], angle)
            self.equations.append(eq)

    '''
    RULES
    '''
    def run_rules(self):
        self.rule_01()
        

    #RULE1: A + B + C = 180 độ
    def rule_01(self):
        vertex1 = self.angles[self.name[0]]
        vertex2 = self.angles[self.name[1]]
        vertex3 = self.angles[self.name[2]]
        eq = Equation(vertex1 + vertex2 + vertex3, 180)
        self.equations.append(eq)


    # Phát sinh sự kiện: tia phân giác từ 1 góc trong tam giác, cắt cạnh đối diện tại 1 điểm thì chia đôi góc và tạo thành 2 tam giác khác
    def set_bisector(self, from_vertex, to_vertex):

        # generate 2 new triangle
        vertex1, vertex2 = self.get_other_vertices(from_vertex)

        triangle1 = Triangle(sort_name(vertex1+from_vertex+to_vertex))
        triangle2 = Triangle(sort_name(vertex2+from_vertex+to_vertex))

        # and angle_name in new 2 triangle = angle_name/2
        triangle1.set_angle(vertex1, self.angles[vertex1])
        triangle2.set_angle(vertex2, self.angles[vertex2])

        triangle1.set_angle(from_vertex, self.angles[from_vertex]/2)
        triangle2.set_angle(from_vertex, self.angles[from_vertex]/2)

        eq = Equation(triangle1.angles[to_vertex] + triangle2.angles[to_vertex], 180)
        self.equations.append(eq)

        return triangle1, triangle2

    
    # Phát sinh sự kiện: tia từ 1 góc cắt cạnh đối diện tại 1 điểm
    def set_ray(self, from_vertex, to_vertex, middle_vertex = None):
        results = []
        '''
        vertex1: A
        vertex2: C
        from_vertex: B
        to_vertex: K
        middle_vertex: M
        '''
        vertex1, vertex2 = self.get_other_vertices(from_vertex) 

        # generate 2 new triangle
        triangle1 = Triangle(sort_name(vertex1 + from_vertex + to_vertex))
        triangle2 = Triangle(sort_name(vertex2 + from_vertex + to_vertex))

        triangle1.set_angle(vertex1, self.angles[vertex1])
        triangle2.set_angle(vertex2, self.angles[vertex2])

        eq = Equation(triangle1.angles[to_vertex] + triangle2.angles[to_vertex], 180)
        self.equations.append(eq)

        eq = Equation(triangle1.angles[from_vertex] + triangle2.angles[from_vertex], self.angles[from_vertex])
        self.equations.append(eq)

        results.extend([triangle1, triangle2])

        if middle_vertex is not None:

            vertex_1 = triangle1.get_other_vertices(from_vertex + to_vertex)
            triangle1_1, triangle1_2 = triangle1.set_ray(vertex_1, middle_vertex)

            vertex_2 = triangle2.get_other_vertices(from_vertex + to_vertex)
            triangle2_1, triangle2_2 = triangle2.set_ray(vertex_2, middle_vertex)

            # one more triangle created 
            triangle3 = Triangle(sort_name(middle_vertex + vertex1 + vertex2))
            triangle3.set_angle(vertex1, triangle1_1.angles[vertex1])
            triangle3.set_angle(vertex2, triangle2_2.angles[vertex2])

            eq = Equation(triangle3.angles[middle_vertex], triangle1_1.angles[middle_vertex] + triangle2_2.angles[middle_vertex])
            self.equations.append(eq)

            eq = Equation(triangle3.angles[middle_vertex], triangle1_1.angles[middle_vertex] + triangle2_2.angles[middle_vertex])

            results.extend([triangle1_1, triangle1_2, triangle2_1, triangle2_2, triangle3])

        return results


    


# v1, v2, v3 = symbols('v1,v2,v3', positive=True)
# rule_01 = Rule(
#     [
#         Triangle(v1, v2, v3)
#     ],
#     [
#         Equation(v1 + v2 + v3, 180)
#     ], id="luat 1"
# )


# # RULE01: TRIANGLE(A,B,C) => A + B + C = 180
# def rule_01(A, B, C):
#     return Equation(A + B + C, 180)