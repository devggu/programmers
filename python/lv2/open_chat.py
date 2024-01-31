def parse_log(log, answer: list):
    try:
        command, uid, name = log.split(" ")
    except:
        command, uid = log.split(" ")

    if command == "Enter":
        answer.append(f"{uid}님이 들어왔습니다.")

    elif command == "Leave":
        answer.append(f"{uid}님이 나갔습니다.")


def get_final_name(record):
    user_dict = {}
    record_list = [x.split(" ") for x in record if x.split(" ")[0] != "Leave"]
    record_list.reverse()
    for command, uid, name in record_list:
        if uid not in user_dict:
            user_dict[uid] = name

    return user_dict


def solution(record):
    answer = []
    answer = []

    user_dict = get_final_name(record)

    for log in record:
        parse_log(log, answer)

    for i in range(len(answer)):
        answer[i] = answer[i].replace(
            answer[i].split("님")[0], user_dict[answer[i].split("님")[0]]
        )

    # for k,v in user_dict.items():
    #     for i in range(len(answer)):
    #         if k in answer[i]:
    #             answer[i] = answer[i].replace(k, v)

    print(user_dict)
    print(answer)
    return answer


if __name__ == "__main__":
    record = [
        "Enter uid1234 Muzi",
        "Enter uid4567 Prodo",
        "Leave uid1234",
        "Enter uid1234 Prodo",
        "Change uid4567 Ryan",
    ]
    # result = ["Prodo님이 들어왔습니다.", "Ryan님이 들어왔습니다.", "Prodo님이 나갔습니다.", "Prodo님이 들어왔습니다."]
    solution(record)
