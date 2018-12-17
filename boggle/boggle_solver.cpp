//
// Created by laomd on 2018/12/17.
//

#include <fstream>
#include <vector>
#include <iterator>
#include "boggle_solver.h"
using namespace std;

BoggleSolver::BoggleSolver(string dictionary_file) {
    ifstream fin(dictionary_file);
    buildTrie(istream_iterator<string>(fin), istream_iterator<string>());
//    bfs(&root);
}

set<string> BoggleSolver::getAllWords(const BoggleBoard& board) {
    set<string> all_words;
    vector<vector<int>> visited(board.rows(), vector<int>(board.cols()));
    for (int i = 0; i < board.rows(); ++i) {
        for (int j = 0; j < board.cols(); ++j) {
            dfs(board, i, j, "", &root, all_words, visited);
        }
    }
    return all_words;
}

int BoggleSolver::scoreOf(string word) {
    int len = 0;
    for (char c: word) {
        len++;
        if (tolower(c) == 'q')
            len++;
    }
    if (len > 7) return 11;
    else if (len > 6) return 5;
    else if (len > 5) return 3;
    else if (len > 4) return 2;
    else if (len > 2) return 1;
    else return 0;
}

template<typename InputIter>
void BoggleSolver::buildTrie(InputIter first, InputIter last) {
    while (first != last) {
        const string& word = *first;
        root.insert(word.begin(), word.end());
        ++first;
    }
}

void BoggleSolver::dfs(const BoggleBoard& board, int i, int j, string prefix, TrieNode* node,
        set<string> &all_words, vector<vector<int>>& visited) {
//    cout << prefix << endl;
    visited[i][j] = 1;
    char letter = board.getLetter(i, j);
    prefix += letter;

    bool is_word;
    TrieNode* child;
    tie(is_word, child) = node->get_child(letter);
    if (is_word)
        all_words.insert(prefix);

    if (child) {
        for (int k = -1; k < 2; ++k) {
            for (int l = -1; l < 2; ++l) {
                if (k == 0 && l == 0)
                    continue;
                int ii = i + k, jj = j + l;
                if (ii >= 0 && jj >= 0 && ii < board.rows() && jj < board.cols())
                    if (visited[ii][jj] == 0)
                        dfs(board, ii, jj, prefix, child, all_words, visited);
            }
        }
    }
    visited[i][j] = 0;
}

