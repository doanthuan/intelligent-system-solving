
def sort_name(name):
    return ''.join(sorted(name))

def remove_duplicates(a_list):
    return list(set(a_list))

def find_common_ele(self, list1, list2):
    common_ele = list(set(list1).intersection(list2))
    return common_ele

def trace_symbol(trace_path, a_symbol, parent_symbol):
    if str(a_symbol) in trace_path:
        old_parent = trace_path[str(a_symbol)]
        if isinstance(old_parent, list):
            old_parent.append(parent_symbol)
        else:
            parents = [old_parent, parent_symbol]
            trace_path[str(a_symbol)] = parents
    else:
        trace_path[str(a_symbol)] = parent_symbol