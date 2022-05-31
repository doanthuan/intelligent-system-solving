class Vertex:
    def __init__(self, name, angle = None):
        self.name = name
        self.angle = angle

    def is_none(self):
        return self.angle is None

    def has_value(self):
        return self.angle is not None