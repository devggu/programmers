#include <stdio.h>
#include <iostream>
#include <map>
#include <string>

using namespace std;

string X = "2300";
string Y = "2345";
// answer = "-1"

bool isZero(string str) {
  for (int i = 0; i < str.length(); i++) {
    if (str[i] != '0') {
      return false;
    }
  }
  return true;
}

string solution(string X, string Y) {
  string result = "";
  map<string, int> x_map;
  map<string, int> y_map;
  map<string, int> xy_map;
  for (int i = 0; i < 10; i++) {
    x_map[to_string(i)] = 0;
    y_map[to_string(i)] = 0;
  }
  for (int i = 0; i < X.length(); i++) {
    x_map[string(1, X[i])]++;
  }

  for (int i = 0; i < Y.length(); i++) {
    y_map[string(1, Y[i])]++;
  }

  for (int i = 0; i < 10; i++) {
    xy_map[to_string(i)] = min(x_map[to_string(i)], y_map[to_string(i)]);
  }

  for (int i = 9; i >= 0; i--) {
    for (int j = 0; j < xy_map[to_string(i)]; j++) {
      result += to_string(i);
    }
  }

  if (result == "") {
    result = "-1";
  } else if (isZero(result)) {
    result = "0";
  }

  return result;
}

int main() { solution(X, Y); }
