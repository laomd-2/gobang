from chessboard import ChessBoard, point


class AI:
    # 赢1，活四1，死四1，活三3，死三3，活二9，死二9，活一27，死一27
    __scores = [8 ** 8, 8 ** 7] + [8 ** 7 / 1.5] * 4 + [8 ** 7 / 4.5] * 3 + \
               [8 ** 7 / 9] * 9 + [8 ** 7 / 13] * 9 + \
               [8 ** 7 / 16] * 27 + [8 ** 7 / 15] * 27

    def __init__(self, chess_board):
        self.__chess_board = chess_board

    def decide_next_pos(self, who):
        # 进攻
        s1, i1, j1 = self._decide(who)
        who = ChessBoard.get_opposite(who)
        # 防守
        s2, i2, j2 = self._decide(who)
        if s2 > s1:
            s1, i1, j1 = s2, i2, j2
        return i1, j1

    def _evaluate(self, i, j, who):
        score = 0
        opposite = ChessBoard.get_opposite(who)
        p = point(i, j)
        for direction in ChessBoard.up_half_direction + ChessBoard.down_half_direction:
            lines = [self.__chess_board.get_chess_at(*(p + direction * t)) for t in range(1, 5)]
            power = 1
            number = 0
            for x in reversed(lines):
                if x is None or x == opposite:
                    x = 2
                elif x == ChessBoard.EMPTY:
                    x = 1
                else:
                    x = 0
                number += x * power
                power *= 3
            score += self.__scores[number]
        return score

    def _decide(self, who):
        i_best, j_best = 0, 0
        score_best = 0
        n = len(self.__chess_board)
        for i in range(n):
            for j in range(n):
                if self.__chess_board.get_chess_at(i, j) == ChessBoard.EMPTY:
                    score = self._evaluate(i, j, who)
                    if score > score_best:
                        score_best = score
                        i_best, j_best = i, j
        return score_best, i_best, j_best
