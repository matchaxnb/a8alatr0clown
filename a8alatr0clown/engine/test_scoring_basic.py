"""Scoring tests

These tests verify basic scoring rules without considering editions or modifiers
"""

from a8alatr0clown.definitions.modifiers import CardEdition
from .handsolver import HandSolver
from a8alatr0clown.definitions import HandType
from .playing_cards import Hand, Card, CardRank, CardSuit

DIAMOND = CardSuit.DIAMOND
HEART = CardSuit.HEART
SPADE = CardSuit.SPADE
CLUB = CardSuit.CLUB

ACE = CardRank.ACE
TWO = CardRank.TWO
THREE = CardRank.THREE
FOUR = CardRank.FOUR
FIVE = CardRank.FIVE
SIX = CardRank.SIX
SEVEN = CardRank.SEVEN
EIGHT = CardRank.EIGHT
NINE = CardRank.NINE
TEN = CardRank.TEN
JACK = CardRank.JACK
QUEEN = CardRank.QUEEN
KING = CardRank.KING

BASIC = CardEdition.BASIC
HOLO = CardEdition.HOLOGRAPHIC
FOIL = CardEdition.FOIL
POLY = CardEdition.POLYCHROME

PAIR = HandType.PAIR
TWO_PAIR = HandType.TWO_PAIR
THREE_OF_A_KIND = HandType.THREE_OF_A_KIND
STRAIGHT = HandType.STRAIGHT
FLUSH = HandType.FLUSH
FULL_HOUSE = HandType.FULL_HOUSE
FOUR_OF_A_KIND = HandType.FOUR_OF_A_KIND
STRAIGHT_FLUSH = HandType.STRAIGHT_FLUSH
ROYAL_FLUSH = HandType.ROYAL_FLUSH
FIVE_OF_A_KIND = HandType.FIVE_OF_A_KIND
FLUSH_HOUSE = HandType.FLUSH_HOUSE
FLUSH_FIVE = HandType.FLUSH_FIVE


def _generate_card_fixtures() -> dict:
    return {
        # High Card
        "AS1": Card(SPADE, ACE, BASIC),
        "2C": Card(CLUB, TWO, BASIC),
        "3D": Card(DIAMOND, THREE, BASIC),
        "4H": Card(HEART, FOUR, BASIC),
        "7S": Card(SPADE, SEVEN, BASIC),
        # Pair
        "AC1": Card(CLUB, ACE, BASIC),
        "AC2": Card(CLUB, ACE, BASIC),
        # Two Pair
        "KH1": Card(HEART, KING, BASIC),
        "KH2": Card(HEART, KING, BASIC),
        "QH1": Card(HEART, QUEEN, BASIC),
        "QH2": Card(HEART, QUEEN, BASIC),
        # Three of a Kind
        "KH3": Card(HEART, KING, BASIC),
        # Straight
        "5S": Card(SPADE, FIVE, BASIC),
        "6C": Card(CLUB, SIX, BASIC),
        # Flush
        "2H": Card(HEART, TWO, BASIC),
        "3H": Card(HEART, THREE, BASIC),
        "5H": Card(HEART, FIVE, BASIC),
        # Full House
        "QH3": Card(HEART, QUEEN, BASIC),
        # Four of a Kind
        "KH4": Card(HEART, KING, BASIC),
        # Straight Flush
        "7D": Card(DIAMOND, SEVEN, BASIC),
        "8D": Card(DIAMOND, EIGHT, BASIC),
        "9D": Card(DIAMOND, NINE, BASIC),
        "TD": Card(DIAMOND, TEN, BASIC),
        "JD": Card(DIAMOND, JACK, BASIC),
        # Royal Flush
        "QD": Card(DIAMOND, QUEEN, BASIC),
        "KD": Card(DIAMOND, KING, BASIC),
        "AD": Card(DIAMOND, ACE, BASIC),
        # Five of a Kind
        "KH5": Card(HEART, KING, BASIC),
        # Flush House
        "KH6": Card(HEART, KING, BASIC),
        "KH7": Card(HEART, KING, BASIC),
        "QH4": Card(HEART, QUEEN, BASIC),
        # Flush Five
        "AS2": Card(SPADE, ACE, BASIC),
        "AS3": Card(SPADE, ACE, BASIC),
        "AS4": Card(SPADE, ACE, BASIC),
        "AS5": Card(SPADE, ACE, BASIC),
    }


def test_score_high_card():
    """High Card: Ace (11) + base 5 chips. Mult 1."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["AS1"], c["2C"], c["3D"], c["4H"], c["7S"]])
    assert hs.compute_hand_score(hand) == (16, 16, 1)


def test_score_pair():
    """Pair: 10 + 11*2 = 32 chips. Mult 2."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["AC1"], c["AC2"], c["3D"], c["4H"], c["7S"]])
    assert hs.compute_hand_score(hand) == (64, 32, 2)


def test_score_two_pair():
    """Two Pair: 20 + 11*2 +10*2 =62. Mult 2."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["AC1"], c["AC2"], c["KH1"], c["KH2"], c["2C"]])
    assert hs.compute_hand_score(hand) == (124, 62, 2)


def test_score_three_of_a_kind():
    """Three of a Kind: 30 +10*3=60. Mult 3."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KH1"], c["KH2"], c["KH3"], c["QH1"], c["2C"]])
    assert hs.compute_hand_score(hand) == (180, 60, 3)


def test_score_straight():
    """Straight: 30 +2+3+4+5+6=50. Mult 4."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["2C"], c["3D"], c["4H"], c["5S"], c["6C"]])
    assert hs.compute_hand_score(hand) == (200, 50, 4)


def test_score_flush():
    """Flush: 35 +10+10+2+3+5=65. Mult 4."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KH1"], c["QH1"], c["2H"], c["3H"], c["5H"]])
    assert hs.compute_hand_score(hand) == (260, 65, 4)


def test_score_full_house():
    """Full House: 40 +10*3 +10*2=90. Mult 4."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KH1"], c["KH2"], c["KD"], c["QH1"], c["QH2"]])
    assert hs.compute_hand_score(hand) == (360, 90, 4)


def test_score_four_of_a_kind():
    """Four of a Kind:60 +10*4=100. Mult7."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KH1"], c["KH2"], c["KH3"], c["KH4"], c["QH1"]])
    assert hs.compute_hand_score(hand) == (700, 100, 7)


def test_score_straight_flush():
    """Straight Flush:100 +7+8+9+10+10=144. Mult8."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["7D"], c["8D"], c["9D"], c["TD"], c["JD"]])
    assert hs.compute_hand_score(hand) == (1152, 144, 8)


def test_score_royal_flush():
    """Royal Flush:100 +10*4 +11=151. Mult8."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["TD"], c["JD"], c["QD"], c["KD"], c["AD"]])
    assert hs.compute_hand_score(hand) == (1208, 151, 8)


def test_score_five_of_a_kind():
    """Five of a Kind:120 +10*5=170. Mult12."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KH1"], c["KH2"], c["KH3"], c["KH4"], c["KD"]])
    assert hs.compute_hand_score(hand) == (2040, 170, 12)


def test_score_flush_house():
    """Flush House:140 +10*3 +10*2=190. Mult14."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KH1"], c["KH2"], c["KH3"], c["QH1"], c["QH2"]])
    assert hs.compute_hand_score(hand) == (2660, 190, 14)


def test_score_flush_five():
    """Flush Five:160 +11*5=215. Mult16."""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["AS1"], c["AS2"], c["AS3"], c["AS4"], c["AS5"]])
    assert hs.compute_hand_score(hand) == (3440, 215, 16)
