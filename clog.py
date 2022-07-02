from sympy import Eq
from cobj import Cobj
from relation import Relation


class Clog:

    trace_paths = {}
    trace_rels = []
    logs = []

    def print_trace_paths(cur_symb):

        if cur_symb not in Clog.trace_paths.keys():
            return

        eq = Clog.trace_paths[cur_symb]
        if isinstance(eq, Eq):
            for a_symbol in eq.free_symbols:
                    if str(a_symbol) != cur_symb and str(a_symbol) not in Cobj.hypo.keys():
                        Clog.print_trace_paths(str(a_symbol))
            Clog.log(f"{eq} => {cur_symb} =  {Cobj.knowns[str(cur_symb)]}")

        elif isinstance(eq, list):
            Clog.log("From multiple equations:")
            for a_eq in eq:
                Clog.log(f"{a_eq}")
            Clog.log(f" => {cur_symb} =  {Cobj.knowns[str(cur_symb)]}")

        Clog.prints()
    
    def print_solution(target):
        print("\n---TARGET---")
        print(f"{str(target)}:{Cobj.knowns[str(target)]}")
        print("---HYPO:---")
        
        for key, value in Cobj.hypo.items():
            print(f"{key}:{value}")
        print("---SOLUTION---")
        Clog.print_trace_paths(str(target))

    def log(*texts):
        Clog.logs.append(texts)

    def log_inline(*texts):
        new_texts = texts
        if len(Clog.logs) > 0:
            texts = Clog.logs.pop()
            new_texts = texts + new_texts
        Clog.logs.append(new_texts)
    
    def prints():
        while len(Clog.logs) > 0:
            texts = Clog.logs.pop(0)
            print(*texts)
    
    def print_logs(logs):
        while len(logs) > 0:
            texts = logs.pop(0)
            print(texts)

    
    def print_trace_rels(relation):
        found = False
        for trace_rel_obj in Clog.trace_rels:
            new_rel, rule_id, inputs = trace_rel_obj
            if relation.equal(new_rel):
                for idx, input in enumerate(inputs):
                    if isinstance(input, Eq):
                        symbs = Cobj.not_in_hypo(input.free_symbols)
                        for a_symb in symbs:
                            Clog.print_trace_paths(a_symb)
                        Clog.log(f"=> {input} ({idx+1})")
                    elif isinstance(input, Relation):
                        Clog.print_trace_rels(input)
                        Clog.log_inline(f" ({idx+1})")
                    else:
                        Clog.log(f"{input} ({idx+1})")
                froms = ["("+str(i+1)+")" for i in range(len(inputs))]
                Clog.log("From:",' '.join(froms))
                Clog.log_inline(f" ({rule_id})=> {relation}")
                found = True
        
        if not found: # not found in trace, from hypo
            Clog.log(f"HYPO: {relation}")
        Clog.prints()