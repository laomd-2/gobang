//
// Created by laomd on 2018/12/17.
//

#ifndef BOGGLE_BOARD_SOLVER_H
#define BOGGLE_BOARD_SOLVER_H

#include <string>
#include <set>
#include <vector>
#include "board.h"
#include "trie.h"
using namespace std;

class BoggleSolver {
public:
    // Initializes the data structure using the given array of strings as the dictionary.
    // (You can assume each word in the dictionary contains only the uppercase letters A through Z.)
    explicit BoggleSolver(string dictionary_file);

    // Returns the set of all valid words in the given Boggle board, as an Iterable.
    set<string> getAllWords(const BoggleBoard& board);

    // Returns the score of the given word if it is in the dictionary, zero otherwise.
    // (You can assume the word contains only the uppercase letters A through Z.)
    int scoreOf(string word);
private:
    template <typename InputIter>
    void buildTrie(InputIter first, InputIter last);

    void dfs(const BoggleBoard& board, int i, int j, string prefix, TrieNode* node,
            set<string>& all_words, vector<vector<int>>&);

    TrieNode root;
};


#endif //BOGGLE_BOARD_SOLVER_H
