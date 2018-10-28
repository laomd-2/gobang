//
// Created by laomd on 2018/10/22.
//

#include <iostream>
#include <vector>
#include <queue>
#include <climits>
using namespace std;

int find_cost(const vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    vector<vector<int>> cost(m, vector<int>(n, INT_MAX));
    cost[m - 1][n - 1] = grid[m - 1][n - 1];

    queue<pair<int, int>> points;
    points.push(make_pair(m - 1, n - 1));
    while (!points.empty()) {
        pair<int, int> p = points.front();
        points.pop();
        int i = p.first, j = p.second;
        if (i > 0) {
            cost[i - 1][j] = min(cost[i - 1][j], cost[i][j] + grid[i - 1][j]);
            points.push(make_pair(i - 1, j));
        }
        if (j > 0) {
            cost[i][j - 1] = min(cost[i][j - 1], cost[i][j] + grid[i][j - 1]);
            points.push(make_pair(i, j - 1));
        }
    }
    return cost[0][0];
}
int main() {
    int m, n;
    cin >> m >> n;

    vector<vector<int>> grid(m, vector<int>(n, 0));

    int x;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            cin >> x;
            grid[i][j] = x;
        }
    cout << find_cost(grid) << endl;
    return 0;
}