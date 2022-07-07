from sympy import Eq, Unequality
from cobj import Cobj
from relation import Relation
from sympy.core.relational import Relational

class Log:

    trace_paths = {}
    trace_rules = []
    logs = []

    def print_trace_paths(cur_symb):

        if cur_symb not in Log.trace_paths.keys():
            return

        eq = Log.trace_paths[cur_symb]
        if isinstance(eq, Eq):
            for a_symbol in eq.free_symbols:
                    if str(a_symbol) != cur_symb and str(a_symbol) not in Cobj.hypo.keys():
                        Log.print_trace_paths(str(a_symbol))
            Log.log(f"{eq} => {cur_symb} =  {Cobj.knowns[str(cur_symb)]}")

        elif isinstance(eq, list):
            Log.log("From multiple equations:")
            for a_eq in eq:
                Log.log(f"{a_eq}")
            Log.log(f" => {cur_symb} =  {Cobj.knowns[str(cur_symb)]}")

        Log.prints()
    
    def print_solution(target):
        print("\n---TARGET---")
        print(f"{str(target)}:{Cobj.knowns[str(target)]}")
        print("---HYPO:---")
        
        for key, value in Cobj.hypo.items():
            print(f"{key}:{value}")
        print("---SOLUTION---")
        Log.print_trace_paths(str(target))

    

    def log(*texts):
        Log.logs.append(texts)

    def log_inline(*texts):
        new_texts = texts
        if len(Log.logs) > 0:
            texts = Log.logs.pop()
            new_texts = texts + new_texts
        Log.logs.append(new_texts)
    
    def prints():
        while len(Log.logs) > 0:
            texts = Log.logs.pop(0)
            print(*texts)
    
    def print_logs(logs):
        while len(logs) > 0:
            texts = logs.pop(0)
            print(texts)

    def trace_rule(object, rule_id, inputs):
        Log.trace_rules.append((object, rule_id, inputs))

    def get_trace_obj(target):
        for trace_obj in Log.trace_rules:
            new_obj, rule_id, inputs = trace_obj
            if (
                (isinstance(target, Relation) and isinstance(new_obj, Relation) and target.equal(new_obj)) or
                (issubclass(type(target), Relational) and issubclass(type(new_obj), Relational) and target.equals(new_obj))
            ):
                return trace_obj
    
    def print_trace_rules(target):
        trace_obj = Log.get_trace_obj(target)
        if trace_obj is not None:
            new_obj, rule_id, inputs = trace_obj
            for idx, input in enumerate(inputs):
                if isinstance(input, Eq):
                    symbs = Cobj.not_in_hypo(input.free_symbols)
                    for a_symb in symbs:
                        Log.print_trace_paths(a_symb)
                    Log.log(f"=> {input} ({idx+1})")
                elif isinstance(input, Relation) or issubclass(type(input), Relational):
                    Log.print_trace_rules(input)
                    #Log.log_inline(f"({idx+1})")
                else:
                    Log.log(f"{input} ({idx+1})")
            froms = ["("+str(i+1)+")" for i in range(len(inputs))]
            Log.log("From:",' '.join(froms))
            Log.log_inline(f" ({rule_id})=> {target}")

        Log.prints()