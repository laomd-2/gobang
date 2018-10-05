from chessboard import ChessBoard
from ai import AI

chessboard = ChessBoard(15)
computer = AI(chessboard)

win = ChessBoard.EMPTY
turns = (ChessBoard.PLAYER, ChessBoard.COMPUTER)
colors = ("Black", "White")
index = 0
print(chessboard)
while win == ChessBoard.EMPTY:
    if turns[index] == ChessBoard.PLAYER:
        while True:
            try:
                i, j = map(int, input("Your turn: ").split())
                x = chessboard.get_chess_at(i, j)
                if x == ChessBoard.EMPTY:
                    break
            except:
                pass
            print("invalid")
    else:
        i, j = computer.decide_next_pos(ChessBoard.COMPUTER)
    chessboard.drop_chess_at(i, j, turns[index])
    print(chessboard)
    win = chessboard.check_winner()
    index = int(not index)
print(colors[win - 1], "win!!!")
