def solution(queue1, queue2):
    q = queue1 + queue2
    target = sum(q) // 2

    i, j = 0, len(queue1)-1
    curr = sum(queue1)
    count = 0

    while i < len(q) and j < len(q):        
        if curr == target:
            return count

        elif curr < target and j < len(q)-1:
            j += 1
            curr += q[j]

        else:
            curr -= q[i]
            i += 1

        count += 1

    return -1

def solution2(queue1, queue2):
    goal = (sum(queue1+queue2)) // 2

    i, j = 0, 0
    current_sum = sum(queue1)
    cnt = 0

    while i < len(queue1) and j < len(queue2):        
        if current_sum == goal:
            return cnt

        elif current_sum < goal and j < len(queue2)-1:
            j += 1
            current_sum += queue2[j]

        else:
            current_sum -= queue1[i]
            i += 1

        cnt += 1

    return -1


if __name__ == '__main__':
    queue1 = [3, 2, 7, 2]  # 14
    queue2 = [4, 6, 5, 1]  # 16
    print(solution2(queue1, queue2))
