import numpy as np

EMPTY = 0
BLACK = 1
WHITE = 2


def point(x, y):
    return np.asarray([x, y])


class ChessBoard:

    def __init__(self, N=15):
        self.__chess_borad = np.zeros((N, N), dtype=int)
        self._last_drop = None
        # 赢1，活四1，死四1，活三3，死三3，活二9，死二9，活一27，死一27
        self.__scores = [8**8, 8**7] + [8**7/1.5] * 4 + [8**7/4.5] * 3 + \
                        [8**7/9] * 9 + [8**7/13] * 9 + \
                        [8**7/16] * 27 + [8**7/15] * 27

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
                    head += ("\033[32;0m" + form) % self.__chess_borad[i][j]
                else:
                    head += ("\033[0m" + form) % self.__chess_borad[i][j]
        return head

    def __len__(self):
        return self.__chess_borad.shape[0]

    def get_at(self, i, j):
        if 0 <= i < len(self) and 0 <= j < len(self):
            return self.__chess_borad[i][j]
        else:
            return None

    def set_at(self, i, j, x):
        if 0 <= i < len(self) and 0 <= j < len(self):
            self.__chess_borad[i][j] = x
            self._last_drop = point(i, j)

    @property
    def directions1(self):
        return [point(0, -1), point(-1, 0), point(-1, -1), point(-1, 1)]

    @property
    def directions2(self):
        d1 = self.directions1
        return [-d for d in d1]

    @staticmethod
    def get_next_turn(who):
        if who == BLACK:
            return WHITE
        else:
            return BLACK

    def _evaluate(self, i, j, who):
        score = 0
        opposite = self.get_next_turn(who)
        p = point(i, j)
        for direction in self.directions1 + self.directions2:
            lines = [self.get_at(*(p + direction * t)) for t in range(1, 5)]
            power = 1
            number = 0
            for x in reversed(lines):
                if x is None or x == opposite:
                    x = 2
                elif x == EMPTY:
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
        n = len(self)
        for i in range(n):
            for j in range(n):
                if self.get_at(i, j) == EMPTY:
                    score = self._evaluate(i, j, who)
                    if score > score_best:
                        score_best = score
                        i_best, j_best = i, j
        return score_best, i_best, j_best

    def decide_next_pos(self, who):
        # 进攻
        s1, i1, j1 = self._decide(who)
        who = self.get_next_turn(who)
        # 防守
        s2, i2, j2 = self._decide(who)
        if s2 > s1:
            s1, i1, j1 = s2, i2, j2
        return i1, j1

    def _count_on_direction(self, i, j, x_dir, y_dir, color):
        count = 0
        for step in range(1, 5):  # 除当前位置外,朝对应方向再看4步
            x = self.get_at(i + x_dir * step, j + y_dir * step)
            if x == color:
                count += 1
            else:
                break
        return count

    def have_five(self, i, j, color):
        # 四个方向计数 上 左 左上 右上
        for x_dir, y_dir in self.directions1:
            axis_count = self._count_on_direction(i, j, x_dir, y_dir, color)
            if axis_count >= 4:
                return True
        return False

    def check(self):
        n = len(self)
        for i in range(4, n):
            for j in range(n):
                color = self.get_at(i, j)
                if color != EMPTY and self.have_five(i, j, color):
                    return color
        return EMPTY


if __name__ == '__main__':
    chess = ChessBoard(15)
    win = EMPTY
    turns = [BLACK, WHITE]
    colors = ["Black", "White"]
    index = 0
    inputs = iter([(5, 1), (5, 6),
                   (4, 2), (4, 6),
                   (3, 3), (3, 6),
                   (2, 4), (2, 6),
                   (1, 5), (1, 6)])
    print(chess)
    while win == EMPTY:
        if turns[index] == BLACK:
            while True:
                try:
                    i, j = map(int, input("Your turn: ").split())
                    x = chess.get_at(i, j)
                    if x == EMPTY:
                        break
                except Exception:
                    pass
                print("invalid")
        else:
            i, j = chess.decide_next_pos(WHITE)
        chess.set_at(i, j, turns[index])
        print(chess)
        win = chess.check()
        index = int(not index)
    print(colors[win - 1])
