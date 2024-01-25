from ast import parse
import re
from turtle import position

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

class Participant:
    def __init__(self, info):
        self.info = info
        self.parse_info()
        
    def parse_info(self):
        m = re.match(r'^(java|cpp|python) (frontend|backend) (junior|senior) (pizza|chicken|-) (\d+)$', self.info)
        self.language = m.group(1)
        self.position = m.group(2)
        self.career = m.group(3)
        self.food = m.group(4)
        self.score = int(m.group(5))


def parse_query(query):
    m = re.match(r'^(java|cpp|python|-) and (frontend|backend|-) and (junior|senior|-) and (pizza|chicken|-) (\d+)$', query)
    language = m.group(1)
    position = m.group(2)
    career = m.group(3)
    food = m.group(4)
    score = int(m.group(5))
    return language, position, career, food, score
    


def solution(info, query):
    participant_objects = [Participant(i) for i in info]
    for i in participant_objects:
        print(i.language, i.position, i.career, i.food, i.score)
    
    
if __name__ == '__main__':
    solution(info, query)