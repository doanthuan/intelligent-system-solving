from cokb import Cokb
from sympy import simplify

if __name__ == "__main__":

    '''
    Bài 1
    '''
    # solve = Cokb()
    # # Cho tam giác ABC
    # #solve.add_event("TRIANGLE", "ABC")
    # solve.set_triangle("ABC")
    # # Với góc A
    # #solve.add_event("ANGLE", ("BAC", 60))
    # solve.set_angle("BAC", 60)
    # # Với góc C
    # solve.set_angle("ACB", 50)

    # ## tia phân giác góc B của tam giác ABC, cắt cạnh đối diện tại D
    # #solve.add_event("BISECTOR", ('ABC', 'B','D'))
    # solve.set_bisector_in('ABC', 'B','D')

    # # xác định góc ADB và CDB
    # solve.add_goal(1 , ("ANGLE", "ADB"))
    # solve.add_goal(1 , ("ANGLE", "CDB"))

    # solve.suy_dien_tien()

    '''
    Bài 2
    '''
    solve2 = Cokb()
    #solve2.add_event("TRIANGLE", "ABC")
    solve2.set_triangle("ABC")

    # tia phân giác góc B, cắt cạnh đối diện tại D
    #solve2.add_event("RAY", ('ABC', 'B', 'K', 'M'))
    solve2.set_ray('ABC', 'B', 'K', 'M')

    solve2.add_goal(2 , ("ANGLE", "AMK", "ABK")) # So sánh


    solve2.suy_dien_tien()







    
