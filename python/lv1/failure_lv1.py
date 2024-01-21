from collections import Counter


N = 5
stages = [1, 1, 1, 2, 3, 4]
reslut = [4, 1, 3, 2, 5]


class Stage:
    def __init__(self, stage_number):
        self.stage_number = stage_number
        self.reached_count = 0
        self.cleared_count = 0
        self.failure_rate = 0

    def calc_failure_rate(self, stage_count: Counter):
        for k, v in stage_count.items():
            if k > self.stage_number:
                self.reached_count += v
                self.cleared_count += v
            elif k == self.stage_number:
                self.reached_count += v
                
        if self.reached_count != 0:
            self.failure_rate = 1 - (self.cleared_count / self.reached_count)


def solution(N, stages):
    stage_list = [Stage(i) for i in range(1, N + 1)]
    stage_counter = Counter(stages)

    for stage in stage_list:
        stage.calc_failure_rate(stage_counter)

    stage_list.sort(key=lambda x: [x.failure_rate, -x.stage_number], reverse=True)

    answer = [stage.stage_number for stage in stage_list]
    return answer


# print(Counter(stages))
print(solution(N, stages))
