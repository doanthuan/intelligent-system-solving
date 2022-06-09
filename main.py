from cokb import Cokb
from sympy import simplify

if __name__ == "__main__":

    '''
    Bài 1
    '''
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

    '''
    Bài 2
    '''
    solver2 = Cokb()
    #solve2.add_event("TRIANGLE", "ABC")
    solver2.set_triangle("ABC")

    # tia phân giác góc B, cắt cạnh đối diện tại D
    #solve2.add_event("RAY", ('ABC', 'B', 'K', 'M'))
    solver2.set_ray('ABC', 'B', 'K', 'M')

    solver2.add_goal(2 , ("ANGLE", "AMK", "ABK")) # So sánh

    solver2.solve_goals()







    
