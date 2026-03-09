from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle, DefaultOnToggle, Choice, Range, NamedRange, OptionGroup


class CharWinsCount(NamedRange):
    """
    Alter the number of wins required for any "100 wins playing as X" challenges.

    - **Default**: Require only 5 wins per character.
    - **Exclude**: Require 100 wins per character, but exclude from logic. Every challenge that has this condition uses it as an alternative, so this doesn't remove any locations.
    - **Vanilla**: Require 100 wins per character, in logic. Not recommended.
    """

    internal_name = "character_wins_count"
    display_name = "Character Wins Count"
    range_start = 1
    range_end = 100
    default = 5
    special_range_names = {
        "default": 5,
        "vanilla": 100,
        "exclude": 0,
    }


@dataclass
class RingRacersOptions(PerGameCommonOptions):
    character_wins_count: CharWinsCount
