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
        "ACP": Card(CLUB, ACE, POLY),
        "ADP": Card(DIAMOND, ACE, POLY),
        "KHB": Card(HEART, KING, BASIC),
        "KCB": Card(CLUB, KING, BASIC),
        "KSB": Card(SPADE, KING, BASIC),
        "KDB": Card(DIAMOND, KING, BASIC),
        "QDH": Card(DIAMOND, QUEEN, HOLO),
        "JDB": Card(DIAMOND, JACK, BASIC),
        "TDB": Card(DIAMOND, TEN, BASIC),
        "2CB": Card(CLUB, TWO, BASIC),
        "3CH": Card(CLUB, THREE, HOLO),
        "3CF": Card(CLUB, THREE, FOIL),
        "4CF": Card(CLUB, FOUR, FOIL),
        "4CH": Card(CLUB, FOUR, HOLO),
        "5HP": Card(HEART, FIVE, POLY),
        "5CH": Card(CLUB, FIVE, HOLO),
        # Additional cards for expanded test cases
        "ADB": Card(DIAMOND, ACE, BASIC),
        "ADH": Card(DIAMOND, ACE, HOLO),
        "ADF": Card(DIAMOND, ACE, FOIL),
        "ADB2": Card(DIAMOND, ACE, BASIC),
        "KHH": Card(HEART, KING, HOLO),
        "KHF": Card(HEART, KING, FOIL),
        "QHB": Card(HEART, QUEEN, BASIC),
        "QHH": Card(HEART, QUEEN, HOLO),
        "QDB": Card(DIAMOND, QUEEN, BASIC),
        "7DB": Card(DIAMOND, SEVEN, BASIC),
        "8DB": Card(DIAMOND, EIGHT, BASIC),
        "9DB": Card(DIAMOND, NINE, BASIC),
        "2HB": Card(HEART, TWO, BASIC),
        "3HB": Card(HEART, THREE, BASIC),
        "4HB": Card(HEART, FOUR, BASIC),
        "7HB": Card(HEART, SEVEN, BASIC),
        "THB": Card(HEART, TEN, BASIC),
        "JHB": Card(HEART, JACK, BASIC),
        "KDB2": Card(DIAMOND, KING, HOLO),
    }


def test_identify_basic_pair():
    """Verify that the hand solver validates a basic pair"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    pair_1 = Hand([c["ACP"], c["ACP"]])
    assert hs.solve_hand_type(pair_1) == HandType.PAIR


def test_identify_pair_in_full_hand():
    """Verify that the hand solver identifies a pair in a hand with more than just the two cards"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    pair_2 = Hand([c["ACP"], c["ADP"], c["3CH"], c["4CH"], c["5CH"]])

    assert hs.solve_hand_type(pair_2) == HandType.PAIR


def test_identify_pair_out_of_order():
    """Verify that the hand solver can find a pair even with non-contiguous cards"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    pair_3 = Hand([c["3CH"], c["ACP"], c["KCB"], c["QDH"], c["KSB"]])
    assert hs.solve_hand_type(pair_3) == HandType.PAIR


def test_find_contained_pair():
    """Verify that the hand solver finds a pair in hands that contain a pair but are not a pair"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    three_of_a_kind_hand = Hand([c["KSB"], c["KDB"], c["KHB"], c["QDH"], c["JDB"]])
    assert hs.hand_contains(three_of_a_kind_hand, HandType.PAIR)


def test_do_not_misidentify_pair():
    """Verify that the hand solver does not identify pairs when there is no pair to find"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    straight_hand = Hand([c["ACP"], c["2CB"], c["3CF"], c["4CF"], c["5HP"]])
    assert hs.solve_hand_type(straight_hand) != HandType.PAIR


def test_do_not_find_not_contained_pair():
    """Verify that the hand solver does not find a pair in a hand when there is none"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    straight_hand = Hand([c["ACP"], c["2CB"], c["3CF"], c["4CF"], c["5HP"]])
    assert not hs.hand_contains(straight_hand, HandType.PAIR)


def test_identify_two_pair():
    """Verify that the hand solver identifies two pairs"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KHB"], c["KCB"], c["QDB"], c["QDH"], c["2CB"]])
    assert hs.solve_hand_type(hand) == TWO_PAIR


def test_identify_three_of_a_kind():
    """Verify that the hand solver identifies three of a kind"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KHB"], c["KCB"], c["KSB"], c["QDB"], c["2CB"]])
    assert hs.solve_hand_type(hand) == THREE_OF_A_KIND


def test_identify_straight_ace_low():
    """Verify that the hand solver identifies an Ace-low straight (A-2-3-4-5)"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["ADB"], c["2CB"], c["3CH"], c["4CF"], c["5HP"]])
    assert hs.solve_hand_type(hand) == STRAIGHT


def test_identify_straight_ace_high():
    """Verify that the hand solver identifies an Ace-high straight (10-J-Q-K-A)"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["TDB"], c["JDB"], c["QDB"], c["KSB"], c["ADB"]])
    assert hs.solve_hand_type(hand) == STRAIGHT


def test_identify_flush():
    """Verify that the hand solver identifies a flush"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KHB"], c["QHB"], c["5HP"], c["2HB"], c["3HB"]])
    assert hs.solve_hand_type(hand) == FLUSH


def test_identify_full_house():
    """Verify that the hand solver identifies a full house"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KHB"], c["KCB"], c["KSB"], c["QDB"], c["QDH"]])
    assert hs.solve_hand_type(hand) == FULL_HOUSE


def test_identify_four_of_a_kind():
    """Verify that the hand solver identifies four of a kind"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KHB"], c["KCB"], c["KSB"], c["KDB"], c["QDH"]])
    assert hs.solve_hand_type(hand) == FOUR_OF_A_KIND


def test_identify_straight_flush():
    """Verify that the hand solver identifies a straight flush (non-royal)"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["7DB"], c["8DB"], c["9DB"], c["TDB"], c["JDB"]])
    assert hs.solve_hand_type(hand) == STRAIGHT_FLUSH


def test_identify_royal_flush():
    """Verify that the hand solver identifies a royal flush"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["TDB"], c["JDB"], c["QDB"], c["KDB"], c["ADB"]])
    assert hs.solve_hand_type(hand) == ROYAL_FLUSH
    assert hs.hand_contains(hand, STRAIGHT_FLUSH)


def test_identify_five_of_a_kind():
    """Verify that the hand solver identifies five of a kind"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KHB"], c["KCB"], c["KSB"], c["KDB"], c["KHH"]])
    assert hs.solve_hand_type(hand) == FIVE_OF_A_KIND


def test_identify_flush_house():
    """Verify that the hand solver identifies a flush house (full house + flush)"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KHB"], c["KHH"], c["KHF"], c["QHB"], c["QHH"]])
    assert hs.solve_hand_type(hand) == FLUSH_HOUSE


def test_identify_flush_five():
    """Verify that the hand solver identifies a flush five (five identical cards)"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["ADB"], c["ADH"], c["ADF"], c["ADP"], c["ADB2"]])
    assert hs.solve_hand_type(hand) == FLUSH_FIVE


def test_flush_not_straight_flush():
    """Verify that a flush is not mistaken for a straight flush"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KHB"], c["QHB"], c["5HP"], c["2HB"], c["3HB"]])
    assert hs.solve_hand_type(hand) == FLUSH
    assert not hs.hand_contains(hand, STRAIGHT_FLUSH)


def test_royal_is_straight_flush():
    """Verify that a royal flush is also a straight flush"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["TDB"], c["JDB"], c["QDB"], c["KDB"], c["ADB"]])
    assert hs.hand_contains(hand, STRAIGHT_FLUSH)


def test_flush_house_contains_full_house_and_flush():
    """Verify that a flush house contains both full house and flush"""
    c = _generate_card_fixtures()
    hs = HandSolver()
    hand = Hand([c["KHB"], c["KHH"], c["KHF"], c["QHB"], c["QHH"]])
    assert hs.hand_contains(hand, FULL_HOUSE)
    assert hs.hand_contains(hand, FLUSH)
