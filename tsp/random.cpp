//
// Created by laomd on 2018/12/9.
//
#include <fstream>
#include <vector>
#include <ctime>
#include <cstdlib>
using namespace std;

int main() {
    for (int t = 0; t < 5; ++t) {
        int n = (t + 1) * 5;
        string file = "../test2.txt";
        file[7] = '0' + t;
        ofstream fout(file);
        fout << n << endl;

        vector<vector<int>> matrix(n, vector<int>(n));

        srand(time(nullptr));
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                matrix[i][j] = matrix[j][i] = rand() % 100;
            }
        }

        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                fout << matrix[i][j] << ' ';
            }
            fout << endl;
        }
    }
}