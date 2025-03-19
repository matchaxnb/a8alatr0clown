from __future__ import annotations
from enum import IntEnum


class CardSuit(IntEnum):
    """The different card suits that exist"""

    SPADE = 1
    HEART = 2
    CLUB = 3
    DIAMOND = 4

    @property
    def symbol(self):
        if self == CardSuit.CLUB:
            return "♣"
        elif self == CardSuit.SPADE:
            return "♠"
        elif self == CardSuit.DIAMOND:
            return "♦"
        elif self == CardSuit.HEART:
            return "♥"

    @classmethod
    def from_symbol(cls, symbol: str) -> CardSuit:
        map_symbols = {
            "♣": CardSuit.CLUB,
            "♠": CardSuit.SPADE,
            "♦": CardSuit.DIAMOND,
            "♥": CardSuit.HEART,
        }
        return map_symbols[symbol]


class CardRank(IntEnum):
    """The different ranks a card may have"""

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    @property
    def symbol(self):
        if self == CardRank.ACE:
            return "A"
        elif self == CardRank.KING:
            return "K"
        elif self == CardRank.QUEEN:
            return "Q"
        elif self == CardRank.JACK:
            return "J"
        else:
            return str(self.value)

    @classmethod
    def from_symbol(cls, symbol: str) -> CardRank:
        map_symbols = {
            "A": CardRank.ACE,
            "K": CardRank.KING,
            "Q": CardRank.QUEEN,
            "J": CardRank.JACK,
            "10": CardRank.TEN,
            "9": CardRank.NINE,
            "8": CardRank.EIGHT,
            "7": CardRank.SEVEN,
            "6": CardRank.SIX,
            "5": CardRank.FIVE,
            "4": CardRank.FOUR,
            "3": CardRank.THREE,
            "2": CardRank.TWO,
        }
        return map_symbols[symbol]
