from copy import copy
import enum
import inspect
from re import sub
from cobj import Cobj

from line import Line

a1 = Line("AB")
b1 = Line("BC")
c1 = Line("CA")

import itertools
def get_combinations(list_args):
    results = []
    for subset in itertools.combinations(list_args[0], len(list_args)):
        results.append(subset)
    return results

def rule_01(a: Line, b: Line, c: Line):
    if a.is_connect(b) and b.is_connect(c) and c.is_connect(a):
        a = 1

g_rules = [rule_01]

def apply_rules():
    for rule_func in g_rules:
        apply_rule(rule_func)

def apply_rule(rule_func):
    func_args = get_func_args(rule_func)
    list_args = get_combinations(func_args)
    for args in list_args:
        rule_func(*args)

def get_func_args(rule_func):
    func_args = []
    specs = inspect.getfullargspec(rule_func)
    for arg in list(specs.annotations.values()):
        print(arg)
        if 'Line' in str(arg):
            func_args.append(list(Cobj.lines.values()))
    return func_args

apply_rules()

def get_combine(args):
    list_args = []
    for arg in args:
        if str(arg) == 'Line':
            list_args.append(Cobj.lines)
    
    combines = []
    if len(list_args) == 2:
        args1 = list_args[0]
        args2 = list_args[1]
        for arg_i in args1:
            for arg_j in args2:
                combines.append(arg_i, arg_j)

def get_combines(list_args, index = 0):
    results = []
    args = list_args[index]
    for arg in args:
        if index < len(list_args) - 1:
            combines = get_combines(list_args, index + 1)
            for a_combine in combines:
                if arg not in a_combine:
                    a_combine.insert(0, arg)
                    results.append(a_combine)
        else:
            results.append([arg])

    #remove duplicates
    if index == 0:
        rm_index = []
        for i in range(len(results)):
            if i < len(results):
                i_combine = results[i]
                for j in range(i + 1, len(results)):
                    if j < len(results):
                        j_combine = results[j]
                        if compare_lists(i_combine, j_combine) == 0:
                            #rm_index.append(j)
                            results.pop(j)

        return results
    return results

from collections import Counter

def compare_lists(list1, list2): 
    return Counter(list1) == Counter(list2)

func_args = [
    ['1', '2', '3'],
    ['1', '2', '3'],
    ['1', '2', '3'],
]
results = get_combines(func_args)
print(results)


