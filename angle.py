class Angle:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def is_none(self):
        return self.value is None

    def has_value(self):
        return self.value is not None