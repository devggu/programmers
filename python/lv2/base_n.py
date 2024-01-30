def get_index_list(t,m,p):
    index_list = []
    for i in range(t):
        index_list.append(p-1+m*i)
    print(index_list)

def num2string(n, t, m, p):
    string = ''
    num = 0
    while len(string) < t*m:
        string += str(n)
        n += 1

def solution(n, t, m, p):
    answer = ''
    while len(answer) < t*m:
        answer += str(n)
        n += 1
    return answer
    
if __name__ == "__main__":
    n = 2
    t = 4
    m = 2
    p = 1
    #result = "0111"
    #1 1+m 1+m+m 1+m+m+m
    solution(n, t, m, p)