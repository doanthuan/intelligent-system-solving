from typing import Tuple, Type, NewType

from sympy import symbols, Eq, Rational
from angle import Angle
from equation import Equation
from relation import Relation
from rule import Rule
from solver import add_relation, angle, eq, symb
from utils import sort_name
from vertex import Vertex

# Attributes: A,B,C,a,b,c,S,p,R

# F: tập các phương trình, quan hệ tính toán, sự kiện vốn có của tam giác. Vd: A+B+C=180, A > 0, B > 0, a + b > C...

# Rules: A=b <=> a=b; a**2 + b**2 + c**2 => A=90; ...

class Triangle:

    @staticmethod
    def triangle_name(name):
        min_value = min(name)
        min_index = name.index(min_value)
        result = name[min_index] + name[(min_index+1)%3] + name[(min_index+2)%3]
        return result

    def __init__(self, name = "ABC"):

        self.name = Triangle.triangle_name(name)

        self.angleols = {}
        self.equations = []

        # 3 angles
        angle_name_1 = self.angle_name(name[0])
        angle_name_2 = self.angle_name(name[1])
        angle_name_3 = self.angle_name(name[2])

        # self.angles = {}
        # self.angles[name[0]] = symbols(angle_name_1, positive=True)
        # self.angles[name[1]] = symbols(angle_name_2, positive=True)
        # self.angles[name[2]] = symbols(angle_name_3, positive=True)
        
        # #self.symbols.extend([self.angles[name[0]], self.angles[name[1]], self.angles[name[2]]])
        # angle(angle_name_1, self.angles[name[0]])
        # angle(angle_name_2, self.angles[name[1]])
        # angle(angle_name_3, self.angles[name[2]])

        self.angles = {}
        self.angles[name[0]] = angle(angle_name_1)
        self.angles[name[1]] = angle(angle_name_2)
        self.angles[name[2]] = angle(angle_name_3)

        self.angles_out = {}

        self.run_rules()
    
    def angle_name(self, vertex):
        vertex1, vertex2 = self.get_other_vertices(vertex)
        #vertexs = sort_name(vertex1 + vertex2)
        return vertex1 + vertex + vertex2

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

    '''
    RULES Nội Tại
    '''
    def run_rules(self):
        self.rule_01()
        

    #RULE1: A + B + C = 180 độ
    def rule_01(self):
        eq(self.angles[self.name[0]] + self.angles[self.name[1]] + self.angles[self.name[2]], 180)


    def set_angle(self, vertex_name, value):
        # angle_obj = (self.angles[vertex_name])
        # angle_obj.set_value(value)
        angle(self.angle_name(vertex_name), value)

    def set_angle_out(self, from_v, ray_name):
        if ray_name is None:
            ray_name = "x"
        v1, v2 = self.get_other_vertices(from_v)
        
        self.angles_out[from_v] = angle(v1 + from_v + ray_name)
        
        eq(self.angles_out[from_v] + self.angles[from_v], 180)


    # Phát sinh sự kiện: tia phân giác từ 1 góc trong tam giác, cắt cạnh đối diện tại 1 điểm thì chia đôi góc và tạo thành 2 tam giác khác
    def set_bisector_in(self, from_v, to_v):

        # generate 2 new triangle
        v1, v2 = self.get_other_vertices(from_v)

        tri1 = Triangle(v1+from_v+to_v)
        tri2 = Triangle(v2+from_v+to_v)

        # and angle_name in new 2 triangle = angle_name/2
        eq(tri1.angles[v1], self.angles[v1])
        eq(tri2.angles[v2], self.angles[v2])

        eq(tri1.angles[from_v], self.angles[from_v]/2)
        eq(tri2.angles[from_v], self.angles[from_v]/2)

        eq(tri1.angles[to_v] + tri2.angles[to_v], 180)

        return tri1, tri2

    def set_bisector_out(self, from_v, ray_name):
        # if don't have angle out yet, set it
        if from_v not in self.angles_out:
            self.set_angle_out(from_v)

        # generate 2 new equal angles
        angle_out_name = str(self.angles_out[from_v])
        angle_out_1 = angle(angle_out_name[0] + angle_out_name[1] + ray_name)
        angle_out_2 = angle(ray_name + angle_out_name[1] + angle_out_name[2])

        eq(angle_out_1, angle_out_2)

        # => 2 góc so le trong
        add_relation(Relation("SO_LE_TRONG", ))

        # Phát sinh sự kiện: kẻ đường cao trong tam giác, cắt cạnh đối diện tại 1 điểm
    def set_height(self, from_v, to_v):

        # generate 2 new triangle
        v1, v2 = self.get_other_vertices(from_v)

        tri1 = Triangle(v1+from_v+to_v)
        tri2 = Triangle(v2+from_v+to_v)

        eq(tri1.angles[v1], self.angles[v1])
        eq(tri2.angles[v2], self.angles[v2])

        tri1.set_angle(to_v, 90)
        tri2.set_angle(to_v, 90)

        eq(tri1.angles[from_v] + tri2.angles[from_v], 180)

        return tri1, tri2

    
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
        tri2 = Triangle(to_v + from_v + v2)

        eq(tri1.angles[v1], self.angles[v1])
        eq(tri2.angles[v2], self.angles[v2])

        eq(tri1.angles[to_v] + tri2.angles[to_v], 180)

        eq(tri1.angles[from_v] + tri2.angles[from_v], self.angles[from_v])

        results.extend([tri1, tri2])

        if m_v is not None:
            tri1_1, tri1_2 = tri1.set_ray(v1, m_v)
            tri2_1, tri2_2 = tri2.set_ray(v2, m_v)

            # one more triangle created 
            tri3 = Triangle(v1 + m_v +  v2)

            eq(tri3.angles[v1], tri1_1.angles[v1])
            eq(tri3.angles[v2], tri2_2.angles[v2])
            
            eq(tri3.angles[m_v], tri1_1.angles[m_v] + tri2_2.angles[m_v])

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