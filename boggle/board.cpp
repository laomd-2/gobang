//
// Created by laomd on 2018/12/17.
//

#include <ctime>
#include <cstdlib>
#include <fstream>
#include "board.h"
using namespace std;

static const char* dice16[4][4] = {
        {"LRYTTE", "VTHRWE", "EGHWNE", "SEOTIS"},
        {"ANAEEG", "IDSYTT", "OATTOW", "MTOICU"},
        {"AFPKFS", "XLDERI", "HCPOAS", "ENSIEU"},
        {"YLDEVR", "ZNRNHL", "NMIQHU", "OBBAOJ"}
};

BoggleBoard::BoggleBoard() : _board(4) {
    for(int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            _board[i] += dice16[i][j][rand() % 6];
        }
    }
}

BoggleBoard::BoggleBoard(string filename) : _board(4) {
    ifstream fin(filename);
    for (auto& row: _board)
        getline(fin, row);
}

int BoggleBoard::rows() const {
    return 4;
}

int BoggleBoard::cols() const {
    return 4;
}

char BoggleBoard::getLetter(int i, int j) const {
    return _board[i][j];
}

string BoggleBoard::toString() const {
    string res;
    for (auto& s: _board) {
        res += s + '\n';
    }
    res.pop_back();
    return res;
}