import re


class Participant:
    def __init__(self, info):
        self.info = info
        self.parse_info()

    def parse_info(self):
        m = re.match(
            r"^(java|cpp|python) (frontend|backend) (junior|senior) (pizza|chicken|-) (\d+)$",
            self.info,
        )
        self.language = m.group(1)
        self.position = m.group(2)
        self.career = m.group(3)
        self.food = m.group(4)
        self.score = int(m.group(5))
    
    def inspect(self, rule):
        if rule.language != "-" and self.language != rule.language:
            return False
        if rule.position != "-" and self.position != rule.position:
            return False
        if rule.career != "-" and self.career != rule.career:
            return False
        if rule.food != "-" and self.food != rule.food:
            return False
        if self.score < rule.score:
            return False
        return True

class Rules:
    def __init__(self, query):
        self.parse_query(query)
        self.num_qualified = 0

    def parse_query(self, query):
        m = re.match(
            r"^(java|cpp|python|-) and (frontend|backend|-) and (junior|senior|-) and (pizza|chicken|-) (\d+)$",
            query,
        )
        self.language = m.group(1)
        self.position = m.group(2)
        self.career = m.group(3)
        self.food = m.group(4)
        self.score = int(m.group(5))


def solution(info, query):
    participant_objects = [Participant(i) for i in info]
    rule_objects = [Rules(i) for i in query]
    answer = []
    for rule in rule_objects:
        for participant in participant_objects:
            if participant.inspect(rule):
                rule.num_qualified += 1
        answer.append(rule.num_qualified)
    print(answer)
    return answer


if __name__ == "__main__":
    info = [
        "java backend junior pizza 150",
        "python frontend senior chicken 210",
        "python frontend senior chicken 150",
        "cpp backend senior pizza 260",
        "java backend junior chicken 80",
        "python backend senior chicken 50",
    ]

    query = [
        "java and backend and junior and pizza 100",
        "python and frontend and senior and chicken 200",
        "cpp and - and senior and pizza 250",
        "- and backend and senior and - 150",
        "- and - and - and chicken 100",
        "- and - and - and - 150",
    ]
    solution(info, query)
