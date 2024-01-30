def solution(msg):
    dict_list = []
    word = msg
    for i in range(26):
        dict_list.append(chr(ord("A") + i))
    print(dict_list)
    answer = []

    while len(word) > 0:
        for i in range(len(dict_list) - 1, -1, -1):
            if word.startswith(dict_list[i]):
                answer.append(i + 1)
                dict_list.append(word[: len(dict_list[i]) + 1])
                word = word[len(dict_list[i]) :]
                break

    return answer


if __name__ == "__main__":
    msg = "KAKAO"
    # answer = [11, 1, 27, 15]
    print(solution(msg))
