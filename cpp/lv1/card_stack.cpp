#include <iostream>
#include <vector>

using namespace std;

vector<string> cards1 = {"i", "drink", "water"};
vector<string> cards2 = {"want", "to"};
vector<string> goal = {"i", "want", "to", "drink", "water"};
// result =  yes

string solution(vector<string> cards1, vector<string> cards2, vector<string> goal) {
    vector<string> answer = {};
    vector<string> goal_temp = goal;
    string result = "NO";
    do {
        if (cards1.front() == goal_temp.front()) {
            answer.push_back(cards1.front());
            cards1.erase(cards1.begin());
            goal_temp.erase(goal_temp.begin());
        } else if (cards2.front() == goal_temp.front()) {
            answer.push_back(cards2.front());
            cards2.erase(cards2.begin());
            goal_temp.erase(goal_temp.begin());
        } else {
            break;
        }
    } while (goal_temp.size() > 0);

    if (answer == goal) {
        result = "YES";
    } else {
        result = "NO";
    }

    return result;
}

int main() {
    solution(cards1, cards2, goal);
    return 0;
}