#include <stdio.h>

#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

vector<int> nums = {1, 2, 3, 4};

vector<int> calc_result = {};
bool isPrime(int number) {
	int i;
	int n = number;
	bool is_prime = true;

	if (n == 0 || n == 1) {
		is_prime = false;
	}

	for (i = 2; i <= n / 2; ++i) {
		if (n % i == 0) {
			is_prime = false;
			break;
		}
	}

	return is_prime;
}

int getCombinations(vector<int> nums, int r) {
	vector<int> visit;
	vector<int> result;
	for (int i = 0; i < nums.size(); ++i) {
		if (i < nums.size() - r)
			visit.push_back(0);
		else
			visit.push_back(1);
	}
	int temp = 0;
	do {
		for (int i = 0; i < nums.size(); ++i)
			if (visit[i] != 0)
				temp += nums[i];
		calc_result.push_back(temp);
		temp = 0;
	} while (next_permutation(visit.begin(), visit.end()));

	for (int i = 0; i < calc_result.size(); ++i) {
		if (isPrime(calc_result[i])) {
			result.push_back(calc_result[i]);
		}
	}

	return result.size();
}

int solution(vector<int> nums) {
	int answer;
	answer = getCombinations(nums, 3);
    printf("%d", answer);
	return answer;
}

int main() { solution(nums); }