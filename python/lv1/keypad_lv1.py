numbers = [1, 3, 4, 5, 8, 2, 1, 4, 5, 9, 5]
hand = "right"
result = "LRLLLRLLRRL"


class Finger:
    def __init__(self, hand):
        self.hand = hand
        self.position = 10 if hand == "right" else 12

    def move(self, position):
        self.position = position
        return "R" if self.hand == "right" else "L"


def get_distance(finger: Finger, destination):
    if finger.position == 0:
        finger.position = 11
    if destination == 0:
        destination = 11

    current_x, current_y = (finger.position - 1) % 3, (finger.position - 1) // 3
    destination_x, destination_y = (destination - 1) % 3, (destination - 1) // 3
    return abs(current_x - destination_x) + abs(current_y - destination_y)

def solution(numbers, hand):
    left_finger = Finger("left")
    right_finger = Finger("right")
    result = ""

    for number in numbers:
        if number in [1, 4, 7]:
            result += left_finger.move(number)
        elif number in [3, 6, 9]:
            result += right_finger.move(number)
        else:
            left_distance = get_distance(left_finger, number)
            right_distance = get_distance(right_finger, number)
            if left_distance < right_distance:
                result += left_finger.move(number)
            elif left_distance > right_distance:
                result += right_finger.move(number)
            else:
                if hand == "right":
                    result += right_finger.move(number)
                else:
                    result += left_finger.move(number)
    answer = result
    return answer


print(solution(numbers, hand))
