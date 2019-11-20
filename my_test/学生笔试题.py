"""
（1） 有一个集合R = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, ],
（2） 由一组R的真子集构成的集合Rn = [R1, R2, R3, R4, R5],其中
R1 = [ a, c, e, g, i, k, l, m]
R2 = [ b, c, d, h, k]
R3 = [ d, f, g, n]
R4 = [ b, f, g, i, j]
R5 = [ b, k, n]
（3） 给定一个目标集 C = [b, d, f, l, n]， C为R的子集
[问题]求在Rn中找出个数最少的一个子集，这个子集的所有元素的并集为U，
要求U ∩ C = C，且U ∪ C = U，请写出求解这样的一个子集的通用算法。
"""

R = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
R1 = ['a', 'c', 'e', 'g', 'i', 'k', 'l', 'm']
R2 = ['b', 'c', 'd', 'h', 'k']
R3 = ['d', 'f', 'g', 'n']
R4 = ['b', 'f', 'g', 'i', 'j']
R5 = ['b', 'k', 'n']
Rn = [R1, R2, R3, R4, R5]
Rn_keys = ['R1', 'R2', 'R3', 'R4', 'R5']
# Rn_keys = ["04","05","07","11","15","16","22","29","31","34"]

C = {'b', 'd', 'f', 'l', 'n'}

# 构建全部可能子集的总字典
total_sets = {}


def sets_recursive(items):
    # 遍历所有可能子集
    result = [[]]
    for x in items:
        result.extend([subset + [x] for subset in result])
    return result


sets_list = sets_recursive(Rn_keys)
for R_set in sets_list:
    temp_list = []
    for single_set in R_set:
        temp_list += (eval(single_set))
    total_sets.setdefault(tuple(R_set), temp_list)

# 循环匹配满足U ∩ C = C，且U ∪ C = U 要求的子集项
match_sets_keys = []

for key, values in total_sets.items():
    if set(values) & C == C and set(values) | C == set(values):
        match_sets_keys.append(key)

# 排序选择个数最少的字典子集
ordered_1 = sorted(match_sets_keys, key=lambda x: len(x))
ordered_2 = []
minimal_1 = len(min(ordered_1))
for item in ordered_1:
    if len(item) == minimal_1:
        ordered_2.append(item)

# 如果子集个数相同，找个数最少
minimal_2 = len(total_sets[ordered_2[0]])
result = []
for item in ordered_2:
    if minimal_2 > len(total_sets[item]):
        minimal_2 = len(total_sets[item])
    result = [item, total_sets[item]]

print('最小子集包括', result[0])
print('其中元素项有', result[1])
