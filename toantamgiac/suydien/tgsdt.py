from sympy import *

# khởi tạo các symbol
a, b, c, A, B, C, ha, hb, hc, S, p, R, r = symbols('a,b,c,A,B,C,ha,hb,hc,S,p,R,r')
m = symbols('m')
init_printing(use_unicode=True)

# khai báo các đẳng thức
dt1 = (A + B + C, pi)
dt2 = (a ** 2, b ** 2 + c ** 2 * 2 * b * c * cos(A))
dt3 = (b ** 2, a ** 2 + c ** 2 * 2 * a * c * cos(B))
dt4 = (c ** 2, a ** 2 + b ** 2 * 2 * a * b * cos(C))

dt5 = (a * sin(B), b * sin(A))
dt6 = (a * sin(C), c * sin(A))
dt7 = (b * sin(C), c * sin(B))

dt8 = (a, 2 * R * sin(A))
dt9 = (b, 2 * R * sin(B))
dt10 = (c, 2 * R * sin(C))

dt11 = (2 * p, a + b + c)
dt12 = (S, a * ha / 2)
dt13 = (S, b * hb / 2)
dt14 = (S, c * hc / 2)

dt15 = (S, p * r)

dt16 = (S, sqrt(p * (p - a) * (p - b) * (p - c)))
dt17 = (S, b * c * sin(A) / 2)
dt18 = (S, b * a * sin(C) / 2)
dt19 = (S, a * c * sin(B) / 2)

dt20 = (ha, b * sin(C))
dt21 = (ha, c * sin(B))
dt22 = (hb, a * sin(C))
dt23 = (hb, c * sin(A))

dt24 = (hc, a * sin(B))
dt25 = (hc, b * sin(A))

TapDangThuc = FiniteSet(dt1, dt2, dt3, dt4, dt5, dt6, dt7, dt8, dt9, dt10, dt11, dt12, dt13, dt14, dt15, dt16, dt17,
                        dt18, dt19, dt20, dt21, dt22, dt23, dt24, dt25)


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


def ThuTimLuat(known: FiniteSet, TapDangThuc: FiniteSet):
    for dangThu in TapDangThuc:
        cac_bien_dangThuc = dangThu.atoms(Symbol)

        giao = HamGiaoHaiTapHop(known, cac_bien_dangThuc)
        numberGiao = len(giao)
        numberBien = len(cac_bien_dangThuc)

        hieuSo = numberBien - numberGiao

        if hieuSo == 1:
            hieuBien = HieuHaiTapHop(cac_bien_dangThuc, giao)

            for b in hieuBien:
                bien = b
                break

            return [True, dangThu, bien]

    return [False]
    # print(cac_bien_dangThuc)


def ApDungLuat(giathuyet, known, solution, dangThuc, bien):
    dtt, dtp = dangThuc

    eq1 = Eq(dtt, dtp)

    for gt in giathuyet:
        vt1, vp1 = gt
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

    giathuyet = giathuyet + FiniteSet(tuple_ketqua)

    return (known, solution, giathuyet)


def SuyDienTien(GT, KL, TapDangThuc=TapDangThuc, SoLanChoPhep=100):
    solution = []
    known = FiniteSet()
    giathuyet = GT

    for gt in GT:
        lhs, rhs = gt
        known = known + FiniteSet(lhs)

    # print(known)
    index = 1
    while True:
        buoc1 = KiemTraKetLuan(KL, known)

        if buoc1:
            return [known, solution]
        else:
            buoc2 = ThuTimLuat(known, TapDangThuc)
            buoc2_ = buoc2[0]

            if buoc2_:
                dangThuc1, dangThuc2 = buoc2[1]
                bien = buoc2[2]
                buoc3 = ApDungLuat(giathuyet, known, solution, (dangThuc1, dangThuc2), bien)

                known, solution, giathuyet = buoc3

        # print("Lần lập thứ: " + index.__str__())
        index = index + 1

        if index > SoLanChoPhep:
            return (known, solution, giathuyet)
            break


def inTapDangThucWeb(TapDangThuc):
    temp = ""
    TapDangThucTemp = FiniteSet()
    for dangThuc in TapDangThuc:
        vetrai, vephai = dangThuc
        tempEq = Eq(vetrai, vephai)
        TapDangThucTemp = TapDangThucTemp + FiniteSet(tempEq)
    temp = "$$" + latex(TapDangThucTemp) + "$$"
    return temp


def inGiaThuyet(GiaThuyet):
    GiaThuyet_temp = FiniteSet()
    for gt in GiaThuyet:
        vetrai, vephai = gt
        fs = FiniteSet(Eq(vetrai, vephai))
        GiaThuyet_temp = GiaThuyet_temp + fs
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

        t21, t22 = t2

        stemp += "$$" + latex(Eq(t21, t22)) + "$$"

        stemp += t3

        t41, t42 = t4
        stemp += "$$" + latex(Eq(t41, t42)) + "$$"

        stemp += t5

        stemp += "$$" + latex(t6) + "$$"
        stemp += "</p>"

        temp += stemp + "<hr>"
    return temp


def inGiaThuyetMoi(giaThuyet):
    fstemp = FiniteSet()
    for gtnew in giaThuyet:
        vt, vp = gtnew
        fstemp += FiniteSet(Eq(vt, vp))
    return "$$" + latex(fstemp) + "$$"


# Khai báo bài toán - giả thuyết
GiaThuyet = FiniteSet((a, m), (c, 5), (A, pi / 3), (B, pi / 4))

# kết luận
KetLuan = FiniteSet(b, C, ha, hc)

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
pprint(giaThuyet)
print("Các bước suy diễn: ")

solution = enumerate(solution, start=1)
for i, s in solution:
    print("Bước số " + i.__str__() + ": ")
    pprint(s)

print("end of code")
