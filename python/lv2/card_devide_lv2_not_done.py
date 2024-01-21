def get_gcd(num_list: list):
    gcd = 1
    for i in range(min(num_list), 0, -1):
        if all([num % i == 0 for num in num_list]):
            gcd = i
            break
    return gcd

def condition_1(num_list: list, gcd: int):
    return all([num % gcd == 0 for num in num_list])

def solution(arrayA, arrayB):
    answer = 0
    return answer


arrayA = [14, 35, 119] #  1 <= len <= 500,000 & 1 <= element <= 1,000,000,000
arrayB = [18, 30, 102]
# return 7
solution(arrayA, arrayB)
print(get_gcd(arrayA))
