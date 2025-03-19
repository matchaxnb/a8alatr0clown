from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from functools import total_ordering
from a8alatr0clown.definitions import CardRank, CardSuit, CardEdition
from random import shuffle


class InvalidCardException(Exception):
    pass


@total_ordering
@dataclass
class Card:
    """A playing card.

    Cards are sorted by suit, then rank, then edition"""

    suit: CardSuit
    rank: CardRank
    edition: CardEdition

    def _is_card(self, other):
        return (
            hasattr(other, "suit")
            and hasattr(other, "rank")
            and hasattr(other, "edition")
        )

    def __eq__(self, other):
        return self._is_card(other) and (self.suit, self.rank, self.edition) == (
            other.suit,
            other.rank,
            other.edition,
        )

    def __hash__(self):
        return hash(f"S{self.suit}\0R{self.rank}\0E{self.edition}")

    def __lt__(self, other):
        """Cards are sorted by suit, then rank, then edition"""
        return self._is_card(other) and (self.suit, self.rank, self.edition) < (
            other.suit,
            other.rank,
            other.edition,
        )

    def __str__(self):
        return f"""[{self.suit}{self.rank}] """

    @property
    def chip_base_value(self) -> int:
        """Return chip base value of card"""
        if self.rank == CardRank.ACE:
            return 11
        elif self.rank in (CardRank.KING, CardRank.QUEEN, CardRank.JACK):
            return 10
        else:
            return self.rank.value

    @classmethod
    def from_string(cls, ref_string: str) -> Card:
        if len(ref_string) not in (4, 5):
            raise InvalidCardException("wrong length")
        # Card.from_string("[♦10]")
        edition_1 = ref_string[0]
        edition_2 = ref_string[3]
        suit_sym = ref_string[1]
        rank_sym = ref_string[2]

        if len(ref_string) == 5:
            if ref_string[2:4] != "10":
                raise InvalidCardException("Wrong value")
            rank_sym = "10"
            edition_2 = ref_string[4]
        edition = None
        try:
            edition = CardEdition.from_symbols(edition_1, edition_2)
        except ValueError:
            raise InvalidCardException("Wrong symbols")
        try:
            rank = CardRank.from_symbol(rank_sym)
        except KeyError:
            raise InvalidCardException("Wrong rank")
        suit = None
        try:
            suit = CardSuit.from_symbol(suit_sym)
        except KeyError:
            raise InvalidCardException("Wrong suit")
        return Card(suit=suit, rank=rank, edition=edition)


@dataclass
class Hand:
    """A playing hand"""

    cards: List[Card]

    scoring_cards: List[Card] = field(default_factory=list)

    def __len__(self):
        return len(self.cards)


@dataclass
class Collection:
    """The collection of cards possessed by the player"""

    cards: List[Card]

    def add_card(self, card: Card):
        """Add a card to the collection"""
        self.cards.append(card)

    def remove_card(self, card: Card):
        """remove one instance of the given card from the collection."""
        raise NotImplementedError("implement Collection.remove_card")

    def create_shuffled_deck(self) -> Deck:
        """Return a shuffled deck from the collection of cards

        So that they are mixed!"""
        cards_in_deck = list(self.cards)
        shuffle(cards_in_deck)
        return Deck(cards=cards_in_deck)


@dataclass
class Deck:
    """The shuffled deck of the player"""

    cards: List[Card]

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        s = f"Deck of {len(self)} cards: "
        for c in self.cards:
            s += str(c)
        return s


@dataclass
class Discarded:
    """The discarded cards, in order of discard"""

    cards: List[Card]


@dataclass
class PlayingTable:
    deck: Deck
    discarded: Discarded
    hand: Hand


__all__ = ["PlayingTable", "Discarded", "Deck", "Collection", "Hand"]
