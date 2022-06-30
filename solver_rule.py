
# Rules
# 1. Tiên đề Euclid Nếu 2 góc so le trong mà bằng nhau => 2 đoạn thẳng song song
# A, B = Angle("xAB"), Angle("yBA")
# rule_01 = Rule(
#     [A, B],
#     IfStm([Relation("SO_LE_TRONG", A, B), Eq(A, B)]),
#     [Relation("SONG_SONG", A.line1, B.line1)],
#     "01"
# )

# 2. 3 đoạn thẳng khép kín => tạo thành tam giác
# a, b, c = Line("AB"), Line("BC"), Line("CA")
# rule_01 = Rule(
#     [a, b, c],
#     IfStm([Relation("SO_LE_TRONG", A, B), Eq(A, B)]),
#     [Relation("SONG_SONG", A.line1, B.line1)],
#     "01"
# )


g_relations = []
g_trace_rels = []

# Rule nội tại
# 3 đoạn thẳng khép kín -> tam giác
def rule_01(a: Line, b: Line, c: Line):
    if a.is_connect(b) and b.is_connect(c) and c.is_connect(a):
        Cobj.set_triangle(a,b,c)

def rule_10(A: Angle, B: Angle) -> Relation:
    if relation_exist(Relation("SO_LE_TRONG", A, B)) and equation_true(Eq(A.name, B.name)):
        pass
    
g_rules = [rule_01]

# 2 góc trùng nhau -> = nhau
# def rule_03(a: Angle, b: Angle):
#     if a.is_connect(b) and b.is_connect(c) and c.is_connect(a):
#         tri = Triangle.create(a, b, c)
#         g_triangles[tri.name] = tri

def add_relation(relation: Union[List[Relation], Relation]) -> _void:
    if isinstance(relation, list):
        for rel in relation:
            g_relations.append(relation)
    elif isinstance(relation, Relation):
        g_relations.append(relation)

def relation_exist(relation: Relation) -> bool:
    for rel in g_relations:
        if relation.equal(rel):
            return True

    return False

def equation_true(equation: Eq) -> bool:
    for a_symbol in equation.free_symbols:
        if str(a_symbol) not in g_knowns.keys():
            return False
    return True

import inspect 
def apply_rules():
    for rule_func in g_rules:
        apply_rule(rule_func)

# def apply_rule(rule_func):
#     args = inspect.signature(rule_func)
#     print(args)
        
def apply_rule(rule: Rule):
    if isinstance(rule.args[0], Angle) and isinstance(rule.args[1], Angle):
        g_angles_list = list(g_angles.values())
        for i in range(len(g_angles_list)):
            for j in range(i+1, len(g_angles_list)):
                angle1 = g_angles_list[i]
                angle2 = g_angles_list[j]
                result, trace_rels, trace_paths = check_if_stm(rule.if_stm, angle1, angle2)
                if result is True:
                    #apply then
                    for stm in rule.then_stm:
                        if isinstance(stm, Relation):
                            if isinstance(stm.left, Line) and isinstance(stm.right, Line):
                                new_rel = Relation(stm.name, angle1.line1, angle2.line1)
                                add_relation(new_rel)
                                
                                g_trace_rels.append((new_rel, rule.id, trace_rels, trace_paths))
                    

def print_trace_rels(relation: Relation):
    found = False
    for trace_rel_obj in g_trace_rels:
        new_rel, rule_id, trace_rels, trace_paths = trace_rel_obj
        if relation.equal(new_rel):
            for rel in trace_rels:
                print_trace_rels(rel)
            for a_path in trace_paths:
                print_trace_paths(a_path[0])
                print(f" => {a_path[1]}")

            print(f"Applied rule {rule_id} => {relation}")
            found = True
    
    if not found: # not found in trace, from hypo
        print(f"we have: {relation}")

            
def check_if_stm(if_stm: IfStm, obj1, obj2) -> bool:
    results = [False] * len(if_stm.cond_list)
    trace_rels = []
    trace_paths = []
    for idx, stm in enumerate(if_stm.cond_list):
        if isinstance(stm, Relation):
            rel = Relation(stm.name, obj1, obj2)
            if relation_exist(rel):
                results[idx] = True
                trace_rels.append(rel)
            
        if isinstance(stm, Eq):
            eq = Eq(g_symbols[obj1.name], g_symbols[obj2.name])
            if equation_true(eq):
                results[idx] = True 
                if not is_in_hypo(obj1.name):
                    trace_paths.append((obj1.name, Eq(symbols(obj1.name), symbols(obj2.name))))
                if not is_in_hypo(obj2.name):
                    trace_paths.append((obj2.name, Eq(symbols(obj1.name), symbols(obj2.name))))

    
    if if_stm.operator == "AND":
        result = (False not in results)
    else:
        result = (True in results)
    return result, trace_rels, trace_paths
