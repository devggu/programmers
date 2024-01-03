n = 5
arr1 = [9, 20, 28, 18, 11]
arr2 = [30, 1, 21, 17, 28]
result = ["#####", "# # #", "### #", "# ##", "#####"]

def solution(n, arr1, arr2):
    map =  [
            bin(i | j)[2:].zfill(n).replace("1", "#").replace("0", " ")
            for i, j in zip(arr1, arr2)
        ]
    answer = map
    return answer


print(solution(n, arr1, arr2))
print(bin(9)[2:])
print(bin(30)[2:])
print(bin(9 | 30)[2:])