from sympy import *


class DangThuc:
    def __init__(self, veTrai, vePhai, id=""):
        self.ve_trai = veTrai
        self.ve_phai = vePhai
        self.id = id

    def getPhuongTrinh(self):
        return Eq(self.ve_trai, self.ve_phai)

    def getLatex(self):
        return latex(self.getPhuongTrinh())

    def getTuble(self):
        return (self.ve_trai, self.ve_phai)

    def getAtomsVeTrai(self):
        temp = self.ve_trai.atoms(Symbol)
        return temp

    def getAtomsVePhai(self):
        temp = self.ve_phai.atoms(Symbol)
        return temp

    def getAtomsQuanHeBang(self):
        temp = self.getPhuongTrinh().atoms(Symbol)
        return temp

    def getDangSymPy(self):
        return Eq(self.ve_trai, self.ve_phai)

    def getDangLatex(self):
        return latex(self.getDangSymPy())


class QuanHeBang:
    def __init__(self, veTrai, vePhai, id="") -> None:
        super().__init__()
        self.ve_trai = veTrai
        self.ve_phai = vePhai
        self.id = id

    def getVeTrai(self):
        return self.ve_trai

    def getVePhai(self):
        return self.ve_phai

    def getDangThuc(self):
        return Eq(self.ve_trai, self.ve_phai)

    def getTuble(self):
        return (self.ve_trai, self.ve_phai)

    def getAtomsVeTrai(self):
        return self.ve_trai.atoms(Symbol)

    def getAtomsVePhai(self):
        return self.ve_phai.atoms(Symbol)

    def getAtomsQuanHeBang(self):
        return self.getDangThuc().atoms(Symbol)

    def getDangSymPy(self):
        return Eq(self.ve_trai, self.ve_phai)

    def getDangLatex(self):
        return latex(self.getDangSymPy())


class QuanHeVuong:

    def __init__(self, veTrai, vePhai, id="") -> None:
        super().__init__()
        self.ve_trai = veTrai
        self.ve_phai = vePhai
        self.id = id

    def getAtomsVeTrai(self):
        return self.ve_trai.atoms(Symbol)

    def getAtomsVePhai(self):
        return self.ve_phai.atoms(Symbol)

    def getTuble(self):
        return (self.ve_trai, self.ve_phai)

    def getAtomsQuanHeVuong(self):
        return self.getAtomsVeTrai().union(self.getAtomsVePhai())

    def getTuongDuong(self, qhvKhac):
        t, p = qhvKhac.getTuble()

        if (self.ve_trai == t and self.ve_phai == p) or (self.ve_trai == p and self.ve_phai == t):
            return True
        else:
            return False

    def getDangSymPy(self):
        vuong = symbols("vuông_gốc_với")
        return (self.ve_trai, vuong, self.ve_phai)

    def getDangLatex(self):
        return latex(self.getDangSymPy())

    def getPhuongTrinh(self):
        return self.getDangSymPy()


class Luat:

    def __init__(self, phatBieu, heQua, id="", markUsed=False) -> None:
        super().__init__()
        typeOfPhatBieu = type(phatBieu)
        if typeOfPhatBieu == list:
            self.phat_bieu = phatBieu
        else:
            print(phatBieu)
            raise Exception("phát biểu phải ở dạng list")
        typeOfHeQua = type(heQua)
        if typeOfHeQua == list:
            self.he_qua = heQua
        else:
            print(heQua)
            raise Exception("hệ quả phải ở dạng list")
        self.id = id
        self.MarkUsed = markUsed

    def getPhanIf(self):
        return self.phat_bieu

    def getPhanThen(self):
        return self.he_qua

    def getTuble(self):
        return (self.phat_bieu, self.he_qua)

    def getID(self):
        return self.id

    def getMarkUsed(self):
        return self.MarkUsed

    def setMarkUsed(self, value):
        self.MarkUsed = value

    def getDangSymPy(self):
        neu, thi = symbols("Nếu,Thì")

        phatbieu = []
        hequa = []

        for pb in self.phat_bieu:
            if type(pb) in (DangThuc, QuanHeBang):
                phatbieu.append(pb.getDangSymPy())
            elif type(pb) is QuanHeVuong:
                phatbieu.append(pb.getDangSymPy())
            else:
                print(pb)
                raise Exception("Xem lại biểu thức trên")

        for hq in self.he_qua:
            if type(hq) in (DangThuc, QuanHeBang):
                hequa.append(hq.getDangSymPy())
            elif type(hq) is QuanHeVuong:
                hequa.append(hq.getDangSymPy())
            else:
                print(hq)
                raise Exception("Xem lại biểu thức trên")

        return [neu, phatbieu, thi, hequa]

    def getDangLatex(self):
        return latex(self.getDangSymPy())


class ThamSo:

    def __init__(self, listDanhSachThamSo) -> None:
        super().__init__()
        if type(listDanhSachThamSo) in (list, set):
            self.danhSachThamSo = listDanhSachThamSo
        else:
            print(listDanhSachThamSo)
            raise Exception("Xem lại danh sách tham số")

    def checkSymBolCoPhaiThamSo(self, symb):
        if type(symb) is Symbol:
            if symb in self.danhSachThamSo:
                return True
            else:
                return False
        else:
            print(symb)
            raise Exception("lỗi")


class UtilsOOC:

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def checkQuanHeBangCoNamTrongGiaThuyet(giaThuyet, quanHe, TapThamSo=set()):
        giaThuyet_list_quanHeBang = []
        giaThuyet_list_quanHeVuong = []
        for giaThuyet_v in giaThuyet:
            if type(giaThuyet_v) in (DangThuc, QuanHeBang):
                giaThuyet_list_quanHeBang.append(giaThuyet_v.getTuble())
            elif type(giaThuyet_v) is QuanHeVuong:
                giaThuyet_list_quanHeVuong.append(giaThuyet_v)

        if type(quanHe) in (DangThuc, QuanHeBang):
            qhvt, qhvp = quanHe.getTuble()

            pt = qhvt - qhvp

            pt = pt.subs(giaThuyet_list_quanHeBang)

            spt = simplify(pt)

            if spt == 0:
                return True
            else:
                return False
        elif type(quanHe) is QuanHeVuong:
            qhv1, qhv2 = quanHe.getTuble()

            for value1 in giaThuyet_list_quanHeVuong:
                at1 = value1.getAtomsQuanHeVuong()

                if qhv1 in at1 and qhv2 in at1:
                    return True

            return False
        else:
            print(quanHe)
            raise Exception("xem lại quan hệ trên")

    @staticmethod
    def thuTimGiaTriMoiOPhanThen(giaThuyet, quanHe):
        list_giaThuyet = []
        for giaThuyet_v in giaThuyet:
            list_giaThuyet.append(giaThuyet_v.getTuble())

        quanHevt, quanHevp = quanHe.getTuble()
        pt = quanHevt - quanHevp

        pt = pt.subs(list_giaThuyet)

        ptAtoms = pt.atoms(Symbol)

        if len(ptAtoms) == 1:
            ptAtom = list(ptAtoms)[0]

            kq = solve(Eq(pt, 0), ptAtom)

            if len(kq) > 0:
                print(kq)
                for kqv in kq:
                    if kqv > 0:
                        return QuanHeBang(ptAtom, kqv)
        else:
            return False

    @staticmethod
    def PhanChiaTapLuatCoKhaNang(tapLuatCoKhaNang, known, giathuyet, TapLuat, KetLuan, TapThamSo=set()):
        KetLuan_temp = KetLuan
        giathuyet_temp = giathuyet
        giathuyet_temp_qhb_list = []
        giathuyet_temp_qhv_list = []

        for gt in giathuyet_temp:
            if type(gt) in (QuanHeBang, DangThuc):
                giathuyet_temp_qhb_list.append(gt.getTuble())
            elif type(gt) is QuanHeVuong:
                giathuyet_temp_qhv_list.append(gt)

        tapLuatCoKhaNang_coTheApDungNgay = []
        tapLuatCoKhaNang_coTheApDungSauDo = []

        for luat in tapLuatCoKhaNang:
            luatp1, luatp2 = luat.getTuble()
            for quanhe in luatp2:
                if type(quanhe) in (QuanHeBang, DangThuc):
                    qh1, qh2 = quanhe.getTuble()
                    pt = qh1 - qh2
                    pt = pt.subs(giathuyet_temp_qhb_list)

                    pt = sympify(pt)
                    atoms = pt.atoms(Symbol)
                    atoms = list(atoms)

                    atoms, thamso = UtilsOOC.LocQuaTapThamSo(atoms, TapThamSo)

                    if len(atoms) == 1:
                        atom = atoms[0]
                        if atom in KetLuan_temp:
                            tapLuatCoKhaNang_coTheApDungNgay.append(luat)
                            break
                    else:
                        continue
                elif type(quanhe) is QuanHeVuong:
                    qh1, qh2 = quanhe.getTuble()

                    trigger = False
                    for kl in KetLuan_temp:
                        if type(kl) is QuanHeVuong:
                            kl1, kl2 = kl.getTuble()

                            if (qh1 == kl1 and qh2 == kl2) or (qh1 == kl2 and qh2 == kl1):
                                trigger = True
                                tapLuatCoKhaNang_coTheApDungNgay.append(luat)

                                break
                            else:
                                continue
                        else:
                            continue
                    if trigger:
                        break
                else:
                    print(quanhe)
                    raise Exception("xem lại quan hệ trên")

        for luat1 in tapLuatCoKhaNang:
            cothe = True
            for luattemp in tapLuatCoKhaNang_coTheApDungNgay:
                if luat.getID() == luattemp.getID():
                    cothe = False
                    break
            if cothe:
                tapLuatCoKhaNang_coTheApDungSauDo.append(luat1)

        return (tapLuatCoKhaNang_coTheApDungNgay, tapLuatCoKhaNang_coTheApDungSauDo)

    @staticmethod
    def ApDungLuat(luattemp1, known, giathuyet, solution, TapLuat, KetLuan, TapThamSo=set()):
        vuong = symbols("vuông")

        known_temp = known
        giathuyet_temp = giathuyet
        solution_temp = solution
        TapLuat_temp = TapLuat

        giathuyet_temp_qhb_list = []
        giathuyet_temp_qhv_list = []

        for gt in giathuyet_temp:
            if type(gt) in (QuanHeBang, DangThuc):
                giathuyet_temp_qhb_list.append(gt.getTuble())
            elif type(gt) is QuanHeVuong:
                giathuyet_temp_qhv_list.append(gt)

        l1, l2 = luattemp1.getTuble()

        for md in l2:
            if type(md) in (QuanHeBang, DangThuc):
                md1, md2 = md.getTuble()

                pt = md1 - md2

                pt = pt.subs(giathuyet_temp_qhb_list)

                atoms = pt.atoms(Symbol)

                atoms = list(atoms)
                atoms, thamso = UtilsOOC.LocQuaTapThamSo(atoms, TapThamSo)

                if len(atoms) == 1:
                    atom = atoms[0]

                    kq = solve(pt, atom)

                    if len(kq) > 0:
                        kq = list(kq)

                        for kqtem in kq:
                            if len(thamso) == 0:
                                if kqtem > 0:
                                    known_temp = known_temp.union(
                                        set(
                                            {
                                                atom
                                            }
                                        )
                                    )
                                    giathuyet_temp = giathuyet_temp.union(set(
                                        {DangThuc(atom, kqtem)}
                                    ))
                                    solution_temp.append(
                                        (
                                            "Áp dụng luật: ", luattemp1,
                                            "Tính được kết quả: ", DangThuc(atom, kqtem),
                                            "Tập thành phần đã biết mới", known_temp
                                        )
                                    )
                                    break
                                else:
                                    continue
                            else:
                                checkKq = UtilsOOC.checkKetQuaCoThamSo(atom, kqtem, TapThamSo)

                                if checkKq:
                                    known_temp = known_temp.union(
                                        set(
                                            {
                                                atom
                                            }
                                        )
                                    )
                                    giathuyet_temp = giathuyet_temp.union(set(
                                        {DangThuc(atom, kqtem)}
                                    ))
                                    solution_temp.append(
                                        (
                                            "Áp dụng luật: ", luattemp1,
                                            "Tính được kết quả: ", DangThuc(atom, kqtem),
                                            "Tập thành phần đã biết mới", known_temp
                                        )
                                    )

                else:
                    continue
                    # print(pt)
                    # raise Exception("pt không thể giải được")
            elif type(md) is QuanHeVuong:
                trigger = True

                for lv in giathuyet_temp_qhv_list:
                    td = md.getTuongDuong(lv)
                    if td == True:
                        trigger = False
                        break
                if trigger:
                    giathuyet_temp = giathuyet_temp.union(
                        set(
                            {
                                md
                            }
                        )
                    )
                    md1, md2 = md.getTuble()
                    known_temp = known_temp.union(
                        set(
                            {
                                md
                            }
                        )
                    )

                    solution_temp.append(
                        (
                            "Áp dụng luật: ", luattemp1,
                            "Tính được kết quả: ", md,
                            "Tập thành phần đã biết mới", known_temp
                        )
                    )
            else:
                print(md)
                raise Exception("xem lại mệnh đề áp dụng")

        return (known_temp, solution_temp, giathuyet_temp)

    @staticmethod
    def KiemTraKetLuan(known, giathuyet, KetLuan):
        known_temp = known
        KetLuan_temp = KetLuan

        trigger = True

        for kl1 in KetLuan_temp:
            if type(kl1) in (DangThuc, QuanHeBang, Symbol):
                if kl1 in known_temp:
                    continue
                else:
                    trigger = False
                    break
            elif type(kl1) is QuanHeVuong:
                timthay = False
                for k in known_temp:
                    if type(k) is QuanHeVuong:
                        t1 = kl1.getTuongDuong(k)
                        if t1 == True:
                            timthay = True
                            break
                if timthay == False:
                    break
            else:
                print(kl1)
                raise Exception("xem lại quan hệ trên")

        if trigger:
            return True
        else:
            return False

    @staticmethod
    def PhanChiaTapDangThucCoThe(TapDangThucCoThe, known, giathuyet, TapDangThuc, KetLuan, TapThamSo=set()):
        TapDangThucCoThe_temp = TapDangThucCoThe
        TapDangThucCoTheApDungNgay = []
        TapDangThucCoTheApDungSauDo = []
        giathuyet_temp = giathuyet
        giathuyet_temp_list = []
        for gt in giathuyet_temp:
            giathuyet_temp_list.append(gt.getTuble())

        for dt in TapDangThucCoThe_temp:
            dt1, dt2 = dt.getTuble()

            pt = dt1 - dt2
            pt = pt.subs(giathuyet_temp_list)

            atoms = pt.atoms(Symbol)
            atoms = list(atoms)
            atoms, thamso = UtilsOOC.LocQuaTapThamSo(atoms, TapThamSo)

            if len(atoms) == 1:
                atom = atoms[0]

                if atom in KetLuan:
                    TapDangThucCoTheApDungNgay.append(dt)
                else:
                    TapDangThucCoTheApDungSauDo.append(dt)

        return (TapDangThucCoTheApDungNgay, TapDangThucCoTheApDungSauDo)

    @staticmethod
    def ApDungDangThucTamGiac(dangThuc, known, giathuyet, solution, TapDangThuc, KetLuan, TapThamSo=set()):
        known_temp = known
        giathuyet_temp = giathuyet
        giathuyet_temp_list = []
        for gt in giathuyet_temp:
            giathuyet_temp_list.append(gt.getTuble())

        dt1, dt2 = dangThuc.getTuble()

        pt = dt1 - dt2
        pt = pt.subs(giathuyet_temp_list)

        atoms = pt.atoms(Symbol)
        atoms = list(atoms)
        atoms, thamso = UtilsOOC.LocQuaTapThamSo(atoms, TapThamSo)

        if len(atoms) == 1:
            bien = atoms[0]

            kq = solve(pt, bien)
            kq = list(kq)

            for v in kq:
                if len(thamso) == 0:
                    if v > 0:
                        known_temp = known_temp.union(
                            set(
                                {
                                    bien
                                }
                            )
                        )
                        giathuyet_temp = giathuyet_temp.union(
                            set(
                                {
                                    QuanHeBang(bien, v)
                                }
                            )
                        )
                        solution.append(
                            (
                                "Áp dụng đẳng thức: ", dangThuc,
                                "Tính được kết quả: ", QuanHeBang(bien, v),
                                "Tập thành phần đã biết mới", known_temp
                            )
                        )
                        break
                    else:
                        continue
                else:
                    checkKq = UtilsOOC.checkKetQuaCoThamSo(bien, v, TapThamSo)

                    if checkKq:
                        known_temp = known_temp.union(
                            set(
                                {
                                    bien
                                }
                            )
                        )
                        giathuyet_temp = giathuyet_temp.union(
                            set(
                                {
                                    QuanHeBang(bien, v)
                                }
                            )
                        )
                        solution.append(
                            (
                                "Áp dụng đẳng thức: ", dangThuc,
                                "Tính được kết quả: ", QuanHeBang(bien, v),
                                "Tập thành phần đã biết mới", known_temp
                            )
                        )

        return (known_temp, solution, giathuyet_temp)

    @staticmethod
    def LocQuaTapThamSo(atoms, TapThamSo):
        atoms_temp = set(atoms)
        TapThamSo_temp = set(TapThamSo)
        temp = atoms_temp.difference(TapThamSo_temp)
        temp1 = atoms_temp.intersection(TapThamSo_temp)
        return list(temp), list(temp1)

    @staticmethod
    def checkKetQuaCoThamSo(bienCanGiai, kqtem, TapThamSo):
        TapSoThu = [0.5]
        trigger = True

        for value in TapSoThu:
            kq = solve(Eq(kqtem, value))

            if len(kq) > 0:
                continue
            else:
                trigger = False
                break

        if trigger:
            return True
        else:
            return False
