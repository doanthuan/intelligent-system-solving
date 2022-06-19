class IfStm:
    def __init__(self, cond_list: list, operator = "AND") -> None:
        self.cond_list = cond_list
        self.operator = operator

class Rule:
    def __init__(self, args: list, if_stm: IfStm, then_stm: list, id="") -> None:
        self.args = args
        self.if_stm = if_stm
        self.then_stm = then_stm
        self.id = id