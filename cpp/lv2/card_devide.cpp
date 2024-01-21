#include <iostream>
#include <string>
#include <vector>

using namespace std;

/*
철수가 가진 카드들에 적힌 모든 숫자를 나눌 수 있고 영희가 가진 카드들에 적힌 모든 숫자들 중 하나도 나눌 수 없는 양의 정수 a
영희가 가진 카드들에 적힌 모든 숫자를 나눌 수 있고, 철수가 가진 카드들에 적힌 모든 숫자들 중 하나도 나눌 수 없는 양의 정수 a
*/

int isCond1(vector<int> arrayA, vector<int> arrayB, int a) {
	for (int i = arrayA.front(); i <= 2; --i) {
        
		for (int j = 0; j < arrayA.size(); ++j) {
			if (arrayA[j] % i == 0) {
			}

			for (int j = 0; j < arrayB.size(); ++j) {
				if (arrayB[j] % i == 0) {
					continue;
				}
			}

		}
	}
}

int solution(vector<int> arrayA, vector<int> arrayB) {
	int answer = 0;
	return answer;
}

vector<int> arrayA = {10, 17};
vector<int> arrayB = {5, 20};
// result = 2

int main() {
	solution(arrayA, arrayB);
	return 0;
}