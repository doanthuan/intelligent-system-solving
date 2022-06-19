from cokb import Cokb
from sympy import simplify

from relation import Relation

if __name__ == "__main__":

    # '''
    # Bài 1
    # '''
    # solver = Cokb()
    # # Cho tam giác ABC
    # #solve.add_event("TRIANGLE", "ABC")
    # solver.set_triangle("ABC")
    # # Với góc A
    # #solve.add_event("ANGLE", ("BAC", 60))
    # solver.set_angle("BAC", 60)
    # # Với góc C
    # solver.set_angle("ACB", 50)

    # ## tia phân giác góc B của tam giác ABC, cắt cạnh đối diện tại D
    # #solve.add_event("BISECTOR", ('ABC', 'B','D'))
    # solver.set_bisector_in('ABC', 'B','D')

    # # xác định góc ADB và CDB
    # solver.add_goal(1 , ("ANGLE", "ADB"))
    # solver.add_goal(1 , ("ANGLE", "CDB"))
    # # solve.find_angle("ADB")
    # # solve.find_angle("CDB")

    # solver.solve_goals()

    # '''
    # Bài 2
    # '''
    # solver2 = Cokb()
    # solver2.set_triangle("BCA")

    # # tia phân giác góc B, cắt cạnh đối diện tại D
    # #solve2.add_event("RAY", ('ABC', 'B', 'K', 'M'))
    # solver2.set_ray('ABC', 'B', 'K', 'M')

    # solver2.add_goal(2 , ("ANGLE", "AMK", "ABK")) # So sánh
    # #solver2.add_goal(2 , ("ANGLE", "AMC", "ABC")) # So sánh

    # solver2.solve_goals()

    # '''
    # Bài 3
    # '''
    # solver3 = Cokb()
    # solver3.set_triangle("ABC")

    # solver3.set_height('ABC', 'B', 'H')
    # solver3.set_height('ABC', 'C', 'K')

    # solver3.add_goal(2 , ("ANGLE", "ABH", "ACK")) # So sánh

    # solver3.solve_goals() 

    '''
    Bài 4
    '''
    solver = Cokb()
    solver.set_triangle("ABC")

    solver.set_angle('ABC', 50)
    solver.set_angle('BCA', 50)

    solver.set_angle_out('ABC', 'A')
    
    solver.add_goal(3 , Relation("SONG_SONG","Am","BC")) # chứng mình 1 mối liên hệ

    solver.solve_goals() 








    
