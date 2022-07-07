from __future__ import annotations
from angle import Angle
from ceq import Ceq
from cobj import Cobj
from line import Line
from point import Point

# Attributes: A,B,C,a,b,c,S,p,R

# F: tập các phương trình, quan hệ tính toán, sự kiện vốn có của tam giác. Vd: A+B+C=180, A > 0, B > 0, a + b > C...

# Rules: A=b <=> a=b; a**2 + b**2 + c**2 => A=90; ...



class Triangle:
    
    def __new__(cls, name):
        if len(name) != 3:
            raise Exception("Create Triangle Error. Triangle name must be 3 characters")
        
        triangle = Cobj.get_triangle(name)
        if triangle is not None:
            return triangle

        name = Cobj.tri_name(name)
        obj = object.__new__(cls)
        
        Cobj.triangles[name] = obj
        return obj
    
    def __init__(self, name):
        if not hasattr(self, 'name'):
            # tri name
            self.name = name

            # 3 vertexts
            self.vertexs = {}
            self.vertexs[name[0]] = Point(name[0])
            self.vertexs[name[1]] = Point(name[1])
            self.vertexs[name[2]] = Point(name[2])

            # 3 edges
            self.edges = {}
            self.edges[name[0]+name[1]] = Line(name[0]+name[1])
            self.edges[name[1]+name[2]] = Line(name[1]+name[2])
            self.edges[name[2]+name[0]] = Line(name[2]+name[0])

            # 3 angles
            self.angles = {}
            self.angles[name[0]] = Angle(self.angle_name(name[0]))
            self.angles[name[1]] = Angle(self.angle_name(name[1]))
            self.angles[name[2]] = Angle(self.angle_name(name[2]))

            # 3 heights
            self.heights = {}
            self.height_center = None

            # 3 bisectors
            self.bisectors = {}
            self.bisector_center = None

            # inside points
            self.points = {}

            self.run_rules()

    def run_rules(self):
        rule_01(self)
        rule_02(self)
        rule_03(self)

    def angle_name(self, v):
        v1, v2 = self.get_other_vertexs(v)
        #vertexs = sort_name(vertex1 + vertex2)
        return v1 + v + v2

    def get_other_vertexs(self, vertex_name):
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



    def part_of(self, tri: Triangle) -> str:
        # for angle_i in self.angles.values():
        #     for angle_j in tri.angles.values():
                # if angle_j.is_adjacent_parent(angle_i) and angle_j.name[2] == angle_i.name[2]:
                #     return angle_i.name[1] + angle_i.name[2] + angle_i.name[0] + angle_j.name[0]
                # if angle_j.is_adjacent_parent(angle_i) and angle_j.name[0] == angle_i.name[0]:
                #     return angle_i.name[0] + angle_i.name[1] + angle_i.name[2] + angle_j.name[2]
        if self.name == tri.name or len(tri.points) == 0:
            return None
        #tri_points = tri.name+''.join(tri.points)
        for v in self.name:
            v1, v2 = self.get_other_vertexs(v)
            if v in tri.name and v2 in tri.name and v1 in tri.points:
                new_name = tri.name.replace(v, "")
                new_name = new_name.replace(v2, "")
                return v + v2 + v1 + new_name
        return None


    # Tia phân giác trong
    def set_bisector_in(self, from_v, to_v = None):
        if to_v is None:
            to_v = Cobj.get_rd_ray()

        # tia phân giác
        self.bisectors[from_v] = Line(from_v + to_v)
        self.run_rules()

    # Giao điểm tia phân giác trong
    def set_bisector_center(self, c_p):
        self.bisector_center = c_p
        self.run_rules()
              

    # Đường cao
    def set_height(self, from_v, to_v):
        self.heights[from_v] = Line(from_v + to_v)
        self.run_rules()
        
    # Phát sinh sự kiện: tia từ 1 góc cắt cạnh đối diện tại 1 điểm
    def set_ray(self, from_v, m_v, to_v):
        
        v1, v2 = self.get_other_vertexs(from_v)

        if m_v is not None:
            self.points[m_v] = m_v

            # tia đi qua điểm m_v
            points = from_v + m_v
            if to_v is not None:
                points += to_v
            Line.from_points(points)

            # điểm to_v nằm trên đoạn thẳng v1 v2
            if to_v is not None:
                Line.from_points(v2 + to_v + v1)
            
            # nối 2 đỉnh còn lại
            Line(v1 + m_v)
            Line(v2 + m_v)
        self.run_rules()

    def set_bisector_out(self, from_v, ray_name):
        v1, v2 = self.get_other_vertexs(from_v)
        
        # vẽ tia cho góc ngoài
        out_ray = "x"
        Line(v2 + out_ray).add_point(from_v)


        # kẻ tia phân giác
        Line(from_v + ray_name)
        Ceq(Angle(out_ray + from_v + ray_name).symb, Angle(out_ray + from_v + v1).symb/2)
        Ceq(Angle(ray_name + from_v + v1).symb, Angle(out_ray + from_v + v1).symb/2)
        self.run_rules()


    


'''
RULES Nội Tại
'''
#RULE1: A + B + C = 180 độ
def rule_01(tri: Triangle):
    #Ceq(self.angles[self.name[0]].symb + self.angles[self.name[1]].symb + self.angles[self.name[2]].symb, 180)
    angle1 = Angle(tri.name[2]+tri.name[0]+tri.name[1])
    angle2 = Angle(tri.name[0]+tri.name[1]+tri.name[2])
    angle3 = Angle(tri.name[1]+tri.name[2]+tri.name[0])
    Ceq( angle1.symb + angle2.symb + angle3.symb, 180)

# định lý về tia phân giác, đường cao trong tam giác
def rule_02(tri: Triangle):
    for from_v in tri.vertexs:
        v1, v2 = tri.get_other_vertexs(from_v)
        to_vs = []
        if from_v in tri.heights.keys():
            to_v = tri.heights[from_v].name[1]
            Angle(from_v + to_v + v1, 90)
            Angle(v2 + to_v + from_v, 90)
            to_vs.append(to_v)

        if from_v in tri.bisectors.keys():
            to_v = tri.bisectors[from_v].name[1]
            Ceq(Angle(v1 + from_v + to_v).symb, Angle(v1 + from_v + v2).symb/2)
            Ceq(Angle(to_v + from_v + v2).symb, Angle(v1 + from_v + v2).symb/2)
            if not tri.bisectors[from_v].is_ray:
                to_vs.append(to_v)
        
        if len(to_vs) == 2 and Angle(from_v + v2 + v1).value is not None and Angle(from_v + v2 + v1).value < 45: # nếu góc bên trái nhỏ hơn 45 độ
            to_vs = to_vs.reverse()
        
        Line(v2 + v1).add_point(to_vs)

# tia phân giác tới giao điểm 3 tia
def rule_03(triangle: Triangle):
    if triangle.bisector_center is not None:
        for from_v in triangle.vertexs:
            if from_v in triangle.bisectors.keys():
                triangle.bisectors[from_v].add_point(triangle.bisector_center)  

  
    
