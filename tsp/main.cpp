#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <algorithm>
#include <climits>
#include <ctime>
using namespace std;

#define INF INT_MAX


vector<int> rowReduce(vector<vector<int>>& reduced_matrix) {
    size_t n = reduced_matrix.size();
    vector<int> row(n, INF);
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) {
            int tmp = reduced_matrix[i][j];
            if (tmp < row[i])
                row[i] = tmp;
        }
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (reduced_matrix[i][j] != INF) {
                if (row[i] != INF)
                    reduced_matrix[i][j] -= row[i];
            }
        }
    }
    return row;
}

vector<int> colReduce(vector<vector<int>>& reduced_matrix) {
    size_t n = reduced_matrix.size();
    vector<int> col(n, INF);
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) {
            int tmp = reduced_matrix[i][j];
            if (tmp < col[j])
                col[j] = tmp;
        }
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (reduced_matrix[i][j] != INF) {
                if (col[j] != INF)
                    reduced_matrix[i][j] -= col[j];
            }
        }
    }
    return col;
}

int calCost(vector<vector<int>>& reduced_matrix) {
    int cost = 0;
    for (int i: rowReduce(reduced_matrix)) {
        if (i != INF)
            cost += i;
    }
    for (int i: colReduce(reduced_matrix)) {
        if (i != INF)
            cost += i;
    }
    return cost;
}

struct Node {
    vector<pair<int, int>> path;
    vector<vector<int>> reduced_matrix;

    int lower_bound;
    int vertex;
    int level;

    Node(vector<vector<int>> parent_matrix,
         vector<pair<int, int>> p,
         int l, int i, int j, int cost=0)
         : path(std::move(p)), reduced_matrix(std::move(parent_matrix)),
         vertex(j), level(l) {
        size_t n = reduced_matrix.size();
        if (level != 0) {
            path.emplace_back(make_pair(i, j));
            for (int k = 0; k < n; ++k) {
                reduced_matrix[i][k] = INF;
                reduced_matrix[k][j] = INF;
            }
        }
        reduced_matrix[j][0] = INF;
        lower_bound = cost + calCost(reduced_matrix);
    }
};

pair<int, vector<int>> solve(vector<vector<int>>& cost_matrix) {
    vector<int> res;
    int cost = INF;

    auto pred = [](Node* a, Node* b) {
        return a->lower_bound > b->lower_bound;
    };
    priority_queue<Node*, vector<Node*>, decltype(pred)> pq(pred);

    vector<pair<int, int>> path;
    Node *root = new Node(cost_matrix, path, 0, -1, 0);

    pq.push(root);
    size_t n = cost_matrix.size();
    while (!pq.empty()) {
        Node *best = pq.top();
        pq.pop();

        int i = best->vertex;
        if (best->level == n - 1) {
            res.push_back(best->path[0].first);
            for (auto p: best->path)
                res.push_back(p.second);
            cost = best->lower_bound;
            break;
        } else {
            for (int j = 0; j < n; ++j) {
                int w = best->reduced_matrix[i][j];
                if (w != INF) {
                    Node *child = new Node(best->reduced_matrix, best->path,
                            best->level + 1, i, j, best->lower_bound + w);
                    pq.push(child);
                }
            }
        }
        delete best;
    }
    return make_pair(cost, res);
}

int main() {
    int t = 4;
    string file = "../test0.txt";
    file[7] = '0' + t;
    ifstream fin(file);
    cin.rdbuf(fin.rdbuf());

    int n;
    cin >> n;
    vector<vector<int>> costMatrix(n, vector<int>(n, INF));
    int x;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> x;
            if (x) costMatrix[i][j] = x;
        }
    }

    clock_t start = clock();
    auto res = solve(costMatrix);
    clock_t end = clock();

    if (res.first == INF) {
        cout << "Cannot be solved!" << endl;
    } else {
        cout << res.first << endl;
        for (int i: res.second)
            cout << i << ' ';
        cout << 0 << endl;
    }
    cout << (double)(end - start) / CLOCKS_PER_SEC << endl;
    return 0;
}