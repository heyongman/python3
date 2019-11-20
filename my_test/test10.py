Rn_keys = ["04","05","07","11","15","16","22","29","31","34"]
Rn_keys1 = ['03', '04', '08', '12']


# 构建全部可能子集的总字典
total_sets = {}


def sets_recursive(items):
    # 遍历所有可能子集
    result = [[]]
    for x in items:
        result.extend([subset + [x] for subset in result])
    return result


sets_list = sets_recursive(Rn_keys)
for l in sets_list:
    if len(l) == 5:
        print(l)

list1 = sets_recursive(Rn_keys1)
for l in list1:
    if len(l) == 2:
        print(l)
