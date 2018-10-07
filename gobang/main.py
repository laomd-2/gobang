import numpy as np
import sys
from chessboard import ChessBoard
from ai import AI

chess_board = np.zeros((15, 15), dtype=int)
chessboard = ChessBoard(chess_board)
computer = AI(chessboard)

win = ChessBoard.EMPTY
turns = (ChessBoard.FIRST, ChessBoard.SECOND)
colors = ("Black", "White")
index = 0

if sys.argv[1] == '1':
    me = ChessBoard.FIRST
else:
    me = ChessBoard.SECOND

while win == ChessBoard.EMPTY:
    if turns[index] != me:
        input("waiting...(press enter)")
        chess_board = np.loadtxt("chessboard.txt", dtype=int).T
        chessboard.set_chessboard(chess_board)
    else:
        i, j = computer.decide_next_pos(me)
        chessboard.drop_chess_at(i, j, me)
        chessboard.output("chessboard.txt")
    win = chessboard.check_winner()
    index = int(not index)
print(colors[win - 1], "win!!!")
