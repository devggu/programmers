from collections import Counter


class Database:
    def __init__(self, cacheSize: int):
        self.cached_city = []
        self.cacheSize = cacheSize
        self.timer = 0
        self.cities = Counter()

    def read(self, city: str):
        time = 0
        if city in self.cached_city:
            time = 1
        else:
            time = 5
        self.timer += time
        self.cities[city] = self.timer
        self.update_cache()
        return time

    def update_cache(self):
        self.cached_city = [i[0] for i in self.cities.most_common(self.cacheSize)]


def solution(cacheSize: int, cities: list):
    answer = 0
    db = Database(cacheSize)
    for city in cities:
        answer += db.read(city.lower())
    print(answer)
    return answer


if __name__ == "__main__":
    cacheSize = 3
    cities = [
        "Jeju",
        "Pangyo",
        "Seoul",
        "NewYork",
        "LA",
        "Jeju",
        "Pangyo",
        "Seoul",
        "NewYork",
        "LA",
    ]
    # 50sec
    # cached: 1sec, not cached: 5sec

    solution(cacheSize, cities)
