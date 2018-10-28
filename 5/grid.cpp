#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <climits>
using namespace std;

string find_path(const vector<vector<int>> &grid) {
    int m = grid.size(), n = grid[0].size();
    vector<vector<int>> cost(m, vector<int>(n, INT_MAX));
    vector<vector<string>> path(m, vector<string>(n, ""));

    cost[m - 1][n - 1] = grid[m - 1][n - 1];

    queue<pair<int, int>> points;
    points.push(make_pair(m - 1, n - 1));
    while (!points.empty()) {
        pair<int, int> p = points.front();
        points.pop();
        int i = p.first, j = p.second;
        if (i > 0) {
            int new_cost = cost[i][j] + grid[i - 1][j];
            if (new_cost < cost[i - 1][j]) {
                cost[i - 1][j] = new_cost;
                path[i - 1][j] = "D" + path[i][j];
            }
            points.push(make_pair(i - 1, j));
        }
        if (j > 0) {
            int new_cost = cost[i][j] + grid[i][j - 1];
            if (new_cost < cost[i][j - 1]) {
                cost[i][j - 1] = new_cost;
                path[i][j - 1] = "R" + path[i][j];
            }
            points.push(make_pair(i, j - 1));
        }
    }
    return path[0][0];
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
    cout << find_path(grid) << endl;
    return 0;
}