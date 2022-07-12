from cobj import Cobj
from sympy import Eq

class Ceq:
    
    def __new__(cls, lhs, rhs, save=True):
        eq = Eq(lhs, rhs)
        Ceq.set_eq(eq)
        return eq

    def eq(lhs, rhs):
        eq = Eq(lhs, rhs)
        Ceq.set_eq(eq)
        return eq

    def ieq(expr):
        if not Ceq.ieq_exist(expr):
            Cobj.ieqs.append(expr)
            return expr

    def set_eq(eq: Eq):
        if eq == True or eq == False:
            return
        if not Ceq.eq_exist(eq):
            Cobj.eqs.append(eq)

    def eq_exist(eq: Eq):
        if eq == True:
            return True
        for a_eq in Cobj.eqs:
            if (a_eq.lhs == eq.lhs and a_eq.rhs == eq.rhs) or (a_eq.lhs == eq.rhs and a_eq.rhs == eq.lhs):
                return True
        return False

    def ieq_exist(expr):
        for ieq in Cobj.ieqs:
            if ieq == True or ieq == False:
                continue
            if ieq.equals(expr):
                return True
        return False

    def get_ieq_by_symb(a_symbol):
        ieqs = []
        for ieq in Cobj.ieqs:
            if a_symbol in ieq.free_symbols:
                ieqs.append(ieq)
        return ieqs 

    def check_ieq(expr):
        if Ceq.ieq_exist(expr):
            return True
            
        new_ieqs = Cobj.sub_ieq_with_knowns(Cobj.ieqs)
        for new_ieq in new_ieqs:
            if new_ieq.equals(expr):
                return True
        return False


