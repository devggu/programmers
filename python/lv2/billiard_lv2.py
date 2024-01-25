def shortest_path(start, end, m, n):
    candidates = []
    start_x = start[0]
    start_y = start[1]
    end_x = end[0]
    end_y = end[1]
    
    if not (start_y == end_y and start_x > end_x):
        candidates.append((start_x + end_x) ** 2 + (start_y - end_y) ** 2)
    if not (start_y == end_y and start_x < end_x):
        candidates.append((m - start_x + m - end_x) ** 2 + (start_y - end_y) ** 2)
    if not (start_x == end_x and start_y > end_y):
        candidates.append((start_x - end_x) ** 2 + (start_y + end_y) ** 2)
    if not (start_x == end_x and start_y < end_y):
        candidates.append((start_x - end_x) ** 2 + (n - start_y + n - end_y) ** 2)

    print((candidates))
    return min(candidates)


def solution(m, n, startX, startY, balls):
    answer = []
    for ball in balls:
        answer.append(shortest_path((startX, startY), ball, m, n))
        
    print(answer)
    return answer


if __name__ == "__main__":
    m = 10
    n = 10
    startX = 3
    startY = 7
    balls = [[7, 7], [2, 7], [7, 3]]
    # result = [52, 37, 116]

    solution(m, n, startX, startY, balls)
