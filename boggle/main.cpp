#include <ctime>
#include <cstdlib>
#include "boggle_solver.h"
using namespace std;

int main() {
    clock_t start = clock();

    srand(time(nullptr));
    while (true) {
        BoggleBoard board;
        BoggleSolver solver("../input/dictionary-yawl.txt");
        int score = 0;
        for (auto& word: solver.getAllWords(board))
            score += solver.scoreOf(word);
        if (score == 20) {
            cout << board.toString() << endl;
            break;
        }
    }

    cout << (double)(clock() - start) / CLOCKS_PER_SEC << endl;
    return 0;
}