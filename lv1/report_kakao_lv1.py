id_list = ["muzi", "frodo", "apeach", "neo"]

report = ["muzi frodo", "apeach frodo", "frodo neo", "muzi neo", "apeach muzi"]

k = 2

result = [2, 1, 1, 0]


class User:
    def __init__(self, id: str):
        self.id = id
        self.users_reported: set[User] = set()
        self.result_emails: list[User] = []
        # self.is_banned = False

    def add_reported_user(self, user, k: int):
        self.users_reported.add(user)
        # for user in self.users_reported:
        #     if len(self.users_reported) >= k and self.is_banned == False:
        #         self.is_banned = True
        #         self.send_email()

    def send_email(self):
        if len(self.users_reported) >= k:
            for user in self.users_reported:
                user.result_emails.append(self)

def solution(id_list: list[str], report: list[str], k: int):
    # init users
    users: dict[str,User] = {}
    for id in id_list:
        users[id] = User(id)
    
    for r in report:
        reporter, reported = r.split()
        users[reported].add_reported_user(users[reporter], k)
    
    for user in users.values():
        user.send_email()
    
    answer = [users[user].result_emails.__len__() for user in id_list] 
    
    return answer

print(solution(id_list, report, k))