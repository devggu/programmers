bandage = [3, 2, 7]
health = 20
attacks = [[1, 15], [5, 16], [8, 6]]
result = 5


class Character:
    def __init__(self, health, bandage):
        self.max_health = health
        self.health = health
        self.bandage = {
            "casting_time": bandage[0],
            "heal": bandage[1],
            "additional_heal": bandage[2],
        }

    def bangage(self, attacks):
        for i in range(len(attacks)):
            if i != 0:
                self.health += (attacks[i][0] - attacks[i - 1][0] - 1) // self.bandage[
                    "casting_time"
                ] * (
                    self.bandage["heal"] * self.bandage["casting_time"]
                    + self.bandage["additional_heal"]
                ) + (
                    attacks[i][0] - attacks[i - 1][0] - 1
                ) % self.bandage[
                    "casting_time"
                ] * self.bandage[
                    "heal"
                ]
            if self.health >= self.max_health:
                self.health = self.max_health
            self.health -= attacks[i][1]

            if self.health <= 0:
                return -1

        return self.health


def solution(bandage, health, attacks):
    char = Character(health, bandage)
    answer = char.bangage(attacks)
    return answer


print(solution(bandage, health, attacks))
