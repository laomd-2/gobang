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
    bfs(&root);
}

set<string> BoggleSolver::getAllWords(BoggleBoard board) {
    set<string> all_words;
    dfs(0, 0, "", &root, all_words);
}

int BoggleSolver::scoreOf(string word) {
    int score = 0;
    for (char c: word) {
        score++;
        if (tolower(c) == 'q')
            score++;
    }
    return score;
}

template<typename InputIter>
void BoggleSolver::buildTrie(InputIter first, InputIter last) {
    while (first != last) {
        const string& word = *first;
        root.insert(word.begin(), word.end());
        ++first;
    }
}

void BoggleSolver::dfs(int i, int j, string prefix, TrieNode* node, set<string> &all_words) {

}

