import re


def level1(new_id:str):
    id = new_id.lower()
    id = re.sub(r"[^a-z0-9-_.]","",id)
    id = re.sub(r"\.+",".",id)
    if id[0] == ".":
        id = id[1:]
    if id == "":
        id = "a"
    if len(id) >= 16:
        id = id[:15]
    if id[-1] == ".":
        id = id[:-1]
    if len(id) <= 2:
        while len(id) < 3:
            id = id+ id[-1]
    
    return id

    

def solution(new_id):
    id = new_id
    
    id = level1(id)
 
    answer = id
    return answer


print(solution("z-+.^."))