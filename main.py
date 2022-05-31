from cokb import Cokb
from sympy import simplify

if __name__ == "__main__":

    '''
    Bài 1
    '''
    solve = Cokb()
    # Cho tam giác ABC
    #solve.event_1("TRIANGLE", "ABC")
    solve.add_event("TRIANGLE", "ABC")
    # Với góc A
    solve.add_event("ANGLE", ("BAC", 60))
    # Với góc C
    solve.add_event("ANGLE", ("ACB", 50))

    # # tia phân giác góc B của tam giác ABC, cắt cạnh đối diện tại D
    solve.add_event("BISECTOR", ('ABC', 'B','D'))

    # xác định góc ADB và CDB
    solve.add_goal(1 , ("TRIANGLE", "ADB", "ANGLE", "D"))
    solve.add_goal(1 , ("TRIANGLE", "CDB", "ANGLE", "D"))

    solve.suy_dien_tien()

    # # Giả thiết cho tam giác ABC với góc A = 60, góc C = 50

    # triangle = Triangle("ABC")
    # triangle.set_angle("A", 60)
    # triangle.set_angle("C", 50)

    # solve.add_triangle(triangle)

    # # tia phân giác góc B, cắt tại D
    # solve.draw_bisector(triangle.name, "B", "D")

    # # Câu hỏi: tìm góc ADB
    # angle = solve.find_angle("ADB")
    # print("Angle ADB:", angle)

    # # Câu hỏi: tìm góc CDB
    # angle = solve.find_angle("CDB")
    # print("Angle CDB:", angle)

    # '''
    # Bài 2
    # '''
    # solve2 = Cokb()

    # solve2.add_events(1, ("TRIANGLE", "ABC"))

    # # # tia phân giác góc B, cắt cạnh đối diện tại D
    # solve2.add_events(2, ("TRIANGLE", "ABC", "RAY", ['B','K','M']))

    # solve2.add_goal(2 , ("TRIANGLE", "ADB", "ANGLE", "D")) # So sánh







    
