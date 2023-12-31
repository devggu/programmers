today = "2023.01.01"
terms = ["A 6"]
privacies = ["2022.07.01 A", "2022.07.01 A", "2022.07.01 A"]
result = [1,2,3]

class Privacy:
    def __init__(self,index:int, privacy:str, terms_dict:dict, today:str, expired:list):
        self.index:int = index
        self.date:int = self.parse_date(privacy.split()[0])
        self.type:str = privacy.split()[1]
        self.check_valid(today, terms_dict, expired)
        
    def check_valid(self, today:str, terms_dict:dict, expired:list):
        today = self.parse_date(today)
        if self.date +int(terms_dict[self.type])*28 <= today:
            self.valid = False
            expired.append(self.index)
        else:
            self.valid = True
            
    def parse_date(self, date:str):
        date_parse = date.split('.')
        return int(date_parse[0])*12*28+int(date_parse[1])*28+int(date_parse[2])


def solution(today, terms:list[str], privacies: list[str]):
    privacy_objects:list[Privacy] = []
    expired_list:list[int] = []
    terms_dict:dict[str,str] = {}
    
    for term in terms:
        term = term.split()
        terms_dict[term[0]] = term[1]

    for i in range(len(privacies)):
        privacy_objects.append(Privacy(i+1, privacies[i], terms_dict, today, expired_list))
        
    answer = expired_list
    return answer

print(solution(today, terms, privacies))