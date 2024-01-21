n = 7
paths = [
    [1, 2, 5],
    [1, 4, 1],
    [2, 3, 1],
    [2, 6, 7],
    [4, 5, 1],
    [5, 6, 1],
    [6, 7, 1],
]

gates = [3, 7]

summits = [1, 5]

result = [3, 4]


class Point:
    def __init__(self, index):
        self.index = index
        self.is_summit = False
        self.is_gate = False
        self.is_visited = False
        self.linked_points_distance = []


# init points
points: list[Point] = []

# append points
for i in range(n):
    points.append(Point(i + 1))
    if i + 1 in gates:
        points[i].is_gate = True
    if i + 1 in summits:
        points[i].is_summit = True

# append linked points
for path in paths:
    points[path[0] - 1].linked_points_distance.append((points[path[1] - 1], path[2]))
    points[path[1] - 1].linked_points_distance.append((points[path[0] - 1], path[2]))

for i in points:
    print(i.index, i.linked_points_distance)
candidates = []


def find_path_from_summit(
    points: list[Point],
    current_point: Point,
    summit: Point,
    intensity=0,
):
    current_point.is_visited = True
    global candidates

    links = [
        link
        for link in current_point.linked_points_distance
        if not link[0].is_summit
        and not link[0].is_visited
        and (link[1] <= intensity or intensity == 0)
    ]

    for link in links: 
        print(f"for {link[0].index}")
        if intensity < link[1]:
            intensity = link[1]

        if current_point.is_gate:
            candidates.append([summit.index, intensity])
            return

        try:
            next_point = link[0]
            find_path_from_summit(points, next_point, summit, intensity)
        except:
            pass


for summit in summits:
    for point in points:
        point.is_visited = False
    find_path_from_summit(points, points[summit - 1], points[summit - 1])

print(candidates)
# answer = min(candidates, key=lambda x: x[1])

# print(answer)
