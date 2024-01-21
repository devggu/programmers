from collections import Counter

def make_set(str:str):
    str = str.lower()
    str_list = []
    for i in range(len(str)-1):
        if str[i].isalpha() and str[i+1].isalpha():
            str_list.append(str[i]+str[i+1])
    return Counter(str_list)

def compare_set(str1:str, str2:str):
    str1_set = make_set(str1)
    str2_set = make_set(str2)
    if len(str1_set) == 0 and len(str2_set) == 0:
        return 65536
    union = str1_set | str2_set
    intersection = str1_set & str2_set
    jaccard = int(sum(intersection.values())/sum(union.values())*65536)
    
    return jaccard

def solution(str1, str2):
    answer = compare_set(str1,str2)
    print(answer)
    return answer

solution("FRANCE","french")