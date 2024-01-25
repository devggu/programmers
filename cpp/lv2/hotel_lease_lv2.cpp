#include <iostream>
#include <sstream>
#include <vector>

using namespace std;

class Room {
  public:
    vector<vector<int>> booked_times = {};

    bool book(vector<int> time) {
        bool is_booked = false;
        for (int i = 0; i < booked_times.size(); ++i) {
            if (true) {
                is_booked = true;
                break;
            }
        }
        if (!is_booked) {
            booked_times.push_back(time);
        }
        return is_booked;
    }
};

int str2Min(string time, bool is_end) {
    stringstream ss(time);
    vector<string> tokens;
    while (getline(ss, time, ':')) {
        tokens.push_back(time);
    }
    int hour = stoi(tokens[0]);
    int minute = stoi(tokens[1]);
    int only_minute = hour * 60 + minute;
    if (is_end) {
        only_minute += 10;
    }
    return only_minute;
}

int solution(vector<vector<string>> book_time) {
    int answer = 0;
    vector<vector<int>> book_time_only_minute = {};
    for (int i = 0; i < book_time.size(); ++i) {
        book_time_only_minute.push_back({str2Min(book_time[i][0], false), str2Min(book_time[i][1], true)});
    }
    cout << book_time_only_minute[0][1] << endl;

    return answer;
}

vector<vector<string>> book_time = {{"15:00", "17:00"}, {"16:40", "18:20"}, {"14:20", "15:20"}, {"14:10", "19:20"}, {"18:20", "21:20"}};

int main() {
    solution(book_time);

    return 0;
}