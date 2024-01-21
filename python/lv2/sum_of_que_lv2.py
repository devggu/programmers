from gettext import find
import itertools

# 3 2 7 2 4 6 5 1 3 2 7 2

# 4 6 5 1 3 2 7 2

queue1 = [3, 2, 7, 2]  # 14
queue2 = [4, 6, 5, 1]  # 16


class QueueSet:
    def __init__(self, queue1: list, queue2: list):
        self.default_queue1 = queue1
        self.default_queue2 = queue2

        self.queue1 = queue1
        self.queue2 = queue2
        self.count = 0

    def pop1(self):
        self.queue2.append(self.queue1.pop(0))
        self.count += 1

    def pop2(self):
        self.queue1.append(self.queue2.pop(0))
        self.count += 1

    def get_possible_combination(self):
        _sum = sum(self.queue1 + self.queue2) / 2
        total_elements = queue1 + queue2
        

    def reset(self):
        self.queue1 = self.default_queue1
        self.queue2 = self.default_queue2
        self.count = 0

    def copy(self):
        return QueueSet(self.queue1, self.queue2)


def calcuate_result(queset: QueueSet):
    queset = queset.copy()
    if sum(queset.queue1 + queset.queue2) % 2 != 0:
        return -1
    i = 0
    while sum(queset.queue1) != sum(queset.queue2):
        if sum(queset.queue1) > sum(queset.queue2):
            queset.pop1()
        else:
            queset.pop2()
        i += 1

    return queset.count


def solution(queue1, queue2):
    queset = QueueSet(queue1, queue2)
    answer = calcuate_result(queset)
    return answer


# print(solution([3, 2, 7, 3], [4, 6, 5, 1]))


