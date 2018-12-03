import bisect
from functools import reduce


__all__ = ['Player']
VALUE = "234567890JQKA"
KING = 'kK'


class Card:
    Heart = 'h'
    Spade = 's'
    Diamond = 'd'
    Club = 'c'
    King = 'j'
    All = 'hsdcj'

    score = [VALUE.index(c) for c in '50K']

    @staticmethod
    def comp(suit, value):
        if suit == Card.King:
            value -= 100
            return ('j' if value == 0 else 'J') + KING[value]
        else:
            return suit.upper() + VALUE[value]

    @staticmethod
    def decomp(card):
        suit = card[0].lower()
        if suit == Card.King:
            value = KING.index(card[1]) + 100
        else:
            value = VALUE.index(card[1])
        return suit, value

    @staticmethod
    def bigger(asuit, avalue, bsuit, bvalue, main_suit):
        if asuit == bsuit:
            return avalue >= bvalue
        elif asuit == main_suit:
            return bsuit != Card.King
        else:
            return False


class Player:

    def __init__(self, role):
        self.__cards = dict()
        self.__round = 0
        self.__main_value = self.__main_color = None
        self.__used_cards = dict()

    def _add_card(self, suit, value):
        if self.__main_value == value or suit == Card.King:
            if self.__main_color is None:
                cards = self.__cards[Card.King]
            else:
                cards = self.__cards[self.__main_color]
        else:
            cards = self.__cards[suit]
        bisect.insort(cards, (value, suit))

    @staticmethod
    def _evaluate(cards):
        return len(cards) * 10 + reduce(lambda a, b: a + b, map(lambda x: x[0], cards), 0)

    def _snatch(self):
        if self.__main_color is None:
            score = 0
            _suit = None
            for _, s in self.__cards[Card.King]:
                if s != Card.King:
                    tmp_score = self._evaluate(self.__cards[s])
                    if tmp_score > score:
                        score = tmp_score
                        _suit = s
            if self.__round == 0 and _suit is not None or score >= 50:
                return Card.comp(_suit, self.__main_value)
        return ""

    def add_card_and_is_snatch(self, current_card):
        """
        摸牌并抢庄
        :param current_card: str, 现在摸到的牌，长度为2
        :return: str, 抢庄的牌
        """
        suit, value = Card.decomp(current_card)
        self._add_card(suit, value)
        return self._snatch()

    def _cards_view(self):
        tmp_cards = [cards for suit, cards in self.__cards.items() if suit != self.__main_color]
        tmp_cards.sort(key=lambda x: len(x))
        tmp_cards.append(self.__cards[self.__main_color])
        return tmp_cards

    def _choice_bottom_cards(self, size):
        tmp_cards = self._cards_view()
        left_cards = []

        i = 0
        while i < len(tmp_cards) and len(left_cards) < size:
            cards = tmp_cards[i]
            j = 0
            length = len(cards)
            while j < length:
                value, suit = cards[j]
                if value < VALUE.index('K') and (value not in Card.score or length < 3):
                    cards.remove((value, suit))
                    left_cards.append(Card.comp(suit, value))
                    break
                else:
                    j += 1
            else:
                i += 1
        return left_cards

    def add_left_cards(self, left_cards):
        """
        拿底牌并埋牌
        :param left_cards: list of str, 底牌
        :return: list of str, 埋牌
        """
        size = len(left_cards)
        for card in left_cards:
            suit, value = Card.decomp(card)
            self._add_card(suit, value)
        left_cards.clear()
        return self._choice_bottom_cards(size)

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
        self.__cards[Card.King].sort(key=lambda card: card[0] + (10 if card[1] == self.__main_color else 0))
        self.__cards[self.__main_color].extend(self.__cards[Card.King])
        del self.__cards[Card.King]

    def player_init(self):
        """
        开始一局新的游戏，初始化相关变量
        :return: None
        """
        self.__round += 1
        self.__used_cards = dict()
        self.__cards = dict()
        for suit in Card.All:
            self.__cards[suit] = []
            if suit != Card.King:
                self.__used_cards[suit] = []
        self.__main_color = None

    def eval_risk(self, suit, value):
        if suit == Card.King:
            return (value == 101) / 54
        elif suit == self.__main_color:
            return (12 + 2 - value) / 54
        else:
            return (13 + 2 + 12 - value) / 54

    def get_consider_cards(self, cards_list):
        considers = []
        cur_risk = 1 / 54
        while not considers and cur_risk <= 1:
            for cards in cards_list:
                if cards:
                    value, s = cards[-1]
                    risk = self.eval_risk(s, value)
                    if risk <= cur_risk:
                        bisect.insort(considers, (risk, s, value))
            cur_risk += 5 / 54
        return considers

    def get_cards(self, suit, value=None):
        if suit == Card.King or value == self.__main_value:
            suit = self.__main_color
        return self.__cards[suit]

    def _play_out_bigger(self, suit, value):
        suit_cards = self.get_cards(suit)
        pos = bisect.bisect_right(suit_cards, (value, suit))
        if 0 <= pos < len(suit_cards):  # 有比对手更大的同花色
            value, suit = suit_cards[pos]
            return suit, value
        elif suit_cards:  # 大不起大不起
            value, suit = suit_cards[0]
            return suit, value
        else:
            if suit == self.__main_color:   # 没有主花色了，随便出
                return self._play_out_not_score()
            else:
                suit_cards = self.get_cards(self.__main_color)
                if suit_cards:
                    value, suit = suit_cards[0]
                    return suit, value
                else:
                    return self._play_out_not_score()

    def _play_out_not_score(self):
        tmp_cards = self._cards_view()
        # 优先出不是分的牌
        for cards in tmp_cards:
            for value, suit in cards:
                if value not in Card.score:
                    return suit, value
        # 居然剩下的全是分，出第一张
        for cards in tmp_cards:
            for value, suit in cards:
                return suit, value
        raise Exception("_play_out_not_score")

    def _play_out_score(self, suit):
        suit_cards = self.get_cards(suit)
        for value, s in reversed(suit_cards):
            if value in Card.score:
                return s, value
        for value, s in suit_cards:
            return s, value
        tmp_cards = self._cards_view()
        for cards in tmp_cards:
            for value, s in cards:
                if value in Card.score:
                    return s, value
        for cards in tmp_cards:
            for value, s in cards:
                return s, value
        raise Exception("_play_out_score")

    def _play(self, suit, value):
        self.get_cards(suit, value).remove((value, suit))
        self._add_used_cards(suit, value)
        return Card.comp(suit, value)

    def play_out_cards(self, turn, current_turn_out_cards):
        """
        出牌
        :param turn: int, 第几个出牌
        :param current_turn_out_cards: 本轮已出的牌
        :return: str, 玩家出的牌
        """
        if turn == 0:
            considers = self.get_consider_cards([cards for suit, cards in self.__cards.items() if suit != self.__main_color])
            if not considers:
                considers = self.get_consider_cards([self.__cards[self.__main_color]])
            risk, suit, value = considers[0]
            return self._play(suit, value)
        else:
            turn_cards = []
            for card in current_turn_out_cards:
                d_card = Card.decomp(card)
                self._add_used_cards(*d_card)
                turn_cards.append(d_card)
            suit, value = turn_cards[0]
            if turn == 1:
                return self._play(*self._play_out_bigger(suit, value))
            elif turn == 2:
                opp_suit, opp_value = turn_cards[1]
                if Card.bigger(suit, value, opp_suit, opp_value, self.__main_color):
                    return self._play(*self._play_out_score(suit))
                else:
                    return self._play(*self._play_out_bigger(opp_suit, opp_value))
            else:
                fri_suit, fri_value = turn_cards[1]
                opp2_suit, opp2_value = turn_cards[2]
                res1 = not Card.bigger(suit, value, fri_suit, fri_value, self.__main_color)
                res2 = Card.bigger(fri_suit, fri_value, opp2_suit, opp2_value, self.__main_color)
                if res1 and res2:
                    return self._play(*self._play_out_score(suit))
                else:
                    if res1:
                        return self._play(*self._play_out_bigger(opp2_suit, opp2_value))
                    if res2:
                        return self._play(*self._play_out_bigger(suit, value))
                    if Card.bigger(suit, value, opp2_suit, opp2_value, self.__main_color):
                        return self._play(*self._play_out_bigger(suit, value))
                    else:
                        return self._play(*self._play_out_bigger(opp2_suit, opp2_value))

    def show_cards(self):
        """
        查看手里的所有牌
        :return: list of str, 玩家手里的所有牌
        """
        return [Card.comp(suit, value) for cards in self.__cards.values() for value, suit in cards]

    def _add_used_cards(self, suit, value):
        """
        将一张牌放入弃牌堆
        :param suit, value: 一张牌
        :return: None
        """
        tmp_suit = suit
        if value >= 100:
            tmp_suit = self.__main_color
        card = (value, suit)
        bisect.insort(self.__used_cards[tmp_suit], card)

    def set_role(self, role):
        pass
