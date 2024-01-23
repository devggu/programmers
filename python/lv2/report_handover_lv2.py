class Lesson:
    def __init__(self, lesson_property: list):
        self.name = lesson_property[0]
        self.start_time = int(lesson_property[1].split(":")[0]) * 60 + int(lesson_property[1].split(":")[1])
        self.duration = int(lesson_property[2])

    def do_homework(self, done_list: list, spare_queue: list, current_time=None, next_lesson=None):
        if current_time != None:
            self.start_time = current_time

        if (next_lesson == None) or (self.start_time + self.duration <= next_lesson.start_time):
            done_list.append(self)
            try:
                spare_queue.remove(self)
            except:
                pass
            return self.duration
        else:
            self.duration = self.duration - (next_lesson.start_time - self.start_time)
            spare_queue.append(self)
            return next_lesson.start_time - self.start_time


def solution(plans):
    plan_objects = [Lesson(plan) for plan in sorted(plans, key=lambda x: x[1])]
    done_list = []
    spare_queue = []
    current_time = plan_objects[0].start_time
    for plan in plan_objects:
        if plan_objects.index(plan) == len(plan_objects) - 1:
            current_time += plan.do_homework(done_list, spare_queue)
            done_list += spare_queue
        else:
            current_time += plan.do_homework(done_list, spare_queue, next_lesson=plan_objects[plan_objects.index(plan) + 1])
            for spare in spare_queue:
                if current_time == plan_objects[plan_objects.index(plan) + 1].start_time:
                    break
                current_time += spare.do_homework(
                    done_list, spare_queue, current_time, plan_objects[plan_objects.index(plan) + 1]
                )

    print([done.name for done in done_list])
    return done_list


# result =  ["science", "history", "computer", "music"]
if __name__ == "__main__":
    plans = [
        ["music", "12:20", "40"],
        ["computer", "12:30", "100"],
        ["science", "12:40", "50"],
        ["history", "14:00", "30"],
    ]
    solution(plans)
