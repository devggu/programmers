#include <iostream>
#include <vector>
#include <map>

using namespace std;

vector<string> name = {"may", "kein", "kain", "radi"};
vector<int> yearning = {5, 10, 1, 3};
vector<vector<string>> photo = {
    {"may", "kein", "kain", "radi"},
    {"may", "kein", "brin", "deny"},
    {"kon", "kain", "may", "coni"},
};

// result = [19, 15, 6];

class Photo {
   public:
    vector<string> name;
    vector<int> yearning;
    vector<vector<string>> photo;
    vector<int> point;
    map<string, int> name_point;

    Photo(vector<string> name, vector<int> yearning,
          vector<vector<string>> photo) {
        this->name = name;
        this->yearning = yearning;
        this->photo = photo;
        for (int i=0; i < name.size(); i++) {
            name_point.insert(make_pair(name[i], yearning[i]));
        }
    }

    int calculate_point(vector<string> p) {
        int pt = 0;
        for (int i = 0; i < p.size(); i++) {
            pt += name_point[p[i]]; 
        }
        return pt;
    }

    void create_point_list() {
        for (int i=0; i < photo.size(); i++) {
            point.push_back(calculate_point(photo[i]));
        }
    }

};

vector<int> solution(vector<string> name, vector<int> yearning,vector<vector<string>> photo) {
    Photo p(name, yearning, photo);
    p.create_point_list();
    for (int i=0; i < p.point.size(); i++) {
        cout << p.point[i] << endl;
    }   
    return p.point;
}

int main() {
    solution(name, yearning, photo);
}
