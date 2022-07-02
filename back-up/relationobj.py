class RelationObj:
    def __init__(self, name: str, left, right):
        self.name = name
        self.left = left
        self.right = right
        
    def equal(self, relation) -> bool:
        return (
            (self.name == relation.name and self.left.equal(relation.left) and self.right.equal(relation.right)) or
            (self.name == relation.name and self.left.equal(relation.right) and self.right.equal(relation.left))
            )

    def __str__(self):
        return f"{self.left} {self.name} {self.right}"