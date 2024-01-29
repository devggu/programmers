def solution(s):
    answer = 0
    candidate = []
    if len(s) == 1:
        return 1
    for i in range(1, len(s) // 2 + 1):
        temp = ""
        temp_back = ""
        cnt = 1
        candidate_item = ""
        for j in range(0, len(s)+i, i):
            temp = s[j : j + i]
            if temp_back == "":
                temp_back = temp
                continue
            if temp == temp_back:
                cnt += 1
            else:
                if cnt > 1:
                    candidate_item += str(cnt)
                candidate_item += temp_back
                cnt = 1
            temp_back = temp

        candidate.append(len(candidate_item))
    print(candidate)
    answer = min(candidate)
    return answer


# result = 7
"""
"aabbaccc"	7
"ababcdcdababcdcd"	9
"abcabcdede"	8
"abcabcabcabcdededededede"	14
"xababcdcdababcdcd"	17
"""

if __name__ == "__main__":
    s = "x"
    print(s[100:200])
    print(solution(s))
