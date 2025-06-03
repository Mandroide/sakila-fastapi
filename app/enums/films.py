from enum import Enum


class Language(str, Enum):
    english = "English"
    spanish = "Spanish"

    @staticmethod
    def values() -> list[str]:
        return list(map(lambda c: c.value, Language))


class Rating(str, Enum):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"

    @staticmethod
    def values(cls: type[Enum]) -> list[str]:
        return list(map(lambda c: c.value, cls))
