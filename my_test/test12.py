from itertools import combinations

list1 = list(combinations(["04", "05", "07", "11", "15", "16", "22", "29", "31", "34"], 5))
list2 = list(combinations(['03', '04', '08', '12'], 2))
list3 = list(combinations([list1, list2], 2))
list4 = [[]]

# print(list4)
# print(list1)
print(list2)
print(list1[0]+list2[1])
# print(list3)
tp = [()]
for l1 in list1:
    for l2 in list2:
        tp.append(l1+l2)
print(len(tp))
sorted(tp)
