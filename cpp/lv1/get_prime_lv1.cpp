#include <iostream>
#include <vector>

using namespace std;

bool isPrime(int n) {
    if (n == 2) {
        return true;
    }

    for (int i = 2; i*i <= n; ++i) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}

int solution(int n) {
    int answer = -1;

    for (int i = 1; i <= n; i++) {
        if (isPrime(i)) {
            answer++;
        }
    }
    return answer;
}

int n = 1000000;

int main() { solution(n); }