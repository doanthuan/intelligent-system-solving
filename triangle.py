from __future__ import annotations

from ceq import Ceq
from cobj import Cobj
from angle import Angle
from line import Line
from log import Log
from point import Point
from relation import Relation

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

            # 3 vertexs
            self.vertexs = {}
            self.vertexs[name[0]] = Point(name[0])
            self.vertexs[name[1]] = Point(name[1])
            self.vertexs[name[2]] = Point(name[2])
            self.v1 = Point(name[0])
            self.v2 = Point(name[1])
            self.v3 = Point(name[2])
            #self.vertexs = [str(self.v1),str(self.v2),str(self.v3)]

            # 3 edges
            self.edges = {}
            self.edges[name[0]] = Line(name[0]+name[1])
            self.edges[name[1]] = Line(name[1]+name[2])
            self.edges[name[2]] = Line(name[2]+name[0])
            self.e1 = Line(name[0]+name[1])
            self.e2 = Line(name[1]+name[2])
            self.e3 = Line(name[2]+name[0])

            # 3 angles
            self.angles = {}
            self.angles[name[0]] = Angle(self.angle_name(name[0]))
            self.angles[name[1]] = Angle(self.angle_name(name[1]))
            self.angles[name[2]] = Angle(self.angle_name(name[2]))
            self.a1 = Angle(self.angle_name(name[0]))
            self.a2 = Angle(self.angle_name(name[1]))
            self.a3 = Angle(self.angle_name(name[2]))

            # 3 heights
            self.heights = {}
            self.height_center = None

            # 3 bisectors
            self.bisectors = {}
            self.bisector_center = None

            # 3 medians
            self.medians = {}
            self.median_center = None

            # inside points
            self.points = {}

            # chu vi
            self.p = None

            self.attrs = None
            self.iso_point = None
            self.rules()

    
    def rules(self):
        rule_01(self)
        rule_02(self)

    def __str__(self):
        return f"TAM_GIAC: {self.name}"

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
    def next_v(self, v):
        i_vertex = self.name.index(v)
        i_next = i_vertex + 1
        if i_next > 2:
            i_next = 0
        return self.name[i_next]

    # def get_other_edges(self, edge):
    #     for e in self.edges:
    #         if e.name == edge.name:
    #             return 

    def is_ident(self, triangle: Triangle) -> bool:
        return self.name == triangle.name

    def part_of(self, tri: Triangle) -> str:
        if self.name == tri.name or len(tri.points) == 0:
            return None
        for v in self.name:
            v1, v2 = self.get_other_vertexs(v)
            if v in tri.name and v2 in tri.name and v1 in tri.points:
                new_name = tri.name.replace(v, "")
                new_name = new_name.replace(v2, "")
                return v + v2 + v1 + new_name
        return None

    def set_angle(self, angle_name, angle_value):
        self.angles[angle_name].set_value(angle_value)

    def set_isosceles(self, v):
        attr = "TG_CAN"
        if self.attrs == attr:
            return

        self.attrs = attr
        self.iso_point = v

        v1, v2 = self.get_other_vertexs(v)

        self.angles[v1].set_equal(self.angles[v2])

        self.edges[v].set_equal(self.edges[v1])

        return Relation.make(attr, self)
        

    def set_equilateral(self):
        attr = "TG_DEU"
        if self.attrs == attr:
            return

        rel = Relation.make(attr, self)

        self.attrs  = attr

        self.a1.set_equal(self.a2)
        self.a1.set_equal(self.a3)

        self.e1.set_equal(self.e2)
        self.e1.set_equal(self.e3)

        
        return rel

    # Tia phân giác trong
    def set_bisector_in(self, from_v, to_v = None):
        if to_v is None:
            to_v = Cobj.get_rd_ray()

        # tia phân giác
        self.bisectors[from_v] = Line(from_v + to_v)

    # Giao điểm tia phân giác trong
    def set_bisector_center(self, c_p):
        self.bisector_center = c_p
              
    # Đường cao
    def set_height(self, from_v, to_v):
        self.heights[from_v] = Line(from_v + to_v)

    # trung tuyến
    def set_median(self, from_v, to_v):
        self.medians[from_v] = Line(from_v + to_v)

    def set_3_lines(self, v):
        if self.bisectors[v] is not None: # tia phân giác -> đường cao, trung tuyến
            self.heights[v] = self.bisectors[v]
            self.medians[v] = self.bisectors[v]
        elif self.heights[v] is not None: # đường cao -> tia phân giác, trung tuyến
            self.bisectors[v] = self.heights[v]
            self.medians[v] = self.heights[v]
        elif self.medians[v] is not None: # trung tuyến -> tia phân giác, đường cao
            self.bisectors[v] = self.medians[v]
            self.heights[v] = self.medians[v]
        
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

    def set_bisector_out(self, from_v, ray_name):
        v1, v2 = self.get_other_vertexs(from_v)
        
        # vẽ tia cho góc ngoài
        out_ray = "x"
        Line(v2 + out_ray).add_point(from_v)


        # kẻ tia phân giác
        Line(from_v + ray_name)
        Ceq(Angle(out_ray + from_v + ray_name).symb, Angle(out_ray + from_v + v1).symb/2)
        Ceq(Angle(ray_name + from_v + v1).symb, Angle(out_ray + from_v + v1).symb/2)


    def set_equal(self, tri: Triangle, v1 = None, v2 = None, v3 = None):
        if v1 is None and v2 is None and v3 is None: # from hypo
            # 3 edges
            self.e1.set_equal(tri.e1)
            self.e2.set_equal(tri.e2)
            self.e3.set_equal(tri.e3)

            # 3 angles
            self.a1.set_equal(tri.a1)
            self.a2.set_equal(tri.a2)
            self.a3.set_equal(tri.a3)
        else: # by edges
            # self.e1.set_equal(tri.edges[v1])
            # self.e2.set_equal(tri.edges[v2])
            # self.e3.set_equal(tri.edges[v3])

            rel = Relation.make("TG_BANG_NHAU", self, tri)
            eq1 = self.a1.set_equal(tri.angles[v1])
            Log.trace_obj(eq1, "(Definition)", [rel])
            eq2 = self.a2.set_equal(tri.angles[v2])
            Log.trace_obj(eq2, "(Definition)", [rel])
            eq3 = self.a3.set_equal(tri.angles[v3])
            Log.trace_obj(eq3, "(Definition)", [rel])

            return rel


#RULE1: A + B + C = 180 độ
def rule_01(tri: Triangle):
    Ceq( tri.a1.symb + tri.a2.symb + tri.a3.symb, 180)

# tam giác cân ( hoặc đều ) -> trung tuyến = tia phân giác = đường cao
def rule_02(triangle: Triangle):
    if triangle.attrs == "TG_CAN":
        v = triangle.iso_point
        triangle.set_3_lines(v)

    if triangle.attrs == "TG_DEU":
        for v in triangle.name:
            triangle.set_3_lines(v)