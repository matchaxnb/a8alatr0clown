from enum import IntEnum


class CardEdition(IntEnum):
    BASIC = 0
    FOIL = 1
    HOLOGRAPHIC = 2
    POLYCHROME = 3

    @classmethod
    def from_symbols(cls, sym1, sym2):
        if (sym1, sym2) == ("[", "]"):
            return CardEdition.BASIC
        elif (sym1, sym2) == (">", "<"):
            return CardEdition.HOLOGRAPHIC
        elif (sym1, sym2) == ("%", "%"):
            return CardEdition.FOIL
        elif (sym1, sym2) == ("*", "*"):
            return CardEdition.POLYCHROME
        else:
            raise ValueError(f"wrong symbols {sym1} & {sym2}")


class JokerEdition(IntEnum):
    BASIC = 0
    FOIL = 1
    HOLOGRAPHIC = 2
    POLYCHROME = 3
    NEGATIVE = 4
