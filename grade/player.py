import bisect
from functools import reduce


__all__ = ['Player']


class Suit:
    Heart = 'h'
    Spade = 's'
    Diamond = 'd'
    Club = 'c'
    King = 'j'
    All = 'hsdcj'


VALUE = "234567890JQKA"
KING = 'kK'


def comp(suit, value):
    if suit == Suit.King:
        value -= 100
        return ('j' if value == 0 else 'J') + KING[value]
    else:
        return suit.upper() + VALUE[value]


def decomp(card):
    suit = card[0].lower()
    if suit == Suit.King:
        value = KING.index(card[1]) + 100
    else:
        value = VALUE.index(card[1])
    return suit, value


class Player:

    def __init__(self, role):
        self.__cards = dict()
        self._round = 0
        self.__main_value = self.__main_color = None

    def _add_card(self, suit, value):
        if self.__main_value == value:
            cards = self.__cards[Suit.King]
        else:
            cards = self.__cards[suit]
        bisect.insort(cards, (value, suit))

    def _snatch(self):
        if self.__main_color is None:
            score = 0
            _suit = None
            for _, s in self.__cards[Suit.King]:
                if s != Suit.King:
                    tmp_score = self.evaluate(self.__cards[s])
                    if tmp_score > score:
                        score = tmp_score
                        _suit = s
            if self._round == 0 and _suit is not None or score >= 50:
                return comp(_suit, self.__main_value)
        return ""

    def add_card_and_is_snatch(self, current_card):
        """
        摸牌并抢庄
        :param current_card: str, 现在摸到的牌，长度为2
        :return: str, 抢庄的牌
        """
        suit, value = decomp(current_card)
        self._add_card(suit, value)
        return self._snatch()

    def add_left_cards(self, left_cards):
        """
        拿底牌并埋牌
        :param left_cards: list of str, 底牌
        :return: list of str, 埋牌
        """
        size = len(left_cards)
        score = [VALUE.index(c) for c in '50K']
        for card in left_cards:
            suit, value = decomp(card)
            self._add_card(suit, value)
        left_cards.clear()

        tmp_cards = [cards for suit, cards in self.__cards.items() if suit != self.__main_color and suit != Suit.King]
        tmp_cards.sort(key=lambda x: len(x))
        tmp_cards.append(self.__cards[self.__main_color])
        tmp_cards.append(self.__cards[Suit.King])

        for cards in tmp_cards:
            for value, suit in cards.copy():
                if value not in score:
                    cards.remove((value, suit))
                    left_cards.append(comp(suit, value))
                    if len(left_cards) >= size:
                        return left_cards

    def finish_one_round(self, current_turn_out_cards, turn):
        """
        一轮出牌结束，4个玩家的出牌信息
        :param current_turn_out_cards: list of (order, role, card), 本轮出牌
        :param turn: 第几个出牌
        :return: None
        """
        pass

    def set_main_value(self, main_value):
        """
        设置主牌面值
        :param main_value: char, 主牌面值
        :return: None
        """
        self.__main_value = VALUE.index(main_value)

    def set_main_color(self, main_color):
        """
        设置主牌花色
        :param main_color: char, 主牌花色
        :return: None
        """
        self.__main_color = main_color.lower()
        self.__cards[Suit.King].sort(key=lambda card: card[0] + (10 if card[1] == self.__main_color else 0))

    def player_init(self):
        """
        开始一局新的游戏，初始化相关变量
        :return: None
        """
        self._round += 1
        self.__cards = dict()
        for suit in Suit.All:
            self.__cards[suit] = []
        self.__main_color = None

    def play_out_cards(self, turn, current_turn_out_cards):
        """
        出牌
        :param turn: int, 第几个出牌
        :param current_turn_out_cards: 本轮已出的牌
        :return: str, 玩家出的牌
        """
        return ""

    def show_cards(self):
        """
        查看手里的所有牌
        :return: list of str, 玩家手里的所有牌
        """
        return [comp(suit, value) for cards in self.__cards.values() for value, suit in cards]

    def add_used_cards(self, current_card_info):
        """
        某个玩家将一张牌放入弃牌堆
        :param current_card_info: pair of (who, card)
        :return: None
        """
        pass

    def calculate_score(self, current_cards):
        """
        统计分数
        :param current_cards: list of str, 得分的牌
        :return: int, 非庄家的得分
        """
        return 0

    def evaluate(self, cards):
        return len(cards) * 10 + reduce(lambda a, b: a + b, map(lambda x: x[0], cards), 0)

