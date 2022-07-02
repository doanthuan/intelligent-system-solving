from cobj import Cobj

class Relation:

    @staticmethod
    def make(name: str, left, right):
        rel = Relation(name, left, right)
        Cobj.relations.append(rel)
        return rel

    @staticmethod
    def relation_exist(relation) -> bool:
        for rel in Cobj.relations:
            if relation.equal(rel):
                return True
        return False

    def __new__(cls, name: str, left, right):
        obj = object.__new__(cls)
        obj.name = name
        obj.left = left
        obj.right = right
        return obj
    
        
    def equal(self, relation) -> bool:
        return (
            (self.name == relation.name and self.left.ident(relation.left) and self.right.ident(relation.right)) or
            (self.name == relation.name and self.left.ident(relation.right) and self.right.ident(relation.left))
            )

    def __str__(self):
        return f"{self.left} {self.name} {self.right}"