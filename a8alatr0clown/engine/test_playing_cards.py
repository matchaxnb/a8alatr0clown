from a8alatr0clown.definitions import CardRank, CardSuit, CardEdition
from a8alatr0clown.engine import Collection, Card, Deck
import pytest

from a8alatr0clown.engine.playing_cards import InvalidCardException


def generate_basic_card_collection() -> Collection:
    card_pack = list()
    for suit in CardSuit:
        for rank in CardRank:
            card_pack.append(Card(suit=suit, rank=rank, edition=CardEdition.BASIC))
    return Collection(card_pack)


def generate_sorted_deck():
    collection = generate_basic_card_collection()
    sorted_list = sorted(collection.cards)
    return Deck(cards=sorted_list)


def test_card_presence_in_deck_basic():
    """Test if ace of spades is present in generated deck"""
    sorted_deck = generate_sorted_deck()
    ACE_OF_SPADES = Card(
        suit=CardSuit.SPADE, rank=CardRank.ACE, edition=CardEdition.BASIC
    )
    assert ACE_OF_SPADES in sorted_deck.cards


def test_card_presence_total():
    """Test if all basic cards are present in generated deck"""
    sorted_deck = generate_sorted_deck()
    for suit in CardSuit:
        for rank in CardRank:
            c = Card(suit=suit, rank=rank, edition=CardEdition.BASIC)
            assert c in sorted_deck.cards


def test_card_absence_basic():
    """Ensure that the holographic jack of diamond is not present in generated deck"""
    holo_jack_of_diamonds = Card(
        suit=CardSuit.DIAMOND, rank=CardRank.JACK, edition=CardEdition.HOLOGRAPHIC
    )
    sorted_deck = generate_sorted_deck()
    assert holo_jack_of_diamonds not in sorted_deck.cards


def test_add_card_works():
    """Ensure we can add a card to a collection"""
    collection = generate_basic_card_collection()
    holo_jack_of_diamonds = Card(
        suit=CardSuit.DIAMOND, rank=CardRank.JACK, edition=CardEdition.HOLOGRAPHIC
    )
    assert holo_jack_of_diamonds not in collection.cards
    collection.add_card(holo_jack_of_diamonds)
    assert holo_jack_of_diamonds in collection.cards


def test_shuffle_pack():
    """Ensure pack shuffling works statistically speaking by shuffling it 30 times and verify if it's different enough"""
    collection = generate_basic_card_collection()
    shuffled_deck = collection.create_shuffled_deck()
    total_identical_cards = 0
    total_different_cards = 0
    for i in range(1, 30):
        new_shuffled_deck = collection.create_shuffled_deck()
        for c1, c2 in zip(shuffled_deck.cards, new_shuffled_deck.cards):
            if c1 == c2:
                total_identical_cards += 1
            else:
                total_different_cards += 1
        shuffled_deck = new_shuffled_deck
    print("Identical cards:", total_identical_cards)
    print("Different cards", total_different_cards)
    assert total_different_cards > total_identical_cards


def test_make_cards_from_string():
    """Ensure Card.from_string generates cards from strings nicely, using the implied format"""
    basic_jack_of_diamonds = Card(
        suit=CardSuit.DIAMOND, rank=CardRank.JACK, edition=CardEdition.BASIC
    )
    holo_ace_of_spades = Card(
        suit=CardSuit.SPADE, rank=CardRank.ACE, edition=CardEdition.HOLOGRAPHIC
    )
    foil_two_of_clubs = Card(
        suit=CardSuit.CLUB, rank=CardRank.TWO, edition=CardEdition.FOIL
    )
    poly_king_of_hearts = Card(
        suit=CardSuit.HEART, rank=CardRank.KING, edition=CardEdition.POLYCHROME
    )
    assert Card.from_string("[♦J]") == basic_jack_of_diamonds
    assert Card.from_string(">♠A<") == holo_ace_of_spades
    assert Card.from_string("%♣2%") == foil_two_of_clubs
    assert Card.from_string("*♥K*") == poly_king_of_hearts
    with pytest.raises(InvalidCardException):
        Card.from_string("♣♦")
