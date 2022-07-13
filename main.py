from program import Program
from sympy import Eq, simplify

from relation import Relation
from line import Line
from cobj import Cobj

if __name__ == "__main__":
    from angle import Angle

    # '''
    # Bài 2 - 137 - HH 7
    # '''
    # program = Program()
    # # Cho tam giác ABC
    # program.set_triangle("ABC")
    # # Với góc A
    # program.set_angle("ABC", "A", 60)
    # # Với góc C
    # program.set_angle("ABC", "C", 50)

    # ## tia phân giác góc B của tam giác ABC, cắt cạnh đối diện tại D
    # program.set_bisector_in('ABC', 'B','D')

    # # xác định góc ADB và CDB
    # program.add_goal(1 , ("ANGLE", "ADB"))
    # program.add_goal(1 , ("ANGLE", "CDB"))

    # program.solve()

    '''
    Bài 2
    '''
    program2 = Program()
    program2.set_triangle("ABC")

    program2.set_ray('ABC', 'B', 'M', 'K')

    program2.add_goal(2 , ("ANGLE", "AMK", "ABK")) # So sánh
    #solver2.add_goal(2 , ("ANGLE", "AMC", "ABC")) # So sánh

    program2.solve()

    # '''
    # Bài 3
    # '''
    # solver3 = Program()
    # solver3.set_triangle("ABC")

    # solver3.set_height('ABC', 'B', 'H')
    # solver3.set_height('ABC', 'C', 'K')

    # solver3.add_goal(2 , ("ANGLE", "ABH", "KCA")) # So sánh

    # solver3.solve() 

    # '''
    # Bài 4
    # '''
    # solver4 = Program()
    # solver4.set_triangle("ABC")

    # solver4.set_angle('ABC', 50)
    # solver4.set_angle('BCA', 50)

    # solver4.set_bisector_out('ABC', 'A', 'm')
    
    # solver4.add_goal(3 , Relation("SONG_SONG", Line("Am"), Line("BC"))) # chứng mình 1 mối liên hệ

    # solver4.solve()

    # '''
    # Bài 8 - Trang 138 Bài Tập Hình Học lớp 7
    # '''
    # solver = Program()
    # solver.set_triangle("ABC")

    # solver.set_angle('CAB', 100)

    # solver.set_equation(Eq(Angle("ABC").symb - Angle("BCA").symb, 20))
    
    # solver.add_goal(1 , ("ANGLE", "ABC"))
    # solver.add_goal(1 , ("ANGLE", "BCA"))

    # solver.solve() 


    # '''
    # Bài 9 - Trang 138 Bài Tập Hình Học lớp 7
    # '''
    # solver = Program()
    # solver.set_triangle("ABC")

    # solver.set_angle('CAB', 90)

    # solver.set_height('ABC', 'A', 'H')

    # solver.add_goal(4 , ("ANGLE", "ABC"))

    # solver.solve()

    # '''
    # Bài 11 - Trang 138 Bài Tập Hình Học lớp 7
    # '''
    # solver = Program()
    # solver.set_triangle("ABC")

    # solver.set_angle('ABC', 70)

    # solver.set_angle('BCA', 30)

    # solver.set_bisector_in('ABC', 'A', 'D')

    # solver.set_height('ABC', 'A', 'H')

    # solver.add_goal(1 , ("ANGLE", "CAB"))
    # solver.add_goal(1 , ("ANGLE", "HDA"))
    # solver.add_goal(1 , ("ANGLE", "HAD"))

    # solver.solve()

    # '''
    # Bài 12 - Trang 138 Bài Tập Hình Học lớp 7
    # '''
    # program = Program()
    # program.set_triangle("ABC")
    # program.set_bisector_in('ABC', 'B')
    # program.set_bisector_in('ABC', 'C')
    # program.set_bisector_center('ABC', 'I')

    # program.set_angle('ABC', 80)
    # program.set_angle('BCA', 40)

    # program.add_goal(1 , ("ANGLE", "CIB"))
    # program.solve()

    # program.reset_state()
    # program.set_triangle("ABC")
    # program.set_bisector_in('ABC', 'B')
    # program.set_bisector_in('ABC', 'C')
    # program.set_bisector_center('ABC', 'I')

    # program.set_angle('CAB', 80)

    # program.solve()

    # '''
    # Bài 15 - Trang 138 Bài Tập Hình Học lớp 7
    # '''
    # program = Program()
    # program.set_triangle("ABC")
    # program.set_angle('CAB', 90)

    # program.set_ray('ABC', 'B', 'E')

    # program.add_goal(3 , Relation("GOC_TU", Angle("CEB"))) # chứng mình 1 mối liên hệ
    # program.solve()

    # '''
    # Bài 23 - Trang 140 - HH7
    # '''
    # program = Program()
    # program.set_triangle_equal("ABC","DEF")
    # program.set_angle('CAB', 55)
    # program.set_angle('DEF', 55)
    

    # program.add_goal(1 , ("ANGLE", "ABC"))
    # program.add_goal(1 , ("ANGLE", "BCA"))
    # program.add_goal(1 , ("ANGLE", "EFD"))
    # program.add_goal(1 , ("ANGLE", "FDE"))
    # program.solve()

    # '''
    # Bài 28 - Trang 141 - HH7
    # '''
    # program = Program()
    # program.set_triangle("ABC")
    # program.set_triangle("ADB")
    # program.set_edge("AB", 3)
    # program.set_edge("BC", 3)
    # program.set_edge("CA", 3)

    # program.set_edge("AD", 2)
    # program.set_edge("DB", 2)
        
    # program.add_goal(3 , Eq(Angle("CAD").symb, Angle("DBC").symb)) # chứng minh
    # program.solve()

    # '''
    # Bài 32 - Trang 141 - HH7
    # '''
    # program = Program()
    # program.set_triangle("ABC")
    # Line("AB").set_equal(Line("AC"))

    # Line("BC").add_midpoint("M")
        
    # program.add_goal(3 , Eq(Angle("AMC").symb, 90)) # chứng minh
    # program.solve()










    
