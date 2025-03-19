from a8alatr0clown.definitions import HandType, CardSuit, CardRank
from a8alatr0clown.definitions.modifiers import CardEdition
from .playing_cards import Hand, Card
from decimal import Decimal
from typing import Tuple


class HandSolver:
    def __init__(self):
        """
        Nom,Chips,Mult
        High Card,5,1
        Pair,10,2
        Two Pair,20,2
        Three of a Kind,30,3
        Straight,30,4
        Flush,35,4
        Full House,40,4
        Four of a Kind,60,7
        Straight Flush,100,8
        Royal Flush,100,8

        """
        self.hand_type_attrs = {
            HandType.HIGH_CARD: (5, 1),
            HandType.PAIR: (10, 2),
            HandType.TWO_PAIR: (20, 2),
            HandType.THREE_OF_A_KIND: (30, 3),
            HandType.STRAIGHT: (30, 4),
            HandType.FLUSH: (35, 4),
            HandType.FULL_HOUSE: (40, 4),
            HandType.FOUR_OF_A_KIND: (60, 7),
            HandType.STRAIGHT_FLUSH: (100, 8),
            HandType.ROYAL_FLUSH: (100, 8),
            HandType.FIVE_OF_A_KIND: (120, 12),
            HandType.FLUSH_HOUSE: (140, 14),
            HandType.FLUSH_FIVE: (160, 16),
        }

    def compute_hand_score(self, hand: Hand) -> Tuple[Decimal, Decimal, Decimal]:
        """Compute the score of a hand

        Returns: (total score, chips count, mult factor)
        """
        hand_type = self.solve_hand_type(hand)
        chip, mult = self.hand_type_attrs[hand_type]
        if hand_type == HandType.HIGH_CARD:
            cards_sorted = sorted(hand.cards, key=lambda x: (x.chip_base_value, x.rank))
            c = cards_sorted[-1]
            hand.scoring_cards.append(c)
        elif hand_type in (
            HandType.FIVE_OF_A_KIND,
            HandType.FLUSH,
            HandType.FLUSH_FIVE,
            HandType.FLUSH_HOUSE,
            HandType.STRAIGHT,
            HandType.STRAIGHT_FLUSH,
            HandType.ROYAL_FLUSH,
            HandType.FULL_HOUSE,
        ):
            hand.scoring_cards = list(hand.cards)
        elif hand_type in (HandType.PAIR, HandType.TWO_PAIR):
            met_ranks = {}
            for idx, card in enumerate(hand.cards):
                if card.rank in met_ranks and card not in hand.scoring_cards:
                    hand.scoring_cards.append(hand.cards[met_ranks[card.rank]])
                    hand.scoring_cards.append(card)
                met_ranks[card.rank] = idx
        elif hand_type == HandType.THREE_OF_A_KIND:
            met_ranks = {}
            for idx, card in enumerate(hand.cards):
                if card.rank in met_ranks:
                    met_ranks[card.rank].append(idx)
                else:
                    met_ranks[card.rank] = [idx]
                if len(met_ranks[card.rank]) == 3:
                    hand.scoring_cards = [hand.cards[a] for a in met_ranks[card.rank]]
        elif hand_type == HandType.FOUR_OF_A_KIND:
            met_ranks = {}
            for idx, card in enumerate(hand.cards):
                if card.rank in met_ranks:
                    met_ranks[card.rank].append(idx)
                else:
                    met_ranks[card.rank] = [idx]
                if len(met_ranks[card.rank]) == 4:
                    hand.scoring_cards = [hand.cards[a] for a in met_ranks[card.rank]]

        for card in hand.scoring_cards:
            chip += card.chip_base_value
            edition = card.edition
            if edition == CardEdition.FOIL:
                chip += 50
            elif edition == CardEdition.HOLOGRAPHIC:
                mult += 10
            elif edition == CardEdition.POLYCHROME:
                mult *= 1.5

        return (chip * mult, chip, mult)

    def solve_hand_type(self, hand: Hand) -> HandType:
        """Identify the hand type of the given hand"""
        contains_flush = self.hand_contains(hand, HandType.FLUSH)
        contains_5oak = self.hand_contains(hand, HandType.FIVE_OF_A_KIND)
        contains_4oak = self.hand_contains(hand, HandType.FOUR_OF_A_KIND)
        contains_3oak = self.hand_contains(hand, HandType.THREE_OF_A_KIND)
        contains_2pair = self.hand_contains(hand, HandType.TWO_PAIR)
        contains_pair = self.hand_contains(hand, HandType.PAIR)
        contains_fullhouse = self.hand_contains(hand, HandType.FULL_HOUSE)
        contains_straight = self.hand_contains(hand, HandType.STRAIGHT)
        contains_ace = (
            len(list(filter(lambda x: x.rank == CardRank.ACE, hand.cards))) > 0
        )
        contains_king = (
            len(list(filter(lambda x: x.rank == CardRank.KING, hand.cards))) > 0
        )
        if contains_flush and contains_5oak:
            return HandType.FLUSH_FIVE
        elif contains_flush and contains_fullhouse:
            return HandType.FLUSH_HOUSE
        elif contains_5oak:
            return HandType.FIVE_OF_A_KIND
        elif contains_flush and contains_straight and contains_ace and contains_king:
            return HandType.ROYAL_FLUSH
        elif contains_flush and contains_straight:
            return HandType.STRAIGHT_FLUSH
        elif contains_4oak:
            return HandType.FOUR_OF_A_KIND
        elif contains_fullhouse:
            return HandType.FULL_HOUSE
        elif contains_flush:
            return HandType.FLUSH
        elif contains_straight:
            return HandType.STRAIGHT
        elif contains_3oak:
            return HandType.THREE_OF_A_KIND
        elif contains_2pair:
            return HandType.TWO_PAIR
        elif contains_pair:
            return HandType.PAIR
        else:
            return HandType.HIGH_CARD

    def hand_contains(self, hand: Hand, hand_type: HandType) -> bool:
        """Tells if a hand contains a given type"""
        met_card_ranks = {}
        met_card_suits = {}

        for card in hand.cards:
            if card.rank in met_card_ranks:
                met_card_ranks[card.rank] += 1
            else:
                met_card_ranks[card.rank] = 1
            if card.suit in met_card_suits:
                met_card_suits[card.suit] += 1
            else:
                met_card_suits[card.suit] = 1

        if hand_type == HandType.FLUSH:
            for card_suit, card_count in met_card_suits.items():
                if card_count == 5:
                    return True
                return False

        pairs_met = 0
        contains_5oak = False
        contains_4oak = False
        contains_3oak = False
        contains_pair = False
        contains_2pair = False
        for card_rank, count in met_card_ranks.items():
            if count >= 5:
                contains_5oak = True
            if count >= 4:
                contains_4oak = True
            if count >= 3:
                contains_3oak = True
            if count >= 2:
                contains_pair = True
                pairs_met += 1
        if pairs_met >= 2:
            contains_2pair = True

        if hand_type == HandType.STRAIGHT:
            if len(hand.cards) < 5:
                return False
            sorted_by_ranks = sorted(hand.cards, key=lambda x: x.rank)
            previous_rank = sorted_by_ranks[0].rank
            if previous_rank == CardRank.ACE:
                ranks = tuple(c.rank for c in sorted_by_ranks)
                return ranks in [
                    (
                        CardRank.ACE,
                        CardRank.TEN,
                        CardRank.JACK,
                        CardRank.QUEEN,
                        CardRank.KING,
                    ),
                    (
                        CardRank.ACE,
                        CardRank.TWO,
                        CardRank.THREE,
                        CardRank.FOUR,
                        CardRank.FIVE,
                    ),
                ]
                # A 2 3 4 5
                # 10 J Q K A
            for card in sorted_by_ranks[1:]:
                if card.rank.value - previous_rank.value != 1:
                    return False
                previous_rank = card.rank
            return True

        if hand_type == HandType.FULL_HOUSE:
            return pairs_met >= 2 and contains_3oak
        elif hand_type == HandType.PAIR:
            return contains_pair
        elif hand_type == HandType.TWO_PAIR:
            return contains_2pair
        elif hand_type == HandType.THREE_OF_A_KIND:
            return contains_3oak
        elif hand_type == HandType.FOUR_OF_A_KIND:
            return contains_4oak
        elif hand_type == HandType.FIVE_OF_A_KIND:
            return contains_5oak
        elif hand_type == HandType.STRAIGHT_FLUSH:
            return self.hand_contains(hand, HandType.STRAIGHT) and self.hand_contains(
                hand, HandType.FLUSH
            )
        else:
            raise ValueError(f"not implemented hand type {hand_type}")
