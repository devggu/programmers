from collections import Counter


friends = ["muzi", "ryan", "frodo", "neo"]
gifts = ["muzi frodo", "muzi frodo", "ryan muzi", "ryan muzi", "ryan muzi", "frodo muzi", "frodo ryan", "neo muzi"]
result = 2

class Character:
    def __init__(self, name: str,gifts: list):
        self.name = name
        self.given = Counter()
        self.received = Counter()
        self.calculate(gifts)
        
    def give(self, name: str):
        self.given[name] += 1
        
    def receive(self, name: str):
        self.received[name] += 1

    def calculate(self,gifts):
        for gift in gifts:
            giver, receiver = gift.split()
            if giver == self.name:
                self.give(receiver)
            if receiver == self.name:
                self.receive(giver)
    
    def next_month(self):
        for giver in self.given:
            if self.given[giver] > 


friend_objs = []
for friend in friends:
    friend_objs.append(Character(friend, gifts))
    
for friend in friend_objs:
    print(friend.name, friend.given, friend.received)
    
  


def solution(friends, gifts):
    answer = 0
    return answer
