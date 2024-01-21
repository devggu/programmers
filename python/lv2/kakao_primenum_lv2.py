def dec2n(n, k):
    rev_base = ""

    while n > 0:
        n, mod = divmod(n, k)
        rev_base += str(mod)

    return rev_base[::-1]


def str2numberlist(k_num):
    number_list = k_num.split("0")
    number_list = [int(i) for i in number_list if i != "" and i != "1"]
    return number_list


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# get prime number from list of numbers
def get_primenum(number_list):
    primenum_list = []
    for number in number_list:
        if number == 2:
            primenum_list.append(number)
        elif number > 2:
            if is_prime(number):
                primenum_list.append(number)
    return primenum_list


def solution(n, k):
    k_num = dec2n(n, k)
    number_list = str2numberlist(k_num)
    prime_list = get_primenum(number_list)
    answer = len(prime_list)
    return answer
