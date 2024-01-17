#include <iostream>
#include <vector>

using namespace std;

vector<int> nums = {1, 2, 3, 4};
// result = 1

vector<int> calc_result = {};
vector<vector<int>> temp_list = {};
vector<int> getCombination(vector<int> nums, int target) {
    
    vector<vector<int>> combination_indexes;
    int len_nums = nums.size();
    for (int i; i < nums.size(); i++) {
        combination_indexes.push_back({i, i + 1, i + 2});
    }


    // for (int i; i < nums.size() - 2; i++) {
    //     vector<int> temp = {};
    //     temp.push_back(nums[i]);
    //     for (int j; j < nums.size() - 1; j++) {
    //         temp.push_back(nums[i + 1]);
    //     }
    // }

    return calc_result;
}

bool isPrime(int number) {

    int i;
    int n = number;
    bool is_prime = true;

    // 0 and 1 are not prime numbers
    if (n == 0 || n == 1) {
        is_prime = false;
    }

    // loop to check if n is prime
    for (i = 2; i <= n / 2; ++i) {
        if (n % i == 0) {
            is_prime = false;
            break;
        }
    }

    return is_prime;
}
int solution(vector<int> nums) {
    int answer = -1;
    return answer;
}

int main() {}