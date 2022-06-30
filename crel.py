class Crel:

    relations = []

    def __new__(cls, name: str, left, right):
        obj = object.__new__(cls)
        obj.name = name
        obj.left = left
        obj.right = right
        Crel.relations.append(obj)
        return obj
        
    def equal(self, relation) -> bool:
        return (
            (self.name == relation.name and self.left.equal(relation.left) and self.right.equal(relation.right)) or
            (self.name == relation.name and self.left.equal(relation.right) and self.right.equal(relation.left))
            )

    def relation_exist(relation) -> bool:
        for rel in Crel.relations:
            if relation.equal(rel):
                return True
        return False

    def __str__(self):
        return f"{self.left} {self.name} {self.right}"