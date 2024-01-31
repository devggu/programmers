from timer_decorator import timer
import itertools

# @timer
# def solution(orders, course):
#     answer = []
#     menu_list = list(set("".join(orders)))
#     menu_list.sort()
#     menu_combinations_counter = {}
    
#     for i in course:
#         menu_combinations_counter[f"{i}"] = {}
#         for combination in itertools.combinations(menu_list, i ):
#             menu_combinations_counter[f"{i}"]["".join(combination)] = 0
    
#     for course_num in menu_combinations_counter.keys():
#         for combination in menu_combinations_counter[course_num].keys():
#             for order in orders:
#                 if set(combination).issubset(set(order)):
#                     menu_combinations_counter[course_num][combination] += 1
#         max_value = max(menu_combinations_counter[course_num].values())
#         answer += [k for k,v in menu_combinations_counter[course_num].items() if v == max_value and v > 1]
    # answer.sort(key= lambda x: x)
    # return answer

@timer
def solution(orders, course):
    answer = []
    combinations = {}
    done = []
    for order in orders:
        i=orders.index(order)
        while i < len(orders)-1:
            temp = set(order) & set(orders[i+1])
            temp = "".join(sorted(temp))
            if temp in done:
                i+=1
                continue
            if temp != "" and len(temp) > 1:
                if temp not in combinations:
                    combinations[temp] = 1
                combinations[temp] += 1
            i+=1
            if i == len(orders)-1:
                done.append(order)
                break
    print(done)
    print(combinations)
            
    return answer


if __name__ == "__main__":
    test_cases = [
        [
            ["ABCFG", "AC", "CDE", "ACDE", "BCFG", "ACDEH"],
            [2, 3, 4],
            ["AC", "ACDE", "BCFG", "CDE"],
        ],
        [
            ["ABCDE", "AB", "CD", "ADE", "XYZ", "XYZ", "ACD"],
            [2, 3, 5],
            ["ACD", "AD", "ADE", "CD", "XYZ"],
        ],
        [
            ["XYZ", "XWY", "WXA"],
            [2, 3, 4],
            ["WX", "XY"],
        ],
    ]

    for case in test_cases:
        orders = case[0]
        course = case[1]
        result = case[2]
        if solution(orders, course) == result:
            print(f"Test Case{test_cases.index(case)}: Pass")
        else:
            print(f"Test Case{test_cases.index(case)}: Fail")
