//
// Created by laomd on 2018/12/17.
//

#ifndef BOGGLE_BOARD_H
#define BOGGLE_BOARD_H

#include <string>
#include <vector>
using namespace std;

class BoggleBoard
{
public:
    // Initializes a random 4-by-4 Boggle board.
    // (using the frequency of letters in the English language)
    BoggleBoard();

    // Initializes a Boggle board from the specified filename.
    explicit BoggleBoard(string filename);

    // Returns the number of rows.
    int rows();

    // Returns the number of columns.
    int cols();

    // Returns the letter in row i and column j.
    // (with 'Q' representing the two-letter sequence "Qu")
    char getLetter(int i, int j);

private:
    vector<string> _board;
};


#endif //BOGGLE_BOARD_H
