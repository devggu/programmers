fees = [120, 0, 60, 591]
records = [
    "16:00 3961 IN",
    "16:00 0202 IN",
    "18:00 3961 OUT",
    "18:00 0202 OUT",
    "23:58 3961 IN",
]
result = [14600, 34400, 5000]

from math import ceil
import re
import datetime


def records_to_dict(records):
    records_dict = {}
    for record in records:
        time, car_num, status = re.split(" ", record)
        if car_num not in records_dict:
            records_dict[car_num] = [datetime.datetime.strptime(time, "%H:%M")]
        else:
            records_dict[car_num].append(datetime.datetime.strptime(time, "%H:%M"))

    return records_dict


def calculate_fee(fees, records_list):
    fee = 0
    total_minute = 0
    if len(records_list) % 2 != 0:
        records_list.append(datetime.datetime.strptime("23:59", "%H:%M"))

    for i in range(len(records_list) - 1, 0, -2):
        total_minute += (records_list[i] - records_list[i - 1]).total_seconds() // 60

    if total_minute <= fees[0]:
        fee += fees[1]
    else:
        fee += fees[1] + ceil((total_minute - fees[0]) / fees[2]) * fees[3]

    return fee


def solution(fees, records):
    records_dict = records_to_dict(records)
    answer = []

    for k, v in records_dict.items():
        fee = calculate_fee(fees, v)
        answer.append([k, fee])

    answer.sort(key=lambda x: x[0])
    answer = [i[1] for i in answer]
    return answer


print(solution(fees, records))
