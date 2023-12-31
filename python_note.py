a = [3, 2, 7, 2, 4, 6, 5, 1, 3, 2, 7, 2]

_sum = 15

combinations = []

for i in range(len(a)):
    for j in range(i + 1, len(a)):
        if sum(a[i:j]) == _sum:
            combinations.append(a[i:j])
        elif (a[i:j]) > _sum:
                break