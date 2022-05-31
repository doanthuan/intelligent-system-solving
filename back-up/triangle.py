from typing import Tuple, Type, NewType
from vertex import Vertex

class Triangle:

    def __init__(self, name = "ABC"):

        name = ''.join(sorted(name))
        self.name = name
        
        # 3 vertexs

        self.vertex1 = Vertex(name[0])
        self.vertex2 = Vertex(name[1])
        self.vertex3 = Vertex(name[2])

        vertexs = {}
        vertexs[name[0]] = self.vertex1
        vertexs[name[1]] = self.vertex2
        vertexs[name[2]] = self.vertex3
        self.vertexs = vertexs

    def get_other_vertices(self, name):
        vertexs = []
        for key, value in self.vertexs.items():
            if key not in name:
                vertexs.append(value)
                
        return tuple(vertexs)

    def set_angle(self, vertex_name, angle):
        
        vertex1 = self.vertexs[vertex_name]
        vertex1.angle = angle

        vertex2, vertex3 = self.get_other_vertices(vertex_name)

        # sum 3 angle in triangle = 180
        if vertex2.is_none() and vertex3.has_value():
            vertex2.angle = 180 - (vertex1.angle + vertex3.angle)
        
        if vertex3.is_none() and vertex2.has_value():
            vertex3.angle = 180 - (vertex1.angle + vertex2.angle)

    # set bisector - tia phân giác
    def draw_bisector(self, from_vertex, to_vertex):

        # generate 2 new triangle
        vertex1, vertex2 = self.get_other_vertices(from_vertex)

        child_triangle1 = Triangle(''.join(sorted(vertex1.name+from_vertex+to_vertex)))
        child_triangle2 = Triangle(''.join(sorted(vertex2.name+from_vertex+to_vertex)))

        # and angle_name in new 2 triangle = angle_name/2
        child_triangle1.set_angle(from_vertex, self.vertexs[from_vertex].angle/2)
        child_triangle1.set_angle(vertex1.name, self.vertexs[vertex1.name].angle)

        child_triangle2.set_angle(from_vertex, self.vertexs[from_vertex].angle/2)
        child_triangle2.set_angle(vertex2.name, self.vertexs[vertex2.name].angle)

        return child_triangle1, child_triangle2

    
    # set ray - tia qua
    def draw_ray(self, from_vertex: str, to_vertex: str):

        # generate 2 new triangle
        vertex1, vertex2 = self.get_other_vertices(from_vertex)

        child_triangle1 = Triangle(''.join(sorted(vertex1.name+from_vertex+to_vertex)))
        child_triangle2 = Triangle(''.join(sorted(vertex2.name+from_vertex+to_vertex)))

        #child_triangle1.set_angle(from_vertex, self.vertexs[from_vertex].angle/2)
        child_triangle1.set_angle(vertex1.name, self.vertexs[vertex1.name].angle)

        #child_triangle2.set_angle(from_vertex, self.vertexs[from_vertex].angle/2)
        child_triangle2.set_angle(vertex2.name, self.vertexs[vertex2.name].angle)

        return child_triangle1, child_triangle2