from typing import Tuple, Type, NewType

from sympy import symbols, Eq, Rational
from equation import Equation
from rule import Rule
from solver import set_equation, set_symbol
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

        self.symbols = {}
        self.equations = []

        # 3 angles

        angle_name_1 = self.get_angle_name(name[0])
        angle_name_2 = self.get_angle_name(name[1])
        angle_name_3 = self.get_angle_name(name[2])

        self.angles = {}
        self.angles[name[0]] = symbols(angle_name_1, positive=True)
        self.angles[name[1]] = symbols(angle_name_2, positive=True)
        self.angles[name[2]] = symbols(angle_name_3, positive=True)
        
        #self.symbols.extend([self.angles[name[0]], self.angles[name[1]], self.angles[name[2]]])
        set_symbol(angle_name_1, self.angles[name[0]])
        set_symbol(angle_name_2, self.angles[name[1]])
        set_symbol(angle_name_3, self.angles[name[2]])
    
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
        if type(angle) in [int, float]:
            #self.angles[vertex_name] = angle
            set_symbol(self.get_angle_name(vertex_name), angle)
        else:
            # eq = Equation(self.angles[vertex_name], angle)
            # self.equations.append(eq)
            set_equation(self.angles[vertex_name], angle)

    '''
    RULES
    '''
    def run_rules(self):
        self.rule_01()
        

    #RULE1: A + B + C = 180 độ
    def rule_01(self):
        set_equation(self.angles[self.name[0]] + self.angles[self.name[1]] + self.angles[self.name[2]], 180)


    # Phát sinh sự kiện: tia phân giác từ 1 góc trong tam giác, cắt cạnh đối diện tại 1 điểm thì chia đôi góc và tạo thành 2 tam giác khác
    def set_bisector(self, from_v, to_v):

        # generate 2 new triangle
        v1, v2 = self.get_other_vertices(from_v)

        triangle1 = Triangle(v1+from_v+to_v)
        triangle2 = Triangle(v2+from_v+to_v)

        # and angle_name in new 2 triangle = angle_name/2
        triangle1.set_angle(v1, self.angles[v1])
        triangle2.set_angle(v2, self.angles[v2])

        triangle1.set_angle(from_v, self.angles[from_v]/2)
        triangle2.set_angle(from_v, self.angles[from_v]/2)

        set_equation(triangle1.angles[to_v] + triangle2.angles[to_v], 180)

        return triangle1, triangle2

    
    # Phát sinh sự kiện: tia từ 1 góc cắt cạnh đối diện tại 1 điểm
    def set_ray(self, from_v, to_v, m_v = None):
        results = []
        '''
        vertex1: A
        vertex2: C
        from_vertex: B
        to_vertex: K
        middle_vertex: M
        '''
        v1, v2 = self.get_other_vertices(from_v) 

        # generate 2 new triangle
        tri1 = Triangle(v1 + from_v + to_v)
        tri2 = Triangle(v2 + from_v + to_v)

        tri1.set_angle(v1, self.angles[v1])
        tri2.set_angle(v2, self.angles[v2])

        set_equation(tri1.angles[to_v] + tri2.angles[to_v], 180)

        set_equation(tri1.angles[from_v] + tri2.angles[from_v], self.angles[from_v])

        results.extend([tri1, tri2])

        if m_v is not None:

            vertex_1 = tri1.get_other_vertices(from_v + to_v)
            tri1_1, tri1_2 = tri1.set_ray(vertex_1, m_v)

            vertex_2 = tri2.get_other_vertices(from_v + to_v)
            tri2_1, tri2_2 = tri2.set_ray(vertex_2, m_v)

            # one more triangle created 
            tri3 = Triangle(m_v + v1 + v2)
            tri3.set_angle(v1, tri1_1.angles[v1])
            tri3.set_angle(v2, tri2_2.angles[v2])
            
            set_equation(tri3.angles[m_v], tri1_1.angles[m_v] + tri2_2.angles[m_v])

            results.extend([tri1_1, tri1_2, tri2_1, tri2_2, tri3])

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