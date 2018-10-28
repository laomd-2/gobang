//
// Created by laomd on 2018/10/28.
//

#ifndef INC_6_MAZE_HPP
#define INC_6_MAZE_HPP

#include <vector>
#include <tuple>
using namespace std;

typedef pair<int, int> point;
point operator+(const point& a, const point& b) {
    return make_pair(a.first + b.first, a.second + b.second);
}

template <typename T>
istream& operator>>(istream& in, vector<T>& v) {
    for (T& a: v)   in >> a;
    return in;
}

template <typename T>
class Maze : vector<vector<T>> {
    bool is_valid_point(const point& p) const {
        size_t n = this->size();
        return p.first > -1 && p.first < n && p.second > -1 && p.second < n;
    }
public:
    explicit Maze(size_t n) : vector<vector<T>>(n, vector<T>(n)) {

    }

    pair<point, point> get_start_end() const {
        point start_point, end_point;
        bool start = false, end = false;
        for (int i = 0; i < this->size(); ++i) {
            for (int j = 0; j < this->size(); ++j) {
                point p = make_pair(i, j);
                T w = (*this)[p];
                if (w == 2) {
                    start = true;
                    start_point = p;
                    if (end)
                        return make_pair(start_point, end_point);
                } else if (w == 3) {
                    end = true;
                    end_point = p;
                    if (start)
                        return make_pair(start_point, end_point);
                }
            }
        }
        return make_pair(start_point, end_point);
    }

    vector<pair<string, point>> get_neighbors(const point& vertex) const {
        vector<pair<string, point>> neighbors;
        vector<pair<int, int>> directions = {make_pair(-1, 0), make_pair(1, 0),
                                             make_pair(0, -1), make_pair(0, 1)};
        string dir_names[] = {"UP", "DOWN", "LEFT", "RIGHT"};
        for (int i = 0; i < directions.size(); ++i) {
            point n = vertex + directions[i];
            if (is_valid_point(n)) {
                if ((*this)[n]) {
                    neighbors.emplace_back(make_pair(dir_names[i], n));
                }
            }
        }
        return neighbors;
    }

    T operator[](const point& p) const {
        int i, j;
        tie(i, j) = p;
        return (vector<vector<T>>::operator[](i))[j];
    }

    T& operator[](const point& p) {
        int i, j;
        tie(i, j) = p;
        return (vector<vector<T>>::operator[](i))[j];
    }

    friend istream& operator>>(istream& in, Maze<T>& maze) {
        return in >> (static_cast<vector<vector<T>>&>(maze));
    }
};

#endif //INC_6_MAZE_HPP
