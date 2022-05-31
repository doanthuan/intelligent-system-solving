from typing import Tuple, Type, NewType

from sympy import symbols, Eq, Rational
from equation import Equation
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
        vertexs = {}
        vertexs[name[0]] = symbols(self.get_angle_name(name[0]))
        vertexs[name[1]] = symbols(self.get_angle_name(name[1]))
        vertexs[name[2]] = symbols(self.get_angle_name(name[2]))
        self.vertexs = vertexs
        self.symbols.extend([vertexs[name[0]], vertexs[name[1]], vertexs[name[2]]])
    
    def get_angle_name(self, vertex):
        vertex1, vertex2 = self.get_other_vertices(vertex)
        return vertex1+vertex+vertex2

    def get_other_vertices(self, vertex_name):
        vertexs = []
        for c_name in self.name:
            if c_name != vertex_name:
                vertexs.append(c_name)
                
        return tuple(vertexs)

    def set_angle(self, vertex_name, angle):
        eq = Equation(self.vertexs[vertex_name], angle)
        self.equations.append(eq)

    '''
    RULES
    '''
    def run_rules(self):
        self.rule_01()
        

    #RULE1: A + B + C = 180 độ
    def rule_01(self):
        vertex1 = self.vertexs[self.name[0]]
        vertex2 = self.vertexs[self.name[1]]
        vertex3 = self.vertexs[self.name[2]]
        eq = Equation(vertex1 + vertex2 + vertex3, 180)
        self.equations.append(eq)


    # Phát sinh sự kiện: tia phân giác từ 1 góc trong tam giác, cắt cạnh đối diện tại 1 điểm thì chia đôi góc và tạo thành 2 tam giác khác
    def set_bisector(self, from_vertex, to_vertex):

        # generate 2 new triangle
        vertex1, vertex2 = self.get_other_vertices(from_vertex)

        child_triangle1 = Triangle(sort_name(vertex1+from_vertex+to_vertex))
        child_triangle2 = Triangle(sort_name(vertex2+from_vertex+to_vertex))

        # and angle_name in new 2 triangle = angle_name/2
        child_triangle1.set_angle(from_vertex, self.vertexs[from_vertex]/2)
        child_triangle1.set_angle(vertex1, self.vertexs[vertex1])

        child_triangle2.set_angle(from_vertex, self.vertexs[from_vertex]/2)
        child_triangle2.set_angle(vertex2, self.vertexs[vertex2])

        return child_triangle1, child_triangle2

    
    # Phát sinh sự kiện: tia từ 1 góc cắt cạnh đối diện tại 1 điểm
    def set_ray(self, from_vertex, to_vertex, middle_vertex = None):

        results = []

        # generate 2 new triangle
        vertex1, vertex2 = self.get_other_vertices(from_vertex)

        triangle1 = Triangle(sort_name(vertex1+from_vertex+to_vertex))
        triangle2 = Triangle(sort_name(vertex2+from_vertex+to_vertex))

        triangle1.set_angle(vertex1, self.vertexs[vertex1])
        triangle2.set_angle(vertex2, self.vertexs[vertex2])

        results.extend([triangle1, triangle2])

        if middle_vertex is not None:
            vertex_1 = triangle1.get_other_vertices(from_vertex+to_vertex)
            triangle1_1, triangle1_2 = triangle1.set_ray(vertex_1, middle_vertex)

            vertex_2 = triangle2.get_other_vertices(from_vertex+to_vertex)
            triangle2_1, triangle2_2 = triangle2.set_ray(vertex_2, middle_vertex)

            results.extend([triangle1_1, triangle1_2, triangle2_1, triangle2_2])

        return results