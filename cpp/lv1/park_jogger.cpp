#include <iostream>
#include <sstream>
#include <vector>

using namespace std;

vector<string> park = {"OSO","OOO","OXO","OOO"};
vector<string> routes = {"E 2","S 3","W 1"};
//result = [0,0]
// 2,1    1,1    
class Park {
    public:
        vector<vector<int>> obstacles;
        vector<int> starting_point;
        vector<unsigned long long> park_size;
        Park(vector<string> park) {
            ParsePark(park);
            park_size = {park.size(), park[0].size()};
        }
        
        void ParsePark(vector<string> park) {
            for (int i=0; i < park.size(); i++) {
                for (int j=0; j < park[i].size(); j++) {
                    if (park[i][j] == 'X') {
                        obstacles.push_back({i,j});                                     
                    } else if (park[i][j] == 'S') {
                        starting_point = {i,j};
                    }
                }
            }
        }
};


class Dog {
    public:
        vector<int> loc;
        Dog(vector<string> park) {
        }
        

        void Move(string route) {
            string direction;
            string distance_str;
            istringstream iss(route);
            iss >> direction >> distance_str;
            int distance = stoi(distance_str);
            
            if (direction == "N") {
                loc[0] -= distance;
            } else if (direction == "S") {
                loc[0] += distance;
            } else if (direction == "E") {
                loc[1] += distance;
            } else if (direction == "W") {
                loc[1] -= distance;
            }
        }
        
        void CheckValid(Park park) {
            for (int i=0; i < park.obstacles.size(); i++) {
                if (park.obstacles[i] == loc) {
                    cout << "Invalid" << endl;
                    return;
                }
            }
            cout << "Valid" << endl;
        }
};

vector<int> solution(vector<string> park,vector<string> routes) {

}

int main() {
    solution();
}