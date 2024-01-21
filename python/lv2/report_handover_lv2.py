class Lesson:
    def __init__(self, lesson_property: list):
        self.name = lesson_property[0]
        self.start_time = int(lesson_property[1].split(":")[0]) * 60 + int(
            lesson_property[1].split(":")[1]
        )
        self.duration = int(lesson_property[2])
        self.done_at = 0

    def do_homework(self, lesson_queue: list, start_time=None, next_lesson=None):
        if start_time:
            self.start_time = start_time
        if next_lesson is None:
            self.done_at = self.start_time + self.duration
            return
        elif self.start_time + self.duration <= next_lesson.start_time:
            self.done_at = self.start_time + self.duration
        else:
            self.duration = self.start_time + self.duration - next_lesson.start_time
            lesson_queue.append(self)


def solution(plans):
    plan_objects = [Lesson(plan) for plan in sorted(plans, key=lambda x: x[1])]
    lesson_queue = []
    current_time = 0

    for i in range(len(plan_objects)):
        if i == len(plan_objects) - 1:
            plan_objects[i].do_homework(lesson_queue)
        plan_objects[i].do_homework(lesson_queue, next_lesson=plan_objects[i + 1])

    answer = []
    for i in plan_objects:
        print(f"i: {i.name}")
    print(f"executed: {plans}")
    return answer


# result =  ["science", "history", "computer", "music"]
if __name__ == "__main__":
    plans = [
        ["science", "12:40", "50"],
        ["music", "12:20", "40"],
        ["history", "14:00", "30"],
        ["computer", "12:30", "100"],
    ]
    solution(plans)
