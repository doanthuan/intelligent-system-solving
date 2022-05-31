from triangle import Triangle

class Solve:

    def __init__(self):
        self.triangles = {}

    def add_triangle(self, triangle):
        if isinstance(triangle, str):
            self.triangles[''.join(sorted(triangle))] = Triangle(triangle)

        if isinstance(triangle, Triangle):
            self.triangles[''.join(sorted(triangle.name))] = triangle
            
        if isinstance(triangle, list):
            for a_tri in triangle:
                self.triangles[''.join(sorted(a_tri.name))] = a_tri
            

    def draw_bisector(self, triangle_name, from_vertex, to_vertex):
        triangle = self.triangles[''.join(sorted(triangle_name))]
        triangle1, triangle2 = triangle.draw_bisector(from_vertex, to_vertex)
        self.add_triangle([triangle1, triangle2])


    # set ray - tia qua
    def draw_ray(self, triangle_name, from_vertex, to_vertex, middle_vertex = None):
        triangle = self.triangles[''.join(sorted(triangle_name))]
        triangle1, triangle2 = triangle.draw_ray(from_vertex, to_vertex)
        self.add_triangle([triangle1, triangle2])

        if middle_vertex is not None:# nếu có điểm nằm tren tia -> vẽ thêm 2 tia của 2 tam giác con
            vertex_1 = triangle1.get_other_vertices(from_vertex+to_vertex)
            triangle1_1, triangle1_2 = triangle1.draw_ray(vertex_1.name, middle_vertex)

            vertex_2 = triangle2.get_other_vertices(from_vertex+to_vertex)
            triangle2_1, triangle2_2 = triangle2.draw_ray(vertex_2.name, middle_vertex)

            self.add_triangle([triangle1_1, triangle1_2, triangle2_1, triangle2_2])
            

    def find_angle(self, angle_name):
        vertex_name = angle_name[1]
        return self.triangles[''.join(sorted(triangle_name))].vertexs[vertex_name].angle

    def compare_angle(angle_name_1, angle_name_2):
