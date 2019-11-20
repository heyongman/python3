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

print(total_sets)
print(eval('R1'))