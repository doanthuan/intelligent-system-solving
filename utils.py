

def sort_name(name):
    return ''.join(sorted(name))

def remove_duplicates(a_list):
    a_list = list(set(a_list))
    return a_list

def find_common_ele(self, list1, list2):
    common_ele = list(set(list1).intersection(list2))
    return common_ele

def flat_list(list):
    results = [ele for sublist in list for ele in sublist]
    return remove_duplicates(results)
