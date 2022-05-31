from oo.ooc import *
from sympy import *

# khởi tạo các symbol
a, b, c, A, B, C, ha, hb, hc, S, p, R, r = symbols('a,b,c,A,B,C,ha,hb,hc,S,p,R,r', positive=True)
# khai báo tham số
m = symbols("m")
TapThamSo = set({m})

init_printing(use_unicode=True)

# khai báo các đẳng thức
# dt1 = (A + B + C, pi)
dt1 = DangThuc(A + B + C, pi, id="dang thuc 1")
# dt2 = (a ** 2, b ** 2 + c ** 2 * 2 * b * c * cos(A))
dt2 = DangThuc(a ** 2, b ** 2 + c ** 2 * 2 * b * c * cos(A), id="dang thuc 2")
# dt3 = (b ** 2, a ** 2 + c ** 2 * 2 * a * c * cos(B))
dt3 = DangThuc(b ** 2, a ** 2 + c ** 2 * 2 * a * c * cos(B), id="dang thuc 3")
# dt4 = (c ** 2, a ** 2 + b ** 2 * 2 * a * b * cos(C))
dt4 = DangThuc(c ** 2, a ** 2 + b ** 2 * 2 * a * b * cos(C), id="dang thuc 4")

# dt5 = (a * sin(B), b * sin(A))
dt5 = DangThuc(a * sin(B), b * sin(A), id="dang thuc 5")
# dt6 = (a * sin(C), c * sin(A))
dt6 = DangThuc(a * sin(C), c * sin(A), id="dang thuc 6")
# dt7 = (b * sin(C), c * sin(B))
dt7 = DangThuc(b * sin(C), c * sin(B), id="dang thuc 7")

# dt8 = (a, 2 * R * sin(A))
dt8 = DangThuc(a, 2 * R * sin(A), id="dang thuc 8")
# dt9 = (b, 2 * R * sin(B))
dt9 = DangThuc(b, 2 * R * sin(B), id="dang thuc 9")
# dt10 = (c, 2 * R * sin(C))
dt10 = DangThuc(c, 2 * R * sin(C), id="dang thuc 10")

# dt11 = (2 * p, a + b + c)
dt11 = DangThuc(2 * p, a + b + c, id="dang thuc 11")
# dt12 = (S, a * ha / 2)
dt12 = DangThuc(S, a * ha / 2, id="dang thuc 12")
# dt13 = (S, b * hb / 2)
dt13 = DangThuc(S, b * hb / 2, id="dang thuc 13")
# dt14 = (S, c * hc / 2)
dt14 = DangThuc(S, c * hc / 2, id="dang thuc 14")

# dt15 = (S, p * r)
dt15 = DangThuc(S, p * r, id="dang thuc 15")

# dt16 = (S, sqrt(p * (p - a) * (p - b) * (p - c)))
dt16 = DangThuc(S, sqrt(p * (p - a) * (p - b) * (p - c)), id="dang thuc 16")
# dt17 = (S, b * c * sin(A) / 2)
dt17 = DangThuc(S, b * c * sin(A) / 2, id="dang thuc 17")
# dt18 = (S, b * a * sin(C) / 2)
dt18 = DangThuc(S, b * a * sin(C) / 2, id="dang thuc 18")
# dt19 = (S, a * c * sin(B) / 2)
dt19 = DangThuc(S, a * c * sin(B) / 2, id="dang thuc 19")

# dt20 = (ha, b * sin(C))
dt20 = DangThuc(ha, b * sin(C), id="dang thuc 20")
# dt21 = (ha, c * sin(B))
dt21 = DangThuc(ha, c * sin(B), id="dang thuc 21")
# dt22 = (hb, a * sin(C))
dt22 = DangThuc(hb, a * sin(C), id="dang thuc 22")
# dt23 = (hb, c * sin(A))
dt23 = DangThuc(hb, c * sin(A), id="dang thuc 23")

# dt24 = (hc, a * sin(B))
dt24 = DangThuc(hc, a * sin(B), id="dang thuc 24")
# dt25 = (hc, b * sin(A))
dt25 = DangThuc(hc, b * sin(A), id="dang thuc 25")

TapDangThuc = set({dt1, dt2, dt3, dt4, dt5, dt6, dt7, dt8, dt9, dt10, dt11, dt12, dt13, dt14, dt15, dt16, dt17, dt18,
                   dt19, dt20, dt21, dt22, dt23, dt24, dt25})

# định nghĩa luật thứ 1
qhb1 = QuanHeBang(a ** 2, b ** 2 + c ** 2, id="quan he bang 1")
kl11 = QuanHeBang(A, pi / 2, id="quan he bang 2")
kl12 = QuanHeVuong(b, c, id="quan he vuong 1")
luat1 = Luat([qhb1], [kl11, kl12], id="luat 1")

qhb2 = QuanHeBang(b ** 2, a ** 2 + c ** 2, id="quan he bang 3")
kl21 = QuanHeBang(B, pi / 2, id="quan he bang 4")
kl22 = QuanHeVuong(a, c, id="quan he vuong 2")
luat2 = Luat([qhb2], [kl21, kl22], id="luat 2")

luat3 = Luat(
    [
        QuanHeBang(c ** 2, a ** 2 + b ** 2, id="quan he bang 5")
    ],
    [
        QuanHeBang(C, pi / 2, id="quan he bang 6"),
        QuanHeVuong(b, a, id="quan he vuong 3")
    ], id="luat 3"
)

luat4 = Luat(
    [
        QuanHeBang(A, pi / 2, id="quan he bang 7")
    ],
    [
        QuanHeBang(a ** 2, b ** 2 + c ** 2, id="quan he bang 8"),
        QuanHeVuong(b, c, id="quan he vuong 4")
    ], id="luat 4"
)

luat5 = Luat(
    [
        QuanHeBang(B, pi / 2, id="quan he bang 9")
    ],
    [
        QuanHeBang(b ** 2, a ** 2 + c ** 2, id="quan he bang 10"),
        QuanHeVuong(a, c, id="quan he vuong 5")
    ], id="luat 5"
)

luat6 = Luat(
    [
        QuanHeBang(C, pi / 2, id="quan he bang 11")
    ],
    [
        QuanHeBang(c ** 2, a ** 2 + b ** 2, id="quan he bang 12"),
        QuanHeVuong(b, a, id="quan he vuong 6")
    ], id="luat 6"
)

luat7 = Luat(
    [
        QuanHeVuong(b, c, id="quan he vuong 7")
    ],
    [
        QuanHeBang(a ** 2, b ** 2 + c ** 2, id="quan he bang 13"),
        QuanHeBang(A, pi / 2, id="quan he bang 14")
    ], id="luat 7"
)

luat8 = Luat(
    [
        QuanHeVuong(a, c, id="quan he vuong 8")
    ],
    [
        QuanHeBang(b ** 2, a ** 2 + c ** 2, id="quan he bang 15"),
        QuanHeBang(B, pi / 2, id="quan he bang 16")
    ], id="luat 8"
)

luat9 = Luat(
    [
        QuanHeVuong(b, a, id="quan he vuong 9")
    ],
    [
        QuanHeBang(c ** 2, a ** 2 + b ** 2, id="quan he bang 17"),
        QuanHeBang(C, pi / 2, id="quan he bang 18")
    ], id="luat 9"
)

luat10 = Luat(
    [
        QuanHeBang(A, B, id="quan he bang 19")
    ],
    [
        QuanHeBang(a, b, id="quan he bang 20")
    ], id="luat 10"
)

luat11 = Luat(
    [
        QuanHeBang(A, C, id="quan he bang 21")
    ],
    [
        QuanHeBang(a, c, id="quan he bang 22")
    ], id="luat 11"
)

luat12 = Luat(
    [
        QuanHeBang(B, C, id="quan he bang 23")
    ],
    [
        QuanHeBang(b, c, id="quan he bang 24")
    ], id="luat 12"
)

luat13 = Luat(
    [
        QuanHeBang(a, b, id="quan he bang 25")
    ],
    [
        QuanHeBang(A, B, id="quan he bang 26")
    ], id="luat 13"
)

luat14 = Luat(
    [
        QuanHeBang(a, c, id="quan he bang 27")
    ],
    [
        QuanHeBang(A, C, id="quan he bang 28")
    ], id="luat 14"
)

luat15 = Luat(
    [
        QuanHeBang(b, c, id="quan he bang 29")
    ],
    [
        QuanHeBang(B, C, id="quan he bang 30")
    ], id="luat 15"
)

luat16 = Luat(
    [
        QuanHeBang(A, B, id="quan he bang 31"),
        QuanHeBang(A, C, id="quan he bang 32")
    ],
    [
        QuanHeBang(A, pi / 3, id="quan he bang 33"),
        QuanHeBang(B, pi / 3, id="quan he bang 34"),
        QuanHeBang(C, pi / 3, id="quan he bang 35")
    ], id="luat 16"
)

luat17 = Luat(
    [
        QuanHeBang(A, B, id="quan he bang 36"),
        QuanHeBang(B, C, id="quan he bang 37")
    ],
    [
        QuanHeBang(A, pi / 3, id="quan he bang 38"),
        QuanHeBang(B, pi / 3, id="quan he bang 39"),
        QuanHeBang(C, pi / 3, id="quan he bang 40")
    ], id="luat 17"
)

luat18 = Luat(
    [
        QuanHeBang(A, C, id="quan he bang 41"),
        QuanHeBang(B, C, id="quan he bang 42")
    ],
    [
        QuanHeBang(A, pi / 3, id="quan he bang 43"),
        QuanHeBang(B, pi / 3, id="quan he bang 44"),
        QuanHeBang(C, pi / 3, id="quan he bang 45")
    ], id="luat 18"
)

TapLuat = set({
    luat1, luat2, luat3, luat4, luat5, luat6, luat7, luat8, luat9, luat10,
    luat11, luat12, luat13, luat14, luat15, luat16, luat17, luat18
})


def KiemTraKetLuan(KetLuan, known):
    kiemtra = known in KetLuan

    return kiemtra


def HamGiaoHaiTapHop(known: FiniteSet, cac_bien_dangThuc: FiniteSet):
    temp = FiniteSet()

    for bien_dt in cac_bien_dangThuc:
        for kn in known:
            if bien_dt == kn:
                temp = temp + FiniteSet(kn)

    return temp


def HieuHaiTapHop(cac_bien_dangThuc, giao):
    temp = FiniteSet()

    for dt in cac_bien_dangThuc:
        if giao._contains(dt):
            continue
        else:
            temp = temp + FiniteSet(dt)
    return temp


def ThuTimDangThucCoThe(known, giathuyet, TapDangThuc, TapThamSo=set()):
    TapDangThucCoThe = []

    giathuyet_temp = giathuyet
    giathuyet_temp_list = []
    for gt in giathuyet_temp:
        giathuyet_temp_list.append(gt.getTuble())

    for dangThuc in TapDangThuc:
        dt1, dt2 = dangThuc.getTuble()

        pt = dt1 - dt2

        pt = pt.subs(giathuyet_temp_list)

        atoms = pt.atoms(Symbol)
        atoms = list(atoms)
        atoms, thamso = UtilsOOC.LocQuaTapThamSo(atoms, TapThamSo)

        if len(atoms) == 1:
            TapDangThucCoThe.append(dangThuc)

    if len(TapDangThucCoThe) > 0:
        return TapDangThucCoThe
    else:
        return False


def ApDungLuat(giathuyet, known, solution, dangThuc, bien):
    dtt, dtp = dangThuc

    eq1 = Eq(dtt, dtp)

    for gt in giathuyet:
        vt1, vp1 = gt.getTuble()
        eq1 = eq1.subs(vt1, vp1)

    kq = solve(eq1, bien)

    if len(kq) > 0:
        tuple_ketqua = (bien, kq[0])
    else:
        raise Exception("Kết quả giải ra hai biến!")

    # update lai tap known
    known = known + FiniteSet(bien)

    solution.append(
        ("Áp dụng đẳng thức: ", dangThuc, "Tính được kết quả là: ", tuple_ketqua,
         "Tập thành phần đã biết mới: ",
         known))

    giathuyet = giathuyet.union(set({DangThuc(bien, kq[0])}))

    return (known, solution, giathuyet)


def ThuTimTapLuatCoThe(known, giaThuyet, TapLuat, TapThamSo=set()):
    tapLuatKhaDi_list = []
    giaThuyet_temp = giaThuyet

    for luat in TapLuat:

        phanIf = luat.getPhanIf()

        bool_PhanIfCoThoaMan = True
        for phanIf_value in phanIf:
            v1 = UtilsOOC.checkQuanHeBangCoNamTrongGiaThuyet(giaThuyet_temp, phanIf_value)
            if v1 == False:
                bool_PhanIfCoThoaMan = False
                break

        if bool_PhanIfCoThoaMan:
            tapLuatKhaDi_list.append(luat)

    if len(tapLuatKhaDi_list) == 0:
        return False
    else:
        return tapLuatKhaDi_list


def SuyDienTien(GT, KL, TapDangThuc=TapDangThuc, TapThamSo=TapThamSo, SoLanChoPhep=100):
    solution = []
    known = set()
    giathuyet = GT

    for gt in GT:
        lhs, rhs = gt.getTuble()
        known = known.union(
            set(
                {
                    lhs
                }
            )
        )

    # print(known)
    index = 1
    while True:
        buoc1 = UtilsOOC.KiemTraKetLuan(known, giathuyet, KetLuan)

        if buoc1:
            return (known, solution, giathuyet)
        else:
            # xử lý trên tập luật
            buoc2_1 = ThuTimTapLuatCoThe(known, giathuyet, TapLuat, TapThamSo)

            if buoc2_1 == False:
                print("Tại lần lập " + index.__str__() + " không thể tìm được tập luật có khả năng!")
            else:
                tapLuatCoKhaNang = buoc2_1

                tapLuatCoKhaNang_phanchia = UtilsOOC.PhanChiaTapLuatCoKhaNang(tapLuatCoKhaNang, known, giathuyet,
                                                                              TapLuat,
                                                                              KetLuan, TapThamSo)

                (luatCoTheApDungNgay, luatCoTheApDungSauDo) = tapLuatCoKhaNang_phanchia

                for luattemp1 in luatCoTheApDungNgay:
                    known, solution, giathuyet = UtilsOOC.ApDungLuat(luattemp1, known, giathuyet, solution, TapLuat,
                                                                     KetLuan, TapThamSo)

                    ktkl = UtilsOOC.KiemTraKetLuan(known, giathuyet, KetLuan)

                    if ktkl:
                        return (known, solution, giathuyet)
                for luattemp2 in luatCoTheApDungSauDo:
                    known, solution, giathuyet = UtilsOOC.ApDungLuat(luattemp2, known, giathuyet, solution, TapLuat,
                                                                     KetLuan, TapThamSo)
                    ktk2 = UtilsOOC.KiemTraKetLuan(known, giathuyet, KetLuan)
                    if ktk2:
                        return (known, solution, giathuyet)

            # xử lý trên tập đẳng thức trong tam giác
            buoc2_2 = ThuTimDangThucCoThe(known, giathuyet, TapDangThuc, TapThamSo)
            if buoc2_2 == False:
                print("Tại lần lập " + index.__str__() + " không thể tìm được tập đẳng thức có khả năng!")
            else:
                TapDangThucCoThe = buoc2_2
                TapDangThucCoThePhanChia = UtilsOOC.PhanChiaTapDangThucCoThe(TapDangThucCoThe, known, giathuyet,
                                                                             TapDangThuc, KetLuan, TapThamSo)

                TapDangThucCoTheApDungNgay, TapDangThucCoTheApDungSauDo = TapDangThucCoThePhanChia

                for dtn in TapDangThucCoTheApDungNgay:
                    known, solution, giathuyet = UtilsOOC.ApDungDangThucTamGiac(dtn, known, giathuyet, solution,
                                                                                TapDangThuc, KetLuan, TapThamSo)
                    ktk3 = UtilsOOC.KiemTraKetLuan(known, giathuyet, KetLuan)
                    if ktk3:
                        return (known, solution, giathuyet)
                for dts in TapDangThucCoTheApDungSauDo:
                    known, solution, giathuyet = UtilsOOC.ApDungDangThucTamGiac(dts, known, giathuyet, solution,
                                                                                TapDangThuc, KetLuan, TapThamSo)
                    ktl4 = UtilsOOC.KiemTraKetLuan(known, giathuyet, KetLuan)
                    if ktl4:
                        return (known, solution, giathuyet)

        # print("Lần lập thứ: " + index.__str__())
        index = index + 1

        if index > SoLanChoPhep:
            return (known, solution, giathuyet)
            break


def inTapDangThucWeb(TapDangThuc):
    temp = ""
    TapDangThucTemp = FiniteSet()
    for dangThuc in TapDangThuc:
        # vetrai, vephai = dangThuc.getTuble()
        tempEq = dangThuc.getDangSymPy()
        TapDangThucTemp = TapDangThucTemp + FiniteSet(tempEq)
    temp = "$$" + latex(TapDangThucTemp) + "$$"
    return temp


def inGiaThuyet(GiaThuyet):
    GiaThuyet_temp = FiniteSet()
    for gt in GiaThuyet:
        # vetrai, vephai = gt
        fs = gt.getPhuongTrinh()
        GiaThuyet_temp = GiaThuyet_temp + FiniteSet(fs)
    temp = "$$" + latex(GiaThuyet_temp) + "$$"
    return temp


def inKetLuan(KetLuan):
    return "$$" + latex(KetLuan) + "$$"


def inBuocGiai(solution):
    temp = ""
    for index, s in solution:
        t1, t2, t3, t4, t5, t6 = s

        stemp = "<p>Bước " + int(index).__str__() + ": </p>"
        stemp += "<p>" + t1

        # t21, t22 = t2

        stemp += "$$" + t2.getDangLatex() + "$$"

        stemp += t3

        # t41, t42 = t4
        stemp += "$$" + t4.getDangLatex() + "$$"

        stemp += t5

        l_temp = []
        if type(t6) is set:
            for v in t6:
                if type(v) is Symbol:
                    l_temp.append(v)
                    # stemp += "$$" + latex(t6) + "$$"
                elif type(v) is QuanHeVuong:
                    l_temp.append(v.getDangSymPy())
                    # stemp += "$$" + latex(v.getDangSymPy()) + "$$"
        stemp += "$$" + latex(l_temp) + "$$"
        stemp += "</p>"

        temp += stemp + "<hr>"
    return temp


def inGiaThuyetMoi(giaThuyet):
    # fstemp = FiniteSet()
    gt_list = []
    for gtnew in giaThuyet:
        if type(gtnew) in (QuanHeBang, DangThuc):
            gt_list.append(gtnew.getDangSymPy())
        elif type(gtnew) is QuanHeVuong:
            gt_list.append(gtnew.getDangSymPy())
        else:
            print(gtnew)
            raise Exception("xem lại")
        # vt, vp = gtnew.getTuble()
        # fstemp += FiniteSet(Eq(vt, vp))
    return "$$" + latex(gt_list) + "$$"


# Khai báo bài toán - giả thuyết

# GiaThuyet = FiniteSet((a, m), (c, 5), (A, pi / 3), (B, pi / 4))
# gt1 = DangThuc(a, m)
# gt2 = DangThuc(b, 1)
# gt3 = DangThuc(A, pi / 2)
# GiaThuyet = set({gt1, gt2, gt3})

gt1 = QuanHeVuong(a, b)
gt2 = DangThuc(c, 5)
gt3 = DangThuc(b, 3)
GiaThuyet = set({gt1, gt2, gt3})

# kết luận
# KetLuan = FiniteSet(b, C, ha, hc)
KetLuan = set({A, ha, hc})

TapDangThuc_latex = inTapDangThucWeb(TapDangThuc)
GiaThuyet_latex = inGiaThuyet(GiaThuyet)
KetLuan_latex = inKetLuan(KetLuan)

# tiến hành thuật giải
known, solution, giaThuyet = SuyDienTien(GiaThuyet, KetLuan)

solution_ = enumerate(solution, start=1)
buocGiai_latex = inBuocGiai(solution_)

giaThuyet_new_latex = inGiaThuyetMoi(giaThuyet)

print("Các thuộc tính của tam giác biết được sau quá trình suy diễn: ")
pprint(known)
print("Giá trị các thuộc tính: ")
pprint(list(map(
    lambda gt: gt.getDangSymPy(), giaThuyet
)))
# pprint(giaThuyet)
print("Các bước suy diễn: ")

solution = enumerate(solution, start=1)
for i, s in solution:
    print("Bước số " + i.__str__() + ": ")
    pprint(s)

print("end of code")
