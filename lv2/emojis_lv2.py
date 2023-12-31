users_ex = [
    [40, 2900],
    [23, 10000],
    [11, 5200],
    [5, 5900],
    [40, 3100],
    [27, 9200],
    [32, 6900],
]  # [emoticon discount, maximum budget]
emoticons_ex = [
    1300,
    1500,
    1600,
    4900,
]  # [emoticon price, subscription price]
result_ex = [4, 13860]  # [emoticon plus subscription, total sales ]

# Goal: 1. Find the scenario that maximizes the total emoticon plus subscriptions.
#       2. Find the scenario that maximizes the budget.
# discount rate = [10,20,30,40]

import itertools


class Users:
    def __init__(self, index: int, desired_discount: int, budget: int):
        self.index: int = index
        self.desired_discount: int = desired_discount
        self.budget: int = budget
        self.is_subscribed: bool = False
        self.total_spent: int = 0

    def purchase_emoticon(self, emoticons):
        for emoticon in emoticons:
            if emoticon.discount >= self.desired_discount:
                self.total_spent += int(
                    emoticon.price * (100 - emoticon.discount) / 100
                )
                if self.total_spent >= self.budget:
                    self.total_spent = 0
                    self.is_subscribed = True

    def reset(self):
        self.is_subscribed: bool = False
        self.emoticon_purchased: list = []
        self.total_spent: int = 0


class Emoticon:
    def __init__(self, index: int, price: int, discount: int = 10):
        self.index: int = index
        self.price: int = price
        self.discount: int = discount


def solution(users: list, emoticons: list):
    emoticon_objects: list = []
    for emoticon in emoticons:
        emoticon_objects.append(Emoticon(emoticons.index(emoticon), emoticon))

    user_objects = []
    for user in users:
        user_objects.append(Users(users.index(user), user[0], user[1]))

    discounts = [10, 20, 30, 40]
    discount_combinations = list(
        itertools.product(discounts, repeat=len(emoticon_objects))
    )

    scenario_list = []
    for i in range(len(discount_combinations)):
        for j in range(len(emoticon_objects)):
            emoticon_objects[j].discount = discount_combinations[i][j]
        for user in user_objects:
            user.purchase_emoticon(emoticon_objects)

        scenario = [0, 0]
        for user in user_objects:
            if user.is_subscribed:
                scenario[0] += 1
            else:
                scenario[1] += user.total_spent
        scenario_list.append(scenario)
        for user in user_objects:
            user.reset()
            
    scenario_list.sort(key=lambda x: (x[0], x[1]))
    answer = scenario_list[-1]
    return answer


print(solution(users_ex, emoticons_ex))
