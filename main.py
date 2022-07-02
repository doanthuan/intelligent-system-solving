from angle import Angle
from program import Program
from sympy import Eq, simplify
from equation import Equation
from line import Line

from relation import Relation

if __name__ == "__main__":

    # '''
    # Bài 1
    # '''
    # program = Program()
    # # Cho tam giác ABC
    # #solve.add_event("TRIANGLE", "ABC")
    # program.set_triangle("ABC")
    # # Với góc A
    # #solve.add_event("ANGLE", ("BAC", 60))
    # program.set_angle("BAC", 60)
    # # Với góc C
    # program.set_angle("ACB", 50)

    # ## tia phân giác góc B của tam giác ABC, cắt cạnh đối diện tại D
    # #solve.add_event("BISECTOR", ('ABC', 'B','D'))
    # program.set_bisector_in('ABC', 'B','D')

    # # xác định góc ADB và CDB
    # program.add_goal(1 , ("ANGLE", "ADB"))
    # program.add_goal(1 , ("ANGLE", "CDB"))
    # # solve.find_angle("ADB")
    # # solve.find_angle("CDB")

    # program.solve_goals()

    # '''
    # Bài 2
    # '''
    # program2 = Program()
    # program2.set_triangle("ABC")

    # # tia phân giác góc B, cắt cạnh đối diện tại D
    # program2.set_ray('ABC', 'B', 'K', 'M')

    # program2.add_goal(2 , ("ANGLE", "AMK", "ABK")) # So sánh
    # #solver2.add_goal(2 , ("ANGLE", "AMC", "ABC")) # So sánh

    # program2.solve_goals()

    # '''
    # Bài 3
    # '''
    # solver3 = Program()
    # solver3.set_triangle("ABC")

    # solver3.set_height('ABC', 'B', 'H')
    # solver3.set_height('ABC', 'C', 'K')

    # solver3.add_goal(2 , ("ANGLE", "ABH", "KCA")) # So sánh

    # solver3.solve_goals() 

    # '''
    # Bài 4
    # '''
    # solver4 = Program()
    # solver4.set_triangle("ABC")

    # solver4.set_angle('ABC', 50)
    # solver4.set_angle('BCA', 50)

    # solver4.set_bisector_out('ABC', 'A', 'm')
    
    # solver4.add_goal(3 , Relation("SONG_SONG", Line("Am"), Line("BC"))) # chứng mình 1 mối liên hệ

    # solver4.solve_goals()

    # '''
    # Bài 8 - Trang 138 Bài Tập Hình Học lớp 7
    # '''
    # solver = Program()
    # solver.set_triangle("ABC")

    # solver.set_angle('CAB', 100)

    # solver.set_equation(Eq(Angle("ABC").symb - Angle("BCA").symb, 20))
    
    # solver.add_goal(1 , ("ANGLE", "ABC"))
    # solver.add_goal(1 , ("ANGLE", "BCA"))

    # solver.solve_goals() 


    # '''
    # Bài 9 - Trang 138 Bài Tập Hình Học lớp 7
    # '''
    # solver = Program()
    # solver.set_triangle("ABC")

    # solver.set_angle('CAB', 90)

    # solver.set_height('ABC', 'A', 'H')

    # solver.add_goal(4 , ("ANGLE", "ABC"))

    # solver.solve_goals()

    '''
    Bài 11 - Trang 138 Bài Tập Hình Học lớp 7
    '''
    solver = Program()
    solver.set_triangle("ABC")

    solver.set_angle('ABC', 70)

    solver.set_angle('BCA', 30)

    solver.set_bisector_in('ABC', 'A', 'D')

    solver.set_height('ABC', 'A', 'H')

    solver.add_goal(1 , ("ANGLE", "CAB"))
    solver.add_goal(1 , ("ANGLE", "HDA"))
    solver.add_goal(1 , ("ANGLE", "HAD"))

    solver.solve_goals() 








    
