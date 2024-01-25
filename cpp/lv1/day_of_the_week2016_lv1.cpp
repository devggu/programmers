#include <iostream>
#include <time.h>
#include <vector>
#include <string>
#include <stdio.h>


using namespace std;

const vector<string> DAYS = {"SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"};
const vector<int> DAYS_OF_MONTH = {31,29,31,30,31,30,31,31,30,31,30,31};

string solution(int a, int b) {
    string answer = "";
    int days = 0;
    for (int i = 0; i < a-1; i++) {
        days += DAYS_OF_MONTH[i];
    }
    days += b - 1;

    int day = (days + 5) % 7;
    answer = DAYS[day];
    return answer;
}

int a = 6;
int b = 8;

int main() {
    solution(a, b);
    return 0;
}