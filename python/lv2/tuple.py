def solution(s: str):
    answer = []
    num_list = eval(s.replace("{", "[").replace("}", "]"))
    num_list.sort(key=lambda x: len(x))
    
    for i in range(len(num_list)):
        if i == 0:
            answer.append(num_list[i][0])
        else:
            answer.append(list(set(num_list[i]) - set(num_list[i-1]))[0])
    
    num_list[-1]
    
    return answer

from collections import Counter

def solution2(s: str):
    answer = []
    num_list = s.replace("{", "").replace("}", "").split(",")
    counter = Counter(num_list)
    
    for key, value in counter.most_common():
        answer.append(int(key))
    
    return answer

if __name__ == "__main__":
    s = "{{2},{2,1},{2,1,3},{2,1,3,4}}"
    solution2(s)
