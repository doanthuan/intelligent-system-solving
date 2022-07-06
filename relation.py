from cobj import Cobj

class Relation:

    @staticmethod
    def make(name: str, left, right):
        rel = Relation(name, left, right)
        if not Relation.exist(rel):
            Cobj.relations.append(rel)
            return rel

    @staticmethod
    def exist(relation) -> bool:
        for rel in Cobj.relations:
            if relation.equal(rel):
                return True
        return False

    def __init__(self, name: str, left, right):
        self.name = name
        self.left = left
        self.right = right
    
        
    def equal(self, relation) -> bool:
        return (
            (self.name == relation.name and self.left.is_ident(relation.left) and self.right.is_ident(relation.right)) or
            (self.name == relation.name and self.left.is_ident(relation.right) and self.right.is_ident(relation.left))
            )

    def __str__(self):
        return f"{self.left} {self.name} {self.right}"