from timer_decorator import timer
import pandas as pd
import itertools


@timer
def solution(relation):
    answer_columns = []
    df = pd.DataFrame(relation)
    column_number = len(df.columns.tolist())

    while len(df.columns.tolist()) > 0:
        for num_columns in range(1, column_number + 1):
            if len(df.columns.tolist()) < num_columns:
                print(answer_columns)
                return len(answer_columns)
            combination_list = [list(i) for i in itertools.combinations(df.columns.tolist(), num_columns)]
            while len(combination_list) > 0:
                temp = combination_list.pop(0)
                if not df[temp].duplicated().any():
                    answer_columns.append(temp)
                    df.drop(temp, axis=1, inplace=True)
                    for i in temp:
                        combination_list = list(filter(lambda x: i not in x, combination_list))
  

            
            # for i in combination_list:

            #     if i not in df.columns.tolist():
            #         continue
            #     print(df.columns.tolist())
            #     print(i)
            #     print(df[i].duplicated().any())
            #     if not df[i].duplicated().any():
            #         answer_columns.append(i)
            #         df.drop(i, axis=1, inplace=True)
            #     if df.empty:
            #         break
            #     print(df)

    print(answer_columns)
    return answer


if __name__ == "__main__":
    test_cases = [
        [
            [
                ["100", "ryan", "music", "2"],
                ["200", "apeach", "math", "2"],
                ["300", "tube", "computer", "3"],
                ["400", "con", "computer", "4"],
                ["500", "muzi", "music", "3"],
                ["600", "apeach", "music", "2"],
            ],
            2,
        ]
    ]

    for t in test_cases:
        if t[1] == solution(t[0]):
            print(f"case{test_cases.index(t)}: Passed")
        else:
            print(f"case{test_cases.index(t)}: Failed")
