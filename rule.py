class Rule:

    def __init__(self, if_stm, else_stm, id="") -> None:
        self.if_stm = if_stm
        self.else_stm = else_stm
        self.id = id
