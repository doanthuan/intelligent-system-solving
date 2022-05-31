from cokb import Solve
from triangle import Triangle

if __name__ == "__main__":

    '''
    Bài 1
    '''
    solve = Solve()

    # Giả thiết cho tam giác ABC với góc A = 60, góc C = 50
    triangle = Triangle("ABC")
    triangle.set_angle("A", 60)
    triangle.set_angle("C", 50)

    solve.add_triangle(triangle)

    # tia phân giác góc B, cắt tại D
    solve.draw_bisector(triangle.name, "B", "D")

    # Câu hỏi: tìm góc ADB
    angle = solve.find_angle("ADB")
    print("Angle ADB:", angle)

    # Câu hỏi: tìm góc CDB
    angle = solve.find_angle("CDB")
    print("Angle CDB:", angle)

    # '''
    # Bài 2
    # '''
    solve2 = Solve()
    triangle = "ABC"
    solve2.add_triangle(triangle)
    solve2.set_ray(triangle, "B", "K", "M")







    
