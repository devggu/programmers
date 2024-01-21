board = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 3],
    [0, 2, 5, 0, 1],
    [0, 2, 4, 4, 2],
    [1, 5, 1, 3, 1],
]
moves = [1,5,3,5,1,2,1,4]

result = 4

import numpy as np

def solution(board, moves):
    board = np.array(board)
    board = board.T.tolist()
    for i in range(len(board)):
        board[i] = list(filter(lambda x: x != 0, board[i]))
    
    stack = [0]
    answer = 0
    
    for i in range(len(moves)):
        if len(board[moves[i] - 1]) == 0:
            continue
        stack.append(board[moves[i]-1].pop(0))
        
        if stack[-1] == stack[-2]:
            stack.pop()
            stack.pop()
            answer += 2
        
    return answer

print(solution(board, moves))