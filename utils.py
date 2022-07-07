

import itertools


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

def next_alpha(s):
    return chr((ord(s.upper())+1 - 65) % 26 + 65).lower()

def get_combinations(list_args, length):
    results = []
    for subset in itertools.combinations(list_args, length):
        results.append(subset)
    return results

def get_permutations(list_args, length):
    results = []
    for subset in itertools.permutations(list_args, length):
        results.append(subset)
    return results
