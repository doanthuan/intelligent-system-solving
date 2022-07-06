# from line import Line


# line1 = Line("AB")
# line2 = Line("BC")
# line2.add_point("A")

# result = line1.is_belong(line2)
# print(result)

def next_alpha(s):
    return chr((ord(s.upper())+1 - 65) % 26 + 65).lower()

for s in 'abcdefghijklmnopqrstuvwxyz':
    print('%s --> %s' % (s, next_alpha(s)))