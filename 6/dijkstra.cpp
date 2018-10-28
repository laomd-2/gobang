//
// Created by laomd on 2018/10/28.
//

#include <iostream>
#include <map>
#include <vector>
#include <algorithm>
using namespace std;

#ifndef INT_MAX
#define INT_MAX 2147483647
#endif

typedef vector<vector<int>> Graph;

int dijkstra(Graph& graph, int src, int dst) {
    size_t n = graph.size();
    vector<int> distance(n, INT_MAX);
    vector<int> num_shortest(n, 0);
    distance[src] = 0;
    num_shortest[src] = 1;

    vector<int> best;
    best.emplace_back(src);
    vector<int> visited(n, 0);
    while (!best.empty()) {
        sort(best.begin(), best.end(), [&](int a, int b) {
            return distance[a] >= distance[b];
        });
        int v = best.back();
        if (v == dst)
            break;
        best.pop_back();
        visited[v] = 1;

        int dis = distance[v];
        for (int neighbor = 0; neighbor < n; neighbor++) {
            if (graph[v][neighbor] && !visited[neighbor]) {
                int old_w = distance[neighbor];
                int new_w = dis + graph[v][neighbor];

                if (new_w < old_w) {
                    distance[neighbor] = new_w;
                    num_shortest[neighbor] = 1;
                    best.emplace_back(neighbor);
                } else if (new_w == old_w) {
                    num_shortest[neighbor]++;
                }
            }
        }
    }
    return num_shortest[dst];
}

int main() {
    int n, m;
    cin >> n >> m;
    Graph graph(n, vector<int>(n, 0));

    int a, b, w;
    while (m--) {
        cin >> a >> b;
        graph[a - 1][b - 1] = graph[b - 1][a - 1] = 1;
    }

    cin >> n >> m;
    cout << dijkstra(graph, n - 1, m - 1) << endl;
    return 0;
}