from typing import Tuple, Type, NewType
from unittest.loader import VALID_MODULE_NAME

from sympy import symbols, Eq, Rational
from angle import Angle
from ceq import Ceq
from cobj import Cobj
from equation import Equation
from line import Line
from crel import Crel
from point import Point
from ruleobj import Rule
from utils import sort_name
from vertex import Vertex

# Attributes: A,B,C,a,b,c,S,p,R

# F: tập các phương trình, quan hệ tính toán, sự kiện vốn có của tam giác. Vd: A+B+C=180, A > 0, B > 0, a + b > C...

# Rules: A=b <=> a=b; a**2 + b**2 + c**2 => A=90; ...

class Triangle:
    # def __init__(self, name = "ABC"):

    #     # tri name
    #     self.name = Triangle.tri_name(name)

    #     # 3 edges
    #     self.edges = {}
    #     self.edges[name[0]+name[1]] = Line(name[0]+name[1])
    #     self.edges[name[1]+name[2]] = Line(name[1]+name[2])
    #     self.edges[name[2]+name[0]] = Line(name[2]+name[0])

    #     # 3 angles
    #     self.angles = {}
    #     self.angles[name[0]] = Angle(self.angle_name(name[0]))
    #     self.angles[name[1]] = Angle(self.angle_name(name[1]))
    #     self.angles[name[2]] = Angle(self.angle_name(name[2]))
    #     self.angles_out = {}

    #     self.run_rules()

    def __new__(cls, name):
        #self = Symbol.__new__(self, name,  positive=True)
        #obj = Symbol.__new__(cls, name, positive=True)
        if len(name) != 3:
            raise Exception("Create Triangle Error. Triangle name must be 3 characters")

        name = Triangle.tri_name(name)
        if name not in Cobj.triangles.keys():
            obj = object.__new__(cls)
            # tri name
            obj.name = name

            # 3 points
            obj.points = {}
            obj.points[name[0]] = Point(name[0])
            obj.points[name[1]] = Point(name[1])
            obj.points[name[2]] = Point(name[2])

            # 3 edges
            obj.edges = {}
            obj.edges[name[0]+name[1]] = Line(name[0]+name[1])
            obj.edges[name[1]+name[2]] = Line(name[1]+name[2])
            obj.edges[name[2]+name[0]] = Line(name[2]+name[0])

            # 3 angles
            obj.angles = {}
            obj.angles[name[0]] = Angle(obj.angle_name(name[0]))
            obj.angles[name[1]] = Angle(obj.angle_name(name[1]))
            obj.angles[name[2]] = Angle(obj.angle_name(name[2]))
            obj.angles_out = {}

            obj.run_rules()
            Cobj.triangles[name] = obj

        return Cobj.triangles[name]
    
    @staticmethod
    def from_lines(a: Line, b: Line):
        if not a.is_connect(b):
            return False
        A, B, C = a.get_points(b)
        return Triangle(A + B + C)

    @staticmethod
    def is_triangle(a: Line, b: Line):
        # c_points = Line.get_connect_points(a,b,c)
        # if len(c_points) != 3:
        #     return False

        # if c_points[0] != c_points[1] and c_points[1] != c_points[2] and c_points[0] != c_points[2]:
        #     return True

        # return False
        return a.is_connect(b)

    @staticmethod
    def tri_name(name):
        min_value = min(name)
        min_index = name.index(min_value)
        result = name[min_index] + name[(min_index+1)%3] + name[(min_index+2)%3]
        return result
        #return sort_name(name)

    def angle_name(self, v):
        v1, v2 = self.get_other_points(v)
        #vertexs = sort_name(vertex1 + vertex2)
        return v1 + v + v2

    def get_other_points(self, vertex_name):
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
        #Ceq(self.angles[self.name[0]].symb + self.angles[self.name[1]].symb + self.angles[self.name[2]].symb, 180)
        Ceq(Angle(self.name[2]+self.name[0]+self.name[1]).symb + Angle(self.name[0]+self.name[1]+self.name[2]).symb + Angle(self.name[1]+self.name[2]+self.name[0]).symb, 180)

    def set_angle_out(self, from_v, ray_name = None):
        if ray_name is None:
            ray_name = "x"
        v1, v2 = self.get_other_points(from_v)
        
        self.angles_out[from_v] = angle(ray_name + from_v + v1)
        
        Ceq(self.angles_out[from_v] + self.angles[from_v], 180)


    # Phát sinh sự kiện: tia phân giác từ 1 góc trong tam giác, cắt cạnh đối diện tại 1 điểm thì chia đôi góc và tạo thành 2 tam giác khác
    def set_bisector_in(self, from_v, to_v):

        v1, v2 = self.get_other_points(from_v)

        # tia phân giác cắt đoạn v1-v2 tại điểm to_v
        Line(from_v + to_v)
        Ceq(Angle(v1 + from_v + to_v).symb, Angle(v1 + from_v + v2).symb/2)
        Ceq(Angle(to_v + from_v + v2).symb, Angle(v1 + from_v + v2).symb/2)
        
        # điểm to_v thuộc đoạn thẳng v1 v2 -> tạo thành 2 đoạn mới
        Line(v2 + v1).add_point(to_v)


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
        v1, v2 = self.get_other_points(from_v)

        # generate 2 new triangle
        # Triangle(v1 + from_v + to_v)
        # Triangle(to_v + from_v + v2)

        # tia phân giác đi qua điểm m_v
        Line(from_v + to_v).add_point(m_v)

        # điểm to_v nằm trên đoạn thẳng v1 v2
        Line(v2 + v1).add_point(to_v)
        
        Line(m_v + v1)
        Line(v2 + m_v)

        

        # Ceq(tri1.angles[v1], self.angles[v1])
        # Ceq(tri2.angles[v2], self.angles[v2])

        #Ceq(tri1.angles[to_v] + tri2.angles[to_v], 180)

        #Ceq(tri1.angles[from_v] + tri2.angles[from_v], self.angles[from_v])

        #results.extend([tri1, tri2])

        # if m_v is not None:
        #     tri1_1, tri1_2 = tri1.set_ray(v1, m_v)
        #     tri2_1, tri2_2 = tri2.set_ray(v2, m_v)

        #     # one more triangle created 
        #     tri3 = Triangle(v1 + m_v +  v2)

        #     Ceq(tri3.angles[v1], tri1_1.angles[v1])
        #     Ceq(tri3.angles[v2], tri2_2.angles[v2])
            
        #     Ceq(tri3.angles[m_v], tri1_1.angles[m_v] + tri2_2.angles[m_v])

        #     results.extend([tri1_1, tri1_2, tri2_1, tri2_2, tri3])

        # return results

    def set_bisector_out(self, from_v, ray_name):
        # if don't have angle out yet, set it
        if from_v not in self.angles_out:
            self.set_angle_out(from_v)

        # generate 2 new Cequal angles
        angle_out_name = str(self.angles_out[from_v])
        angle_out_1 = angle(angle_out_name[0] + angle_out_name[1] + ray_name)
        angle_out_2 = angle(ray_name + angle_out_name[1] + angle_out_name[2])

        Ceq(angle_out_1, self.angles_out[from_v]/2)
        Ceq(angle_out_2, self.angles_out[from_v]/2)

        # => 2 góc so le trong
        v1, v2 = self.get_other_points(from_v)
        angle_out_2_obj = get_angle_obj(str(angle_out_2))
        tri_angle_v1 = get_angle_obj(str(self.angles[v1]))
        add_relation(Crel("SO_LE_TRONG", angle_out_2_obj, tri_angle_v1))

        # Phát sinh sự kiện: kẻ đường cao trong tam giác, cắt cạnh đối diện tại 1 điểm
    def set_height(self, from_v, to_v):

        # generate 2 new triangle
        v1, v2 = self.get_other_points(from_v)

        tri1 = Triangle(v1 + from_v + to_v)
        tri2 = Triangle(to_v + from_v + v2)

        Ceq(tri1.angles[v1], self.angles[v1])
        Ceq(tri2.angles[v2], self.angles[v2])

        tri1.set_angle(to_v, 90)
        tri2.set_angle(to_v, 90)

        Ceq(tri1.angles[from_v] + tri2.angles[from_v], self.angles[from_v])

        return tri1, tri2

    
    
