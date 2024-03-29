import re


class Participant:
    def __init__(self, info):
        self.info = info
        self.properties = set()
        self.parse_info()

    def parse_info(self):
        m = re.match(
            r"^(java|cpp|python) (frontend|backend) (junior|senior) (pizza|chicken|-) (\d+)$",
            self.info,
        )
        for i in range(1,5):
            self.properties.add(m.group(i))
        self.score = int(m.group(5))
    
    def inspect(self, rule):
        if not rule.properties.issubset(self.properties):
            return False
        elif self.score < rule.score:
            return False
        return True

class Rules:
    def __init__(self, query):
        self.properties = set()
        self.num_qualified = 0
        self.parse_query(query)

    def parse_query(self, query):
        m = re.match(
            r"^(java|cpp|python|-) and (frontend|backend|-) and (junior|senior|-) and (pizza|chicken|-) (\d+)$",
            query,
        )
        for i in range(1,5):
            if m.group(i) != "-":
                self.properties.add(m.group(i))
        self.score = int(m.group(5))


def solution(info, query):
    participant_objects = [Participant(i) for i in info]
    rule_objects = [Rules(i) for i in query]
    answer = []
    for rule in rule_objects:
        if len(rule.properties) == 0:
            for 
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
