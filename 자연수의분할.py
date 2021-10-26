from itertools import combinations_with_replacement as cwr
sum_num = int(input())
sum_count = int(input())
sum_list = []
for i in cwr(range(1,sum_num-1*(sum_count-1)+1),sum_count):
    i = sorted(list(i))
    if sum(i)==sum_num:
        if i not in sum_list:
            sum_list.append(i)
print(sum_list)



