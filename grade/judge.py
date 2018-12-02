# coding:utf-8

import random
import time
import player as p1
import player as p2
import player as p3
import player as p4


# H S D C
# Heart Spade Diamond Club
# jk small king, JK big king

class Judge:

    def __init__(self):
        self.cards = None
        self.players = []
        self.players.append(p1.Player('East'))
        self.players.append(p2.Player('North'))
        self.players.append(p3.Player('West'))
        self.players.append(p4.Player('South'))

        self.level = [2, 2]

        self.master = None

        self.false = [0, 0, 0, 0]  # 记录每个人犯错次数

        self.main_color = None
        self.main_num = 2

        self.loser = 0  # 记录先犯错的一方，最后判输

        self.point = 0
        self.biggest = [0, 0, 0, 0]
        self.bottom = None

    @staticmethod
    def covert(s):
        if s == 1 or s == 14:
            return 'A'
        elif s < 10:
            return str(s)
        elif s == 10:
            return '0'
        elif s == 11:
            return 'J'
        elif s == 12:
            return 'Q'
        elif s == 13:
            return 'K'

    # 新游戏，初始化
    def new_game(self):
        self.main_color = None
        self.false = [0, 0, 0, 0]
        self.loser = -1
        self.bottom = []
        self.point = 0
        self.biggest = [0, 0, 0, 0]

        for y in self.players:
            # y.initial_new_game()

            y.set_main_value(self.covert(self.main_num))

        cards = self.create_card()
        random.shuffle(cards)
        for i in range(4):
            self.players[i].player_init()

        # 发牌
        turn = 0
        for i in range(48):
            x = self.players[turn].add_card_and_is_snatch(cards[i])
            if x != '' and x[1] == self.covert(self.main_num) and self.main_color is None:
                self.main_color = x[0]
                if self.master is None:
                    self.master = turn
                for y in self.players:
                    y.set_main_color(self.main_color)
            elif x == '':
                pass
            else:
                self.false[turn] += 1
                if self.loser == -1:
                    self.loser = turn
            # background.add_card(cards[i], turn)
            turn += 1
            turn %= 4
        if self.main_color is None:
            col = ['H', 'C', 'D', 'S']
            self.main_color = random.choice(col)
            for y in self.players:
                y.set_main_color(self.main_color)
        if self.master is None:
            self.master = random.randint(0, 3)
        self.bottom = self.players[self.master].add_left_cards(cards[48:])
        if len(self.bottom) != 6:
            self.false[self.master] += 1
            if self.loser == -1:
                self.loser = self.master
        # background.add_cards_over(self.main_color, self.master)

    @staticmethod
    def create_card():
        """生成一副牌"""
        colors = ['H', 'S', 'D', 'C']
        nums = 'A234567890JQK'
        cards = []
        for color in colors:
            for i in range(13):
                c = color + nums[i]
                cards.append(c)
        cards.append('jk')
        cards.append('JK')
        return cards

    # 判断玩家手里是否有该花色的牌，y表示该轮是否要出主牌
    def find_color(self, p_cards, this_color, y):
        for x in p_cards:
            if y:
                if x == this_color or x == 'jk' or x == 'JK' or x == self.main_num:
                    return True
            else:
                if x == this_color:
                    return True
        return False

    # a先出， 判断b的数字是否大于a
    @staticmethod
    def is_big(b, a):
        num_order = ['A', 'K', 'Q', 'J', '0', '9', '8', '7', '6', '5', '4', '3', '2']
        for x in num_order:
            if x == a:
                return False
            if x == b:
                return True

    # 判断a 是否大于b，a先出
    def is_bigger(self, a, b, this_color):
        if a == 'JK':
            return True
        if a == 'jk':
            if b == 'JK':
                return False
            else:
                return True
        if a[1] == self.main_num:
            if b == 'jk' or b == 'JK' or b[0] == self.main_color and b[1] == self.main_num:
                return False
            else:
                return True
        if a[0] == self.main_color:
            if b == 'jk' or b == 'JK' or b[1] == self.main_num or b[0] == self.main_color and self.is_big(b[1], a[1]):
                return False
            else:
                return True
        if a[0] == this_color:
            if b == 'jk' or b == 'JK' or b[1] == self.main_num or \
                    b[0] == self.main_color or b[0] == this_color and self.is_big(b[1], a[1]):
                return False
            else:
                return True

        if b == 'jk' or b == 'JK' or b[1] == self.main_num or b[0] == self.main_color or \
                b[0] == this_color or self.is_big(b[1], a[1]):
            return False
        else:
            return True

    def add_points(self, cards):
        for x in cards:
            if x[1] == '5':
                self.point += 5
            elif x[1] == '0' or x[1] == 'K':
                self.point += 10

    # 判断一轮中最大的牌是谁出的，是否加分
    def get_max_index_and_add_points(self, cards, turn, this_color):
        index = 0
        max_card = cards[0]
        for i in range(1, 4):
            if not self.is_bigger(max_card, cards[i], this_color):
                index = i
                max_card = cards[i]

        if index % 2 != self.master % 2:
            self.add_points(cards)

        return (turn + index) % 4

    @staticmethod
    def is_a_card(s):
        if s == 'jk' or s == 'JK':
            return True
        if s[0] in ['H', 'S', 'D', 'C'] and s[1] in ['A', 'K', 'Q', 'J', '0', '9', '8', '7', '6', '5', '4', '3', '2']:
            return True
        else:
            return False

    # 出牌到结束
    def run_game(self):
        turn = self.master
        for i in range(12):
            # UI.check_events()
            this_turn_cards = []
            first_card = self.players[turn].play_out_cards(0, this_turn_cards)
            this_turn_cards.append(first_card)

            # background.push_cards([first_card], turn)

            turn += 1
            turn %= 4

            if not self.is_a_card(first_card):
                print('Please input a card')
                self.false[turn] += 1
            if first_card == 'jk' or first_card == 'JK' or first_card[0] == self.main_color or \
                    first_card[1] == self.main_num:
                this_color = self.main_color
            else:
                this_color = first_card[0]

            for j in range(1, 4):
                a_cards = self.players[turn].play_out_cards(j, this_turn_cards)
                this_turn_cards.append(a_cards)
                p_cards = self.players[turn].show_cards()
                if a_cards[0] == this_color:
                    pass
                elif this_color == self.main_color:
                    if a_cards == 'jk' or a_cards == 'JK' or a_cards[1] == self.main_num:
                        pass
                    elif not self.find_color(p_cards, this_color, True):
                        pass
                    else:
                        self.false[turn] += 1
                        if self.loser == -1:
                            self.loser = turn
                else:
                    if self.find_color(p_cards, this_color, False):
                        self.false[turn] += 1
                        if self.loser == -1:
                            self.loser = turn

                # background.push_cards([a_cards], turn)

                turn += 1
                turn %= 4

            # 告诉所有玩家本轮出的牌
            for ii in range(4):
                self.players[ii].finish_one_round(this_turn_cards, (ii + turn) % 4)
            print(this_turn_cards)
            print()
            for p in self.players:
                print(p.show_cards())

            max_index = self.get_max_index_and_add_points(this_turn_cards, turn, this_color)
            turn = max_index
            self.biggest[max_index] += 1

            # background.update_point(self.point, self.level[0], self.level[1])
            # background.turn_over()

        # 底牌是否得分
        if turn % 2 != self.master % 2:
            self.add_points(self.bottom)

        if self.loser % 2 == self.master:
            self.main_num = self.level[(self.master + 1) % 2]
            self.master = (self.master + 1) % 2
        elif self.loser % 2 != self.master and self.loser != -1:
            self.level[self.master % 2] += 1
            self.main_num = self.level[self.master % 2]
            if self.master == self.master % 2:
                self.master += 2
            else:
                self.master %= 2
        elif self.point < 40:
            self.level[self.master % 2] += 1
            self.main_num = self.level[self.master % 2]
            if self.master == self.master % 2:
                self.master += 2
            else:
                self.master %= 2
        else:
            self.main_num = self.level[(self.master + 1) % 2]
            self.master = (self.master + 1) % 2
        # print(self.biggest)


if __name__ == '__main__':
    # Initialize pygame
    # pygame.init()
    # setting = UI.Setting()

    # SCREEN_WIDTH, SCREEN_HEIGHT = setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT
    # x, y = 150, 60
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # pygame.display.set_caption("升级")
    #
    # background = UI.Background(screen, setting)
    judge = Judge()
    while True:
        judge.new_game()
        for p in judge.players:
            print(p.show_cards())
        print(judge.master, judge.main_color)
        judge.run_game()
        # background.initial()

        if judge.level[0] == 13 or judge.level[1] == 13:
            break
    print(judge.level)
