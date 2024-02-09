from timer_decorator import timer


# class Hotel:
#     def __init__(self, k):
#         self.soldout = []

#     def dispense_room(self, room_number):
#         if room_number in self.soldout:
#             room_number = self.soldout[-1] + 1


#         self.soldout.append(room_number)
#         return room_number


# @timer
# def solution(k, room_number):
#     answer = []
#     hotel = Hotel(k)
#     for number in room_number:
#         answer.append(hotel.dispense_room(number))

#     return answer


# @timer
# def solution(k, room_number):
#     answer = []
#     answer_set = set()
#     for number in room_number:
#         if number not in answer_set:
#             answer.append(number)
#             answer_set.add(number)
#         else:
#             if number == max(answer_set):
#                 answer.append(number+1)
#                 answer_set.add(number+1)
#             else:
#                 for i in answer_set:
#                     if i >= number and i+1 not in answer_set:
#                         answer.append(i+1)
#                         answer_set.add(i+1)
#                         break
                        
    
#     return answer

@timer
def solution(k, room_number: list):
    answer = []
    room_map = map(room_number.count, room_number)
    
    for room in room_map:
        if room not in answer:
            answer.append(room)
        else:
            if room == max(answer):
                answer.append(room+1)
            else:
                for i in range(room, max(answer)):
                    if i not in answer:
                        answer.append(i)
                        break
    
    return answer



if __name__ == "__main__":
    test_cases = [
        [
            10,
            [1, 3, 4, 1, 3, 1],
            [1, 3, 4, 2, 5, 6],
        ],
        [
            1,
            [1],
            [1],
        ],
        [
            20000000,
            [3,5,6,8,8,10000000000000,8,8,8,8,8,9,9999999999,9999999999],
            [],
        ],
    ]

    for t in test_cases:
        k, room_number, answer = t
        result = solution(k, room_number)

        if answer == result:
            print(f"CASE {test_cases.index(t)}: PASS")
        else:
            print(f"CASE {test_cases.index(t)}: FAIL")
            print(f"Answer: {answer}, Result: {result}")
