import re


def solution(dartResult):
    result_list = re.findall(r"\d+[D,S,T,#,*]+", dartResult)
    result_values = []
    for i, result in enumerate(result_list):
        number_temp = re.findall(r"\d+", result)[0]
        number = int(number_temp)
        area = re.findall(r"[D,S,T]", result)[0]
        try:
            bonus = re.findall(r"[#,*]", result)[0]
        except:
            bonus = ""

        if area == "D":
            number = number**2

        elif area == "T":
            number = number**3

        if bonus == "*":
            if i == 0:
                number *= 2
            else:
                number *= 2
                result_values[i - 1] *= 2

        elif bonus == "#":
            number *= -1

        result_values.append(number)

    answer = sum(result_values)

    return answer


print(solution("1D2S#10S"))
