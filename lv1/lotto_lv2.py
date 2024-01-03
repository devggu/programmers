lottos = [44, 1, 0, 0, 31, 25]
win_nums = [31, 10, 45, 1, 6, 19]
result = [3, 5]

WIN_DICT = {0: 6, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}


def solution(lottos, win_nums):
    zeros = lottos.count(0)
    match_cnt = 0
    for i in lottos:
        if i in win_nums:
            match_cnt += 1
    answer = [WIN_DICT[match_cnt + zeros], WIN_DICT[match_cnt]]
    return answer


print(solution(lottos, win_nums))
