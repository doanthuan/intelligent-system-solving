class Line:
    def __init__(self, name: str, value = None):
        self.name = name
        self.from_v = name[0]
        self.to_v = name[1]
        self.value = value

    def equal(self, line) -> bool:
        if (self.from_v == line.from_v and self.to_v == line.to_v) or (self.from_v == line.to_v and self.to_v == line.from_v):
            return True
        return False

    def __str__(self):
        return f"{self.name}"