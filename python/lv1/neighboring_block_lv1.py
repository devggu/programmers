

board = [
    ["blue", "red", "orange", "red"],
    ["red", "red", "blue", "orange"],
    ["blue", "orange", "red", "red"],
    ["orange", "orange", "red", "blue"],
]

h = 1
w = 1
result = 2

from collections import Counter


def solution(board, h, w):
    neighbors = []
    for i in [(h+1,w),(h-1,w),(h,w+1),(h,w-1)]:
        if i[0] < 0 or i[1] < 0 or i[0] > len(board)-1 or i[1] > len(board)-1:
            continue
        neighbors.append(board[i[0]][i[1]])
    neighbors_cnt = Counter(neighbors)
        
    me = board[h][w]

    answer = neighbors_cnt[me]
    return answer

print(solution(board, h, w))