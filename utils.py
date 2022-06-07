
from sympy import solve
from equation import Equation


def sort_name(name):
    return ''.join(sorted(name))

def remove_duplicates(a_list):
    return list(set(a_list))

def find_common_ele(self, list1, list2):
    common_ele = list(set(list1).intersection(list2))
    return common_ele

# def symbol(name):
#     global all_eq, all_symbol
#     return all_symbol[name]

