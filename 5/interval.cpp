//
// Created by laomd on 2018/10/15.
//
#include <iostream>
#include <algorithm>
#include <list>
using namespace std;

typedef pair<int, int> interval;

list<interval> read_interval() {
    int n;
    cin >> n;
    list<interval> intervals;
    int first, last;
    while (n--) {
        cin >> first >> last;
        intervals.emplace_back(make_pair(first, last));
    }
    return intervals;
}

bool is_intersect(const interval& a, const interval& b) {
    return !(a.second < b.first or a.first > b.second);
}

int main() {
    list<interval> blues = read_interval();
    list<interval> reds = read_interval();

    auto pred = [](const interval& a, const interval& b) {
        return a.second < b.second;
    };
    blues.sort(pred);
    reds.sort(pred);

    int count = 0;
    auto it = blues.begin(), it2 = reds.begin();
    while (it != blues.end() and it2 != reds.end()) {
        auto best = reds.end();
        while (it2 != reds.end()) {
            if (is_intersect(*it, *it2))
                best = it2;
            else if (it2->first > it->second)
                break;
            ++it2;
        }
        if (best == reds.end())
            break;
        count++;
        do {
            ++it;
        }while (is_intersect(*it, *best) and it != blues.end());
    }
    if (it == blues.end())
        cout << count;
    else
        cout << -1;
    cout << endl;
}