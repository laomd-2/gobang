import numpy as np


def point(x, y):
    return np.asarray([x, y])


class ChessBoard:
    EMPTY = 0
    PLAYER = 1
    COMPUTER = 2

    up_half_direction = (point(0, -1), point(-1, 0), point(-1, -1), point(-1, 1))
    down_half_direction = (point(0, 1), point(1, 0), point(1, 1), point(1, -1))

    def __init__(self, n=15):
        self.__chess_board = np.zeros((n, n), dtype=int)
        self._last_drop = None

    def __str__(self):
        form = "%-3d"
        head = "  |"
        for i in range(len(self)):
            head += form % i
        head += '\n' + '-' * len(head)
        for i in range(len(self)):
            head += '\n' + "%-2d" % i + '|'
            for j in range(len(self)):
                if self._last_drop is not None and \
                        i == self._last_drop[0] and \
                        j == self._last_drop[1]:
                    head += ("\033[32;0m" + form) % self.__chess_board[i][j]
                else:
                    head += ("\033[0m" + form) % self.__chess_board[i][j]
        return head

    def __len__(self):
        return self.__chess_board.shape[0]

    @staticmethod
    def get_opposite(who):
        if who == ChessBoard.PLAYER:
            return ChessBoard.COMPUTER
        else:
            return ChessBoard.PLAYER

    def get_chess_at(self, i, j):
        if 0 <= i < len(self) and 0 <= j < len(self):
            return self.__chess_board[i][j]
        else:
            return None

    def drop_chess_at(self, i, j, x):
        if 0 <= i < len(self) and 0 <= j < len(self):
            self.__chess_board[i][j] = x
            self._last_drop = point(i, j)

    def check_winner(self):
        n = len(self)
        for i in range(4, n):
            for j in range(n):
                color = self.get_chess_at(i, j)
                if color != ChessBoard.EMPTY and self._have_five(i, j, color):
                    return color
        return ChessBoard.EMPTY

    def _count_on_direction(self, i, j, x_dir, y_dir, color):
        count = 0
        for step in range(1, 5):  # 除当前位置外,朝对应方向再看4步
            x = self.get_chess_at(i + x_dir * step, j + y_dir * step)
            if x == color:
                count += 1
            else:
                break
        return count

    def _have_five(self, i, j, color):
        # 四个方向计数 上 左 左上 右上
        for x_dir, y_dir in self.up_half_direction:
            axis_count = self._count_on_direction(i, j, x_dir, y_dir, color)
            if axis_count >= 4:
                return True
        return False
